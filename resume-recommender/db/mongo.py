from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["resume_db"]

resumes_collection = db["resumes"]
jobs_collection = db["jobs"]