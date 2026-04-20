from pymongo import MongoClient
from app.core.config import settings

# -----------------------------
# MongoDB Client (with pooling)
# -----------------------------
client = MongoClient(
    settings.MONGO_URI,
    maxPoolSize=50,       # max connections in pool
    minPoolSize=5,        # keep some connections ready
    serverSelectionTimeoutMS=5000  # fail fast if DB not reachable
)

# -----------------------------
# Database Reference
# -----------------------------
db = client[settings.DB_NAME]

# -----------------------------
# Health Check (optional)
# -----------------------------
def check_db_connection():
    try:
        client.admin.command("ping")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False