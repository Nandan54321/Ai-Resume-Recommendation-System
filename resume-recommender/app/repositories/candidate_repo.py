# from app.core.database import db

# def vector_search_candidates(query_embedding):
#     pipeline = [
#         {
#             "$vectorSearch": {
#                 "index": "resume_index",
#                 "path": "embedding",
#                 "queryVector": query_embedding,
#                 "numCandidates": 100,
#                 "limit": 5
#             }
#         },
#         {
#             "$project": {
#                 "_id": 0,
#                 "name": 1,
#                 "title": 1,
#                 "skills": 1,
#                 "resume_text": 1,
#                 "score": {"$meta": "vectorSearchScore"}
#             }
#         }
#     ]

#     return list(db.candidates.aggregate(pipeline))

from typing import List, Dict
from app.core.database import db


# -----------------------------
# Vector Search (MongoDB)
# -----------------------------
def vector_search_candidates(
    query_embedding: List[float],
    limit: int = 5,
    num_candidates: int = 100
) -> List[Dict]:
    """
    Perform vector similarity search using MongoDB Atlas ($vectorSearch)

    Args:
        query_embedding: embedding vector of the query
        limit: number of final results
        num_candidates: number of candidates to consider before ranking

    Returns:
        List of candidate documents
    """

    pipeline = [
        {
            "$vectorSearch": {
                "index": "resume_index",   # must match your MongoDB index name
                "path": "embedding",       # field storing embeddings
                "queryVector": query_embedding,
                "numCandidates": num_candidates,
                "limit": limit
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": 1,
                "title": 1,
                "skills": 1,
                "resume_text": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    return list(db.candidates.aggregate(pipeline))


# -----------------------------
# Insert Candidates (bulk)
# -----------------------------
def insert_candidates(candidates: List[Dict]):
    """
    Insert multiple candidate documents
    """
    if not candidates:
        return

    db.candidates.insert_many(candidates)


# -----------------------------
# Check if DB is seeded
# -----------------------------
def is_candidates_collection_empty() -> bool:
    return db.candidates.count_documents({}) == 0


# -----------------------------
# Clear Candidates (dev only)
# -----------------------------
def clear_candidates():
    """
    ⚠️ Use only in development
    """
    db.candidates.delete_many({})