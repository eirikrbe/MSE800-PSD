
#main.py

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model='gemini-2.5-flash', contents='Hello, world! Please write a short poem about the beauty of nature.'
)
print(type(response))
print()
print()
print(dir(response))
print()
print()
print(response)
print()
print()
print(response.text)
print()
print()
print(type(response.usage_metadata))
print()
print()
print(type(response.candidates))
print()
print()
print(type(response.text))
