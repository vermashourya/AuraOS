from google import genai

client = genai.Client(api_key="AIzaSyAYLKNaH_hRXvjesOfpwzocf9-rFM7exhM")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello, who are you?"
)

print(response.text)