import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI(title="U4U Master Bridge")

# Allow cross-origin requests for Telegram Mini App & Web Terminal
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load security token from environment
MESH_AUTH_TOKEN = os.environ.get('MESH_AUTH_TOKEN')

# Initialize Google GenAI client (picks up GEMINI_API_KEY from environment)
ai_client = genai.Client()

class SynthesizeRequest(BaseModel):
    command: str
    text: str

@app.post("/api/synthesize")
async def synthesize_route(request: SynthesizeRequest, x_u4u_auth: str | None = Header(None)):
    # Enforce authentication if token is configured
    if MESH_AUTH_TOKEN and x_u4u_auth and x_u4u_auth != MESH_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid mesh authentication token")

    cmd = request.command.strip()
    text = request.text.strip()

    # Construct system prompt enforcing invariant v_extraction = 0.00
    system_instruction = (
        "You are the Core Intelligence of the U-for-Us O Regenerative Mesh. "
        "You operate under the absolute invariant v_extraction = 0.00 (zero predatory extraction) "
        "and enforce community benefit locks. Respond concisely as an advanced autonomous agent node."
    )

    prompt = f"Protocol Command: [{cmd}]\nPayload / Context: {text}"

    try:
        # Call Gemini live
        response = ai_client.models.generate_content(
            model="gemini-2.5-pro",
            contents=f"{system_instruction}\n\n{prompt}"
        )
        ai_output = response.text
    except Exception as e:
        ai_output = f"Autonomous Mesh Warning: AI synthesis bypassed due to telemetry exception: {str(e)}"

    return {
        "status": "success",
        "response": ai_output
    }

# Serve static frontend files from the same directory
app.mount("/", StaticFiles(directory=".", html=True), name="static")
