from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import sensor, dashboard

app = FastAPI(
    title       = "Pond Management API",
    description = "IoT-based Intelligent Pond Management System",
    version     = "1.0.0"
)

# ── CORS — Dashboard থেকে request আসবে ──
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],  # Production এ Netlify URL দেবে
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ── Routes ──
app.include_router(sensor.router,    prefix="/api", tags=["Sensor"])
app.include_router(dashboard.router, prefix="/api", tags=["Dashboard"])


@app.get("/")
async def root():
    return {
        "project" : "Pond Management System",
        "status"  : "running",
        "docs"    : "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "ok"}