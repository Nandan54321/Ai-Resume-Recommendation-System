from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# -----------------------------
# Base Candidate Model
# -----------------------------
class CandidateBase(BaseModel):
    name: str = Field(..., example="John Doe")
    title: str = Field(..., example="ML Engineer")
    skills: List[str] = Field(..., example=["Python", "NLP", "TensorFlow"])
    resume_text: str = Field(..., example="Experienced ML engineer with NLP projects")


# -----------------------------
# Candidate (Stored in DB)
# -----------------------------
class CandidateInDB(CandidateBase):
    embedding: List[float]
    created_at: datetime


# -----------------------------
# Candidate Response (API)
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
# Optional: Search Request Model
# -----------------------------
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, example="Looking for Python NLP engineer")


# -----------------------------
# Optional: Paginated Response
# -----------------------------
class PaginatedCandidates(BaseModel):
    total: int
    results: List[CandidateResponse]