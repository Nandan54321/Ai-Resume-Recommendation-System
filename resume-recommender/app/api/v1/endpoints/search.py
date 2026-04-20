
# from fastapi import APIRouter
# from app.services.search_service import search_candidates

# router = APIRouter()

# @router.post("/")
# def search(query: str):
#     return search_candidates(query)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from app.services.search_service import search_candidates

router = APIRouter()


# -----------------------------
# Request Model
# -----------------------------
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, example="Looking for Python NLP engineer")


# -----------------------------
# Response Model
# -----------------------------
class CandidateResponse(BaseModel):
    name: str
    title: str
    skills: List[str]
    vector_score: float
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    reasoning: str


# -----------------------------
# Search Endpoint
# -----------------------------
@router.post("/", response_model=List[CandidateResponse])
def search(request: SearchRequest):
    try:
        results = search_candidates(request.query)

        if not results:
            return []

        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )