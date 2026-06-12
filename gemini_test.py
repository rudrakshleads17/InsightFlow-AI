from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

import google.generativeai as genai

# Put your NEW API key here
genai.configure(api_key="API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content(
    "Convert this question into SQL: Show all premium customers"
)

print(response.text)