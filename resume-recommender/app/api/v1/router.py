from fastapi import APIRouter
from app.api.v1.endpoints import search

# Main API router (versioned)
api_router = APIRouter()

# -----------------------------
# Include feature routers
# -----------------------------
api_router.include_router(
    search.router,
    prefix="/search",
    tags=["Search"]
)

# -----------------------------
# Health Check (optional)
# -----------------------------
@api_router.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}