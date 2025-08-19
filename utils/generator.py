# utils/generator.py
import random
from faker import Faker
from typing import Dict, Any, List
from utils.db import init_db, add_candidate, bulk_insert_candidates

fake = Faker()
SKILLS = ["Python", "Django", "Flask", "FastAPI", "SQL", "Postgres", "MySQL",
          "Docker", "Kubernetes", "React", "Node.js", "NLP", "Pandas", "TensorFlow",
          "PyTorch", "Redis", "Airflow", "AWS", "GCP"]

ROLES = ["Backend Engineer", "Machine Learning Engineer", "Data Scientist", "Frontend Engineer", "DevOps Engineer"]

def generate_one() -> Dict[str, Any]:
    name = fake.name()
    role = random.choice(ROLES)
    headline = f"{role} at {fake.company()}"
    # Build work history 1-4 entries
    history = []
    num_jobs = random.randint(1, 3)
    year = random.randint(2016, 2022)
    for _ in range(num_jobs):
        start_year = year
        end_year = start_year + random.randint(0, 2)
        bullets = [
            f"Worked on {random.choice(SKILLS)} for backend services",
            f"Improved performance of critical services using {random.choice(SKILLS)}",
            f"Built CI/CD pipelines and containerized apps with Docker"
        ]
        history.append({
            "title": random.choice(["Junior Developer", "Software Engineer", "Senior Engineer", "Lead Engineer"]),
            "company": fake.company(),
            "start": f"{start_year}-01",
            "end": f"{end_year}-12",
            "bullets": random.sample(bullets, k=2)
        })
        year = end_year + 1
    repos = []
    for _ in range(random.randint(1, 3)):
        topics = random.sample(SKILLS, k=2)
        repos.append({
            "name": fake.word() + "-repo",
            "stars": random.randint(0, 80),
            "topics": topics
        })
    profile = {
        "linkedin": {
            "headline": headline,
            "work_history": history
        },
        "github": {
            "repos": repos
        }
    }
    return {"name": name, "headline": headline, "profile": profile}

def bulk_generate(n: int = 100) -> int:
    init_db()
    batch = [generate_one() for _ in range(n)]
    count = bulk_insert_candidates(batch)
    return count

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", type=int, default=100, help="Number of synthetic candidates to generate")
    args = parser.parse_args()
    print(f"Generating {args.num} synthetic candidates into DB...")
    inserted = bulk_generate(args.num)
    print(f"Inserted {inserted} candidates.")
