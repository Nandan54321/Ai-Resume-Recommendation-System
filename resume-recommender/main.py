from fastapi import FastAPI
from services.retriever import retrieve_resumes
from services.scorer import score_candidate

app = FastAPI(title="AI Resume Recommendation API")


@app.get("/")
def home():
    return {"message": "API Running"}


@app.post("/recommend")
def recommend(job: dict):
    job_desc = job["description"]
    job_title = job.get("title", "Unknown Job")

    candidates = retrieve_resumes(job_desc)

    results = []

    for c in candidates:
        score = score_candidate(job_desc, c.get("resume_text", ""))

        results.append({
            "name": c.get("name"),
            "title": c.get("title"),
            **score
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {
        "job": job_title,
        "recommendations": results
    }
