import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def get_gemini_response(prompt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        contents = prompt,
        model='gemini-1.5-flash',
    )

    return response