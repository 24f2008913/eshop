from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import json
from fastapi import Request


# Load telemetry JSON from project root
try:
    with open("telemetry.json") as f:
        raw_data = json.load(f)
except FileNotFoundError:
    # fallback to an empty list so the service still starts during local tests
    raw_data = []

df = pd.DataFrame(raw_data)

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class LatencyRequest(BaseModel):
    regions: list[str]
    threshold_ms: float

@app.post("/")
@app.post("/api/latency")
def latency_metrics(req: LatencyRequest):
    result = {}
    for region in req.regions:
        region_data = df[df['region'] == region]
        avg_latency = region_data['latency_ms'].mean()
        p95_latency = np.percentile(region_data['latency_ms'], 95)
        avg_uptime = region_data['uptime_pct'].mean()
        breaches = (region_data['latency_ms'] > req.threshold_ms).sum()
        result[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": int(breaches)
        }
    return result


@app.get("/health")
@app.get("/api/latency/health")
def health():
    return {"ok": True}


@app.post("/{full_path:path}")
async def catch_all(full_path: str, request: Request):
    """Catch-all POST handler: try to parse the incoming JSON as LatencyRequest and forward to latency_metrics."""
    try:
        body = await request.json()
    except Exception:
        return {"detail": "invalid json body"}

    # If this looks like the latency request, forward to the handler
    if isinstance(body, dict) and 'regions' in body and 'threshold_ms' in body:
        try:
            req = LatencyRequest(**body)
        except Exception as e:
            return {"detail": f"invalid payload: {e}"}
        return latency_metrics(req)

    return {"detail": "not found"}
