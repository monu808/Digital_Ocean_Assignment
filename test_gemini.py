"""Quick test for Gemini API"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key found: {api_key[:20]}...")

genai.configure(api_key=api_key)

# Test with correct model name
model = genai.GenerativeModel('gemini-1.5-flash')
print(f"Model initialized: gemini-1.5-flash")

response = model.generate_content("Say hello!")
print(f"Response: {response.text}")
print("\n✅ Gemini API working correctly!")
