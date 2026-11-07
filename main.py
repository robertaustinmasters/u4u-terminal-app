from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="U4U Master Bridge")

import os
MESH_AUTH_TOKEN = os.environ.get('MESH_AUTH_TOKEN')

class SynthesizeRequest(BaseModel):
    command: str
    text: str

@app.post("/api/synthesize")
async def synthesize_route(request: SynthesizeRequest, x_u4u_auth: str | None = Header(None)):
    if MESH_AUTH_TOKEN and x_u4u_auth and x_u4u_auth != MESH_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid mesh authentication token")
        
    cmd = request.command.strip()
    text = request.text.strip()
    
    output_message = f"Master Bridge executed protocol [{cmd}] successfully. Payload: {text}"
    
    return {
        "status": "success",
        "response": output_message
    }

# Serve static frontend files from the same directory
app.mount("/", StaticFiles(directory=".", html=True), name="static")

