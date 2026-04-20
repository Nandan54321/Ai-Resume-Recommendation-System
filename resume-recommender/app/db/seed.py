from datetime import datetime
import random
from faker import Faker

from app.services.embeddings import get_embedding
from app.repositories.candidate_repo import (
    insert_candidates,
    is_candidates_collection_empty
)

fake = Faker()

# -----------------------------
# Skill & Job Pools
# -----------------------------
SKILLS_POOL = [
    "Python", "Machine Learning", "Deep Learning", "NLP",
    "FastAPI", "MongoDB", "Docker", "Kubernetes",
    "AWS", "SQL", "Data Analysis", "TensorFlow", "PyTorch"
]

JOB_TITLES = [
    "Data Scientist",
    "ML Engineer",
    "Backend Developer",
    "AI Engineer",
    "Data Analyst"
]


# -----------------------------
# Generate Single Candidate
# -----------------------------
def generate_candidate():
    skills = random.sample(SKILLS_POOL, k=random.randint(3, 6))

    name = fake.name()
    title = random.choice(JOB_TITLES)

    resume_text = (
        f"{name} is a {title} with experience in "
        f"{', '.join(skills)}. "
        f"Worked on multiple real-world projects involving "
        f"{random.choice(skills)}."
    )

    return {
        "name": name,
        "title": title,
        "skills": skills,
        "resume_text": resume_text,
        "embedding": get_embedding(resume_text),  # 🔥 AI part
        "created_at": datetime.utcnow()
    }


# -----------------------------
# Main Seed Function
# -----------------------------
def run_seed(num_records: int = 120):
    """
    Seed database with fake candidates
    """

    # Prevent duplicate seeding
    if not is_candidates_collection_empty():
        print("⚡ Database already seeded. Skipping...")
        return

    print("🌱 Seeding database...")

    candidates = [generate_candidate() for _ in range(num_records)]

    insert_candidates(candidates)

    print(f"✅ Seeded {num_records} candidates successfully!")