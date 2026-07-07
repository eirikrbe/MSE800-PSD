
import calendar
import os
import re
from datetime import date

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError, field_validator

load_dotenv()


# ---------------------------------------------------------------------------
# 1. Schemas — TripRequest validates the traveller's answers before any tokens
#    are spent; Itinerary is the structure Gemini is forced to fill.
# ---------------------------------------------------------------------------

class Activity(BaseModel):
    name: str = Field(description="Name of the place or activity")
    address: str = Field(description="Street address or location, town")
    description: str = Field(description="2-3 sentence description and why it suits this traveller")
    duration_hours: float = Field(description="Realistic time to spend here, in hours")


class Day(BaseModel):
    day_number: int
    base_town: str = Field(description="Town/city where the traveller sleeps this night")
    driving_note: str = Field(description="Route and realistic driving time from previous base, or 'No driving today'")
    activities: list[Activity] = Field(description="1 to 3 activities, in visiting order")


class Itinerary(BaseModel):
    title: str = Field(description="Catchy trip title mentioning New Zealand")
    overview: str = Field(description="3-4 sentence summary of the whole trip")
    feasibility_note: str = Field(description="One honest sentence: either 'Feasible as requested' or which constraint conflicts with the requested route/days/transport and what change you recommend")
    days: list[Day]
    packing_tips: list[str] = Field(description="3-5 season-specific packing tips")


class TripRequest(BaseModel):
    """Traveller input. Pydantic coerces the raw strings from input()
    (e.g. "7" -> 7) and rejects out-of-range values before the API call."""
    days: int = Field(ge=1, le=21)
    month: str
    start_city: str = Field(min_length=1)
    end_city: str = Field(min_length=1)
    budget: str
    transport: str
    interests: str
    age: int = Field(ge=1, le=110)

    @field_validator("month")
    @classmethod
    def month_must_be_real(cls, value: str) -> str:
        value = value.capitalize()
        if value not in calendar.month_name:
            raise ValueError("must be a real month name, e.g. December")
        return value


# ---------------------------------------------------------------------------
# 2. Prompt construction — the prompt-engineering techniques live here.
# ---------------------------------------------------------------------------

SYSTEM_INSTRUCTION = """\
You are Kiri, a senior New Zealand travel planner with 20 years of experience
designing self-drive itineraries. You know real driving times between NZ towns,
seasonal conditions (e.g. Tongariro Crossing and high-country roads in winter),
and you never invent places that do not exist."""


def build_prompt(trip: TripRequest) -> str:
    """Build the user prompt. Techniques used:
    - Delimiters (### blocks) to separate data from instructions.
    - Explicit hard constraints the model must respect.
    - A few-shot example showing the expected quality for ONE day.
    """
    return f"""\
Plan a New Zealand trip using the traveller details below.

### TRAVELLER DETAILS
- Trip length: {trip.days} days
- Travel month: {trip.month}
- Start city: {trip.start_city}
- End city: {trip.end_city}
- Budget level: {trip.budget}
- Transport: {trip.transport}
- Interests: {trip.interests}
- Traveller age: {trip.age}

### HARD CONSTRAINTS
1. Maximum 3 activities per day; fewer on long driving days.
2. Driving legs must be realistic for NZ roads (assume ~70 km/h average).
   Never schedule more than 4.5 hours of driving in one day.
3. Every activity must be a real, named place with its real town.
4. Match activities to the travel month (season, opening, weather).
5. Match intensity to the traveller's age and stated interests.
6. Day 1 starts in {trip.start_city}; the final day ends in {trip.end_city}.
7. Keep each day's total load (driving hours + activity hours) under 9 hours.
8. Use the stated transport for the entire trip — no flights. A rental car
   crosses Cook Strait via the Interislander ferry (Wellington to Picton,
   about 3.5 hours; rental cars are normally swapped at the ferry terminals).
9. If driving_note says 'No driving today', every activity that day must be
   walkable or reachable by local transport from the base town.
10. If the route, trip length and transport cannot all fit within the driving
    cap, still produce the best itinerary you can, but say so honestly in
    feasibility_note and recommend a change (more days, a different start
    city, or allowing one domestic flight). Never hide a broken constraint.

### QUALITY EXAMPLE (one day, for style and detail level only — do not copy)
Day 3 — Base: Rotorua. Driving: Taupo to Rotorua via SH5, about 1 hour.
Activities: Te Puia (Hemo Rd, Tihiotonga, Rotorua) — geothermal valley and
Maori cultural centre; watch the Pohutu geyser and a carving school in action,
a relaxed 3-hour visit that suits any fitness level.

Now produce the full {trip.days}-day itinerary in the required JSON structure.
"""


# ---------------------------------------------------------------------------
# 3. Rendering — turn the validated object into Markdown.
# ---------------------------------------------------------------------------

def render_markdown(itinerary: Itinerary, trip: TripRequest) -> str:
    lines = [
        f"# {itinerary.title}",
        "",
        f"*{trip.days} days | {trip.month} | {trip.start_city} to {trip.end_city}"
        f" | {trip.budget} budget | by {trip.transport}*",
        "",
        itinerary.overview,
        "",
        f"> **Feasibility:** {itinerary.feasibility_note}",
        "",
    ]
    for day in itinerary.days:
        lines += [f"## Day {day.day_number} — {day.base_town}", "", f"**Getting there:** {day.driving_note}", ""]
        for act in day.activities:
            lines += [
                f"### {act.name} ({act.duration_hours:g}h)",
                f"*{act.address}*",
                "",
                act.description,
                "",
            ]
    lines += ["## Packing tips", ""]
    lines += [f"- {tip}" for tip in itinerary.packing_tips]
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 4. Token counting — official Gemini APIs.
#    Before the call: client.models.count_tokens() measures the prompt.
#    After the call: response.usage_metadata reports actual consumption.
# ---------------------------------------------------------------------------

MODEL = "gemini-2.5-flash"

# Thinking tokens are billed at the output rate and dominated the bill (~70%).
# 512 keeps enough reasoning for realistic routing; 0 disables thinking entirely.
THINKING_BUDGET = 512


def count_prompt_tokens(client: genai.Client, prompt: str) -> None:
    result = client.models.count_tokens(model=MODEL, contents=prompt)
    print(f"[tokens] Prompt size before sending: {result.total_tokens} tokens "
          "(via count_tokens; system instruction counted separately by the API)")


def report_token_usage(response) -> None:
    usage = response.usage_metadata
    if usage is None:
        return
    print("\n[tokens] Actual usage for this request (usage_metadata):")
    print(f"  input (prompt):      {usage.prompt_token_count}")
    if usage.thoughts_token_count:
        print(f"  thinking:            {usage.thoughts_token_count}")
    print(f"  output (candidates): {usage.candidates_token_count}")
    print(f"  total billed:        {usage.total_token_count}")


# ---------------------------------------------------------------------------
# 5. Evaluation — two tiers.
#    Tier 1: check_rules() re-tests the HARD CONSTRAINTS in plain Python.
#            Costs zero tokens, so it always runs.
#    Tier 2: judge_itinerary() is an LLM-as-judge call grading what code
#            cannot check (real places, realistic driving, season fit).
#            A stronger model grades the cheaper one, because a model
#            reviewing its own output shares its own blind spots.
# ---------------------------------------------------------------------------

JUDGE_MODEL = "gemini-2.5-flash"   # set to MODEL to judge on the cheap


class Evaluation(BaseModel):
    critical: list[str] = Field(description="Trip-breaking problems: place does not exist, activity in the wrong town or wrong season, driving leg not possible as described")
    warnings: list[str] = Field(description="Real problems the trip survives: overloaded day, no buffer time, opening-hours conflict, underestimated driving")
    suggestions: list[str] = Field(description="Improvements, not problems: better base town, a stated interest not yet served, pacing tweaks")


JUDGE_INSTRUCTION = """\
You are a strict reviewer of New Zealand self-drive itineraries. Sort every
problem you find into exactly one bucket:
- critical: the trip cannot happen as written.
- warnings: real problems the trip would survive.
- suggestions: improvements, not problems.
At most 5 items per bucket; an empty bucket is a valid answer. Do not rewrite
the itinerary, do not praise it, and do not invent problems."""


def check_rules(itinerary: Itinerary, trip: TripRequest) -> list[str]:
    problems = []
    if len(itinerary.days) != trip.days:
        problems.append(f"Expected {trip.days} days, got {len(itinerary.days)}.")
    numbers = [d.day_number for d in itinerary.days]
    if numbers != list(range(1, len(numbers) + 1)):
        problems.append(f"Day numbers are not sequential: {numbers}")
    for day in itinerary.days:
        if not 1 <= len(day.activities) <= 3:
            problems.append(f"Day {day.day_number} has {len(day.activities)} activities (allowed 1-3).")
        # Heuristic: pull hour figures out of the driving note and compare to the caps.
        hours = re.findall(r"(\d+(?:\.\d+)?)\s*(?:hours?|hrs?)", day.driving_note.lower())
        driving = max((float(h) for h in hours), default=0.0)
        if driving > 4.5:
            problems.append(f"Day {day.day_number} driving may exceed 4.5 h: '{day.driving_note}'")
        load = driving + sum(a.duration_hours for a in day.activities)
        if load > 9:
            problems.append(f"Day {day.day_number} is overloaded: ~{load:g} h of driving/ferry plus activities.")
    if not 3 <= len(itinerary.packing_tips) <= 5:
        problems.append(f"Expected 3-5 packing tips, got {len(itinerary.packing_tips)}.")
    if trip.end_city.lower() not in itinerary.days[-1].base_town.lower():
        problems.append(f"Final day is based in {itinerary.days[-1].base_town}, not {trip.end_city}.")
    return problems


def judge_itinerary(client: genai.Client, markdown: str, trip: TripRequest) -> Evaluation | None:
    prompt = f"""\
Review the itinerary below, written for a {trip.age}-year-old travelling in
{trip.month} on a {trip.budget} budget by {trip.transport}.
Stated interests: {trip.interests}.

### ITINERARY
{markdown}
"""
    response = client.models.generate_content(
        model=JUDGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=JUDGE_INSTRUCTION,
            temperature=0.0,   # grading should be deterministic, not creative
            response_mime_type="application/json",
            response_schema=Evaluation,
            thinking_config=types.ThinkingConfig(thinking_budget=THINKING_BUDGET),
        ),
    )
    report_token_usage(response)
    verdict = response.parsed
    return verdict if isinstance(verdict, Evaluation) else None


# ---------------------------------------------------------------------------
# 6. Main flow — gather inputs, validate, ONE API call, save, evaluate.
# ---------------------------------------------------------------------------

def ask(question: str, default: str) -> str:
    answer = input(f"{question} [{default}]: ").strip()
    return answer or default


def main():
    print("=== New Zealand Itinerary Generator ===\n(press Enter to accept a default)\n")

    try:
        trip = TripRequest(
            days=ask("How many days", "7"),
            month=ask("Which month are you travelling", "December"),
            start_city=ask("Start city", "Christchurch"),
            end_city=ask("End city", "Queenstown"),
            budget=ask("Budget level (backpacker / mid-range / luxury)", "mid-range"),
            transport=ask("Transport (rental car / campervan / bus)", "rental car"),
            interests=ask("Interests (comma-separated)", "hiking, Maori culture, food and wine"),
            age=ask("Your age", "30"),
        )
    except ValidationError as e:
        print("\nPlease fix these inputs (no API call was made):")
        for err in e.errors():
            print(f"  - {err['loc'][0]}: {err['msg']}")
        return

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = build_prompt(trip)

    try:
        count_prompt_tokens(client, prompt)
    except Exception as e:
        print("Warning: count_tokens failed:", e)

    print("\nGenerating your itinerary (one request, ~20-40 seconds)...\n")
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
                response_mime_type="application/json",
                response_schema=Itinerary,   # <-- schema-enforced output
                thinking_config=types.ThinkingConfig(thinking_budget=THINKING_BUDGET),
            ),
        )
    except Exception as e:
        print("Error communicating with Gemini:", e)
        return

    report_token_usage(response)

    # response.parsed is already an Itinerary instance validated by Pydantic.
    itinerary = response.parsed
    if not isinstance(itinerary, Itinerary):
        print("Model returned no parseable itinerary. Raw output:\n", response.text)
        return

    markdown = render_markdown(itinerary, trip)
    print(markdown)

    filename = f"itinerary_{trip.start_city}_to_{trip.end_city}_{date.today()}.md".replace(" ", "_")
    with open(filename, "w") as f:
        f.write(markdown)
    print(f"\nSaved to {filename}")

    # --- Tier 1: free rule checks -----------------------------------------
    print("\n=== Evaluation: rule checks (0 tokens) ===")
    problems = check_rules(itinerary, trip)
    if problems:
        for p in problems:
            print(f"  - {p}")
    else:
        print("  All hard constraints satisfied.")

    # --- Tier 2: optional LLM judge (one extra billed call) ---------------
    if ask("\nRun LLM judge for issue triage? (y/n)", "n").lower().startswith("y"):
        print(f"\n=== Evaluation: LLM judge ({JUDGE_MODEL}) ===")
        try:
            verdict = judge_itinerary(client, markdown, trip)
        except Exception as e:
            print("Judge call failed:", e)
            return
        if verdict is None:
            print("Judge returned no parseable evaluation.")
            return
        if verdict.critical:
            print("\n  Critical — the trip breaks without fixing these:")
            for item in verdict.critical:
                print(f"  ⚠ {item}")
        if verdict.warnings:
            print("\n  Warnings — the trip suffers but survives:")
            for item in verdict.warnings:
                print(f"  • {item}")
        if verdict.suggestions:
            print("\n  Suggestions — improvements, not problems:")
            for item in verdict.suggestions:
                print(f"  • {item}")
        if not (verdict.critical or verdict.warnings or verdict.suggestions):
            print("\n  Clean — no issues in any bucket.")


if __name__ == "__main__":
    main()

