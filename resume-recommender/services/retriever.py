from db.mongo import resumes_collection
from services.embeddings import get_embedding


def retrieve_resumes(job_desc: str, top_k: int = 5):
    job_embedding = get_embedding(job_desc)

    pipeline = [
        {
            "$vectorSearch": {
                "index": "resume_index",
                "path": "embedding",
                "queryVector": job_embedding,
                "numCandidates": 100,
                "limit": top_k
            }
        }
    ]

    results = list(resumes_collection.aggregate(pipeline))
    return results
