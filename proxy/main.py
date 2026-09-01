from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os

app = FastAPI()

API_KEY = os.environ.get("GEMINI_API_KEY")

class Prompt(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "AuraOS proxy Running"}

@app.post("/gemini")
def ask_gemini(request: Prompt):
    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model = 'gemini-2.5-flash',
            contents=request.prompt
        )
        return {"text": response.text}
    except Exception as e:
        return {"error":str(e)}

