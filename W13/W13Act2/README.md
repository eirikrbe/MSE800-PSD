# Week 13 – Activity 2: LLM-Powered New Zealand Travel Itinerary Generator

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/eirikrbe/MSE800-PSD/tree/main/W13/W13Act2)

Command-line program that generates a self-drive New Zealand travel itinerary
with the Google Gemini API. The traveller answers eight questions (trip length,
month, route, budget, transport, interests, age) and the program makes ONE
API call that returns a schema-enforced JSON itinerary, renders it to Markdown,
and then evaluates its own output. The main features are prompt engineering, token-cost control, and evaluation of LLM output through LLM-as-judge.

## Overview

The program runs as a pipeline:

```mermaid
flowchart TD
    A[Traveller answers 8 questions]
    --> B{TripRequest validation<br>Pydantic}

    B -- Invalid --> X[Validation errors<br>0 tokens]

    B -- Valid --> C[Build optimized prompt]

    C --> C1[Count prompt tokens]

    C1 --> D[Single Gemini inference<br>Thinking budget = 512]

    D --> E[Pydantic parses JSON<br>Itinerary object]

    E --> F[Render Markdown]

    F --> G[Tier 1 rule checks<br>0 tokens]

    G --> H{Run LLM judge?}

    H -- Yes --> I[Tier 2 quality review]

    H -- No --> J[Done]

    I --> J
```

1. **Validate input** — a Pydantic `TripRequest` model checks every answer
   (days 1–21, real month name, sensible age) *before* any tokens are spent,
   so bad input never costs an API call.
2. **One Gemini call** — the prompt is built from the answers and the response
   is forced into the `Itinerary` schema via `response_schema`, so the output
   is always validated JSON, never free text.
3. **Render** — the itinerary object becomes a Markdown file, opening with an
   honest **Feasibility** note.
4. **Evaluate** — free rule checks always run; an optional LLM-as-judge call
   triages the remaining issues by severity.

Unlike a traditional software application, an LLM application cannot assume
that every generated response is correct.

This project therefore treats the LLM as a probabilistic component rather than
a deterministic function. Instead of trusting the first response, the
application validates inputs, constrains outputs with a schema, measures token
usage, performs rule-based verification, and optionally asks a second LLM to
critique the result.

## The Optimized Prompt

The prompt combines five techniques: a **role persona** (system instruction),
**delimiters** separating data from instructions, **numbered hard
constraints**, a **few-shot quality example**, and an **escape hatch** that
tells the model to admit when the request itself is infeasible instead of
silently breaking a constraint.

System instruction:

```text
You are Kiri, a senior New Zealand travel planner with 20 years of experience
designing self-drive itineraries. You know real driving times between NZ towns,
seasonal conditions (e.g. Tongariro Crossing and high-country roads in winter),
and you never invent places that do not exist.
```

User prompt template (`{fields}` are filled from the validated `TripRequest`):

```text
Plan a New Zealand trip using the traveller details below.

### TRAVELLER DETAILS
- Trip length: {days} days
- Travel month: {month}
- Start city: {start_city}
- End city: {end_city}
- Budget level: {budget}
- Transport: {transport}
- Interests: {interests}
- Traveller age: {age}

### HARD CONSTRAINTS
1. Maximum 3 activities per day; fewer on long driving days.
2. Driving legs must be realistic for NZ roads (assume ~70 km/h average).
   Never schedule more than 4.5 hours of driving in one day.
3. Every activity must be a real, named place with its real town.
4. Match activities to the travel month (season, opening, weather).
5. Match intensity to the traveller's age and stated interests.
6. Day 1 starts in {start_city}; the final day ends in {end_city}.
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

Now produce the full {days}-day itinerary in the required JSON structure.
```

## Sample AI-Generated Itinerary

[itinerary_Christchurch_to_Queenstown_2026-07-07.md](itinerary_Christchurch_to_Queenstown_2026-07-07.md)
— 7 days, December, mid-range budget, by rental car.

## Token-Cost Optimization

The first run billed 5,129 tokens, and 71% of that was *thinking* tokens,
which Gemini bills at the expensive output rate. Capping the thinking budget
(`ThinkingConfig(thinking_budget=512)`) cut the bill by two thirds without
hurting the itinerary.

| Version | Total billed tokens |
|---|---|
| First run (unlimited thinking) | 5,129 |
| Thinking capped at 512 | 1,719 |

The program also prints its own usage after every call: `count_tokens` before
sending, and `usage_metadata` (input / thinking / output) after.

## Self-Evaluation of the Output

- **Tier 1: rule checks (0 tokens)** — plain Python re-tests the hard
  constraints on the returned JSON: day count and numbering, activities per
  day, the 4.5 h driving cap, the 9 h daily load, packing-tip count, and that
  the trip really ends in the requested city.
- **Tier 2: LLM-as-judge (optional, one extra call)** — a second model reviews
  the itinerary for what code cannot check (real places, realistic driving,
  season fit) and sorts every finding into **critical** (trip-breaking),
  **warnings** (trip survives), or **suggestions** (improvements). Severity
  buckets proved far more useful than 1–5 scores, which were noisy and
  conflated "route impossible" with "museum is 45 minutes further than
  implied".

## Tech

Python, Google Gemini API (`google-genai`), Pydantic, python-dotenv

## Running

```bash
pip install google-genai pydantic python-dotenv
```

Create a `.env` file next to the script (never commit it):

```text
GEMINI_API_KEY=your_key_here
```

Then:

```bash
python W13Act2.py
```

## Future Work

A future version could make the model **self-check before returning**: feed
the judge's *critical* findings back to the generator for one automatic
revision pass (generate → evaluate → repair), so the itinerary the user sees
has already survived its own review.
