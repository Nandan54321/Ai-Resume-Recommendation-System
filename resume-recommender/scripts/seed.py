"""
Manual database seeding script

Usage:
    python scripts/seed.py
    python scripts/seed.py 200   # seed 200 records
"""

import sys
from app.db.seed import run_seed


def main():
    try:
        # Default number of records
        num_records = 120

        # Allow override from CLI
        if len(sys.argv) > 1:
            num_records = int(sys.argv[1])

        print(f"🌱 Seeding {num_records} candidates...")
        run_seed(num_records)
        print("🎉 Seeding completed successfully!")

    except Exception as e:
        print(f"❌ Seeding failed: {e}")


if __name__ == "__main__":
    main()