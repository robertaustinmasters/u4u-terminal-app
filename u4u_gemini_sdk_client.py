import os
from google import genai
from pydantic import BaseModel

# Initialize client using environment variable
client = genai.Client()

print("[+] U-for-Us Gemini SDK Client Initialized Successfully.")
response = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents="Verify system invariants: v_extraction = 0.00. Confirm status.",
)
print("Gemini Response:", response.text)
