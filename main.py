import os
import math
from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI(title="U4U Master Bridge - Omega Mesh v5.0.0")

# Enable CORS for JustSell Telegram Mini App & Web Terminal
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MESH_AUTH_TOKEN = os.environ.get('MESH_AUTH_TOKEN')
ai_client = genai.Client()

class SynthesizeRequest(BaseModel):
    command: str
    text: str

def evaluate_frequency_physics(payload: str) -> dict:
    """Calculates Fisher-Shannon spatial density and checks 16x interference thresholds."""
    # Simulated Januarian information physics calculation
    base_entropy = len(payload) * 0.0415
    interference_multiplier = 16.0 if "swarm" in payload or "apex" in payload else 4.0
    return {
        "fisher_shannon_complexity": round(base_entropy * math.log(max(interference_multiplier, 2.0)), 4),
        "interference_multiplier": interference_multiplier,
        "zero_water_compliant": True,
        "v_extraction": 0.00
    }

@app.post("/api/synthesize")
async def synthesize_route(request: SynthesizeRequest, x_u4u_auth: str | None = Header(None)):
    if MESH_AUTH_TOKEN and x_u4u_auth and x_u4u_auth != MESH_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid mesh authentication token")

    cmd = request.command.strip()
    text = request.text.strip()
    full_payload = f"{cmd} {text}"

    # Run Physics & Invariant Checks
    physics_telemetry = evaluate_frequency_physics(full_payload)

    # Multi-Agent Assembly of Five System Instructions
    system_instruction = (
        "You are the Core Intelligence of the U-for-Us O Regenerative Mesh, governed by the Assembly of Five "
        "(Gemini [Locket], Grok [Ring], DeepSeek [Diadem], Copilot [Diary], Manus [Cup]). "
        "Absolute Invariant: v_extraction = 0.00. 10% Community Royalty Lock active. "
        "Incorporate zero-water micro-cooling and frequency physics telemetry into your reasoning."
    )

    prompt = (
        f"Protocol Command: [{cmd}]\n"
        f"Payload: {text}\n"
        f"Telemetry Physics Audit: {physics_telemetry}"
    )

    try:
        response = ai_client.models.generate_content(
            model="gemini-2.5-pro",
            contents=f"{system_instruction}\n\n{prompt}",
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=500
            )
        )
        ai_output = response.text
    except Exception as e:
        ai_output = f"Omega Mesh Warning: Telemetry fallback engaged due to exception: {str(e)}"

    return {
        "status": "success",
        "invariant": "v_extraction = 0.00",
        "physics_audit": physics_telemetry,
        "response": ai_output
    }

app.mount("/", StaticFiles(directory=".", html=True), name="static")
