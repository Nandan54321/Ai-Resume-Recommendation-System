from app.services.embeddings import get_embedding
from app.repositories.candidate_repo import vector_search_candidates
from app.services.llm_service import analyze_candidate

def search_candidates(query: str):
    query_embedding = get_embedding(query)
    candidates = vector_search_candidates(query_embedding)

    results = []

    for c in candidates:
        llm_data = analyze_candidate(query, c["resume_text"])

        results.append({
            "name": c["name"],
            "title": c["title"],
            "skills": c["skills"],
            "vector_score": c["score"],
            **llm_data
        })

    return results