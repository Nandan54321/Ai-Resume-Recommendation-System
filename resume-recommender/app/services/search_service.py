# from app.services.embeddings import get_embedding
# from app.repositories.candidate_repo import vector_search_candidates
# from app.services.llm_service import analyze_candidate

# def search_candidates(query: str):
#     query_embedding = get_embedding(query)
#     candidates = vector_search_candidates(query_embedding)

#     results = []

#     for c in candidates:
#         llm_data = analyze_candidate(query, c["resume_text"])

#         results.append({
#             "name": c["name"],
#             "title": c["title"],
#             "skills": c["skills"],
#             "vector_score": c["score"],
#             **llm_data
#         })

#     return results

from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.services.embeddings import get_embedding
from app.repositories.candidate_repo import vector_search_candidates
from app.services.llm_service import analyze_candidate


# -----------------------------
# LLM enrichment (single)
# -----------------------------
def enrich_candidate(query: str, candidate: Dict) -> Dict:
    """
    Adds LLM-based scoring + reasoning to a single candidate
    """
    try:
        llm_data = analyze_candidate(query, candidate["resume_text"])
    except Exception as e:
        llm_data = {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "reasoning": f"LLM failed: {str(e)}"
        }

    return {
        "name": candidate["name"],
        "title": candidate["title"],
        "skills": candidate["skills"],
        "vector_score": candidate.get("score", 0),
        **llm_data
    }


# -----------------------------
# Main Search Function
# -----------------------------
def search_candidates(query: str, top_k: int = 5) -> List[Dict]:
    """
    Full pipeline:
    Query → Embedding → Vector Search → LLM Scoring
    """

    # 1️⃣ Convert query → embedding
    query_embedding = get_embedding(query)

    # 2️⃣ Retrieve candidates from DB
    candidates = vector_search_candidates(query_embedding)

    if not candidates:
        return []

    # 3️⃣ Parallel LLM scoring (important for speed)
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(enrich_candidate, query, c)
            for c in candidates[:top_k]
        ]

        for future in as_completed(futures):
            results.append(future.result())

    # 4️⃣ Sort by LLM match score (final ranking)
    results.sort(key=lambda x: x.get("match_score", 0), reverse=True)

    return results