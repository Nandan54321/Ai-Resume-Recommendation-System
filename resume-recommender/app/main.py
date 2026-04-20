# app/main.py

from fastapi import FastAPI
from app.api.v1.router import api_router
from app.db.seed import run_seed

app = FastAPI(
    title="AI Resume Recommender",
    description="Embedding-based retrieval + LLM scoring (OpenAI / Local)",
    version="1.0.0"
)

# -----------------------------
# Startup Event (Auto Seed)
# -----------------------------
@app.on_event("startup")
def startup_event():
    print("🚀 Starting application...")
    run_seed()
    print("✅ Startup complete")

# -----------------------------
# Root Endpoint (Health Check)
# -----------------------------
@app.get("/")
def root():
    return {"message": "AI Resume Recommender is running 🚀"}

# -----------------------------
# API Routes
# -----------------------------
app.include_router(api_router, prefix="/api/v1")