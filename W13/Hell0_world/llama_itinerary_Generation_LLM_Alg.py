'''
from together import Together
'''

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def instructor_chatbot():
    #client = Together(api_key="LLAMA API KEY")
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    """Command-line AI Itinerary Chatbot."""
    print("Welcome to AI Itinerary recommender! Answer a few questions to get personalized itenary advice.\n")
    
    days = input("How many (days): ")
    location = input("Where is the destination (city name): ")
    age = input("Enter your age: ")
    # fitness_goal = input("What is your fitness goal? (e.g., lose weight, build muscle, endurance, etc.): ")
    
    # Construct prompt
    prompt = f"""
    You are a professional trouist recommender. Provide an itinerary recommendation based on user data.
    
    User Details:
    - days: {days} days
    - destination: {location} city
    - Age: {age} years
    
    Based on your personal information, 
    Then, give a structured itinerary with a name of the place, address and short description for each day seperatly in order with maximom three activities in a day.
    """
    
    try:
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="You are a professional itinerary recommender.",
            temperature=0.8,
            #max_output_tokens=1000,
        ),
        )

        print("\n My Name is Chris as AI Itinerary expert:")
        print(response.text)


    except Exception as e:
        print("Error communicating :", e)

if __name__ == "__main__":
    instructor_chatbot()