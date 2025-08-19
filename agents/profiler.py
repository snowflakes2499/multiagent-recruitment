import re
from utils.db import get_candidate_by_name

# ======================================================
# SKILL DEFINITIONS
# ======================================================

VALID_SKILLS = {
    "python": "programming",
    "sql": "programming",
    "node.js": "framework",
    "react": "framework",
    "django": "framework",
    "flask": "framework",
    "fastapi": "framework",
    "docker": "infrastructure",
    "kubernetes": "infrastructure",
    "airflow": "infrastructure",
    "ci/cd": "infrastructure",
    "postgres": "database",
    "mysql": "database",
    "mongodb": "database",
    "nlp": "ml",
    "ml": "ml",
    "machine learning": "ml"
}

STOPWORDS = {
    "of", "on", "for", "the", "a", "an", "and",
    "apps", "backend", "performance", "critical",
    "built", "pipelines", "containerized", "with",
    "using", "developed", "engineer", "developer"
}

# ======================================================
# HELPER FUNCTIONS
# ======================================================

def normalize_text(text: str) -> str:
    """Lowercase + strip punctuation"""
    return re.sub(r"[^a-z0-9+.#/]", " ", text.lower()).strip()

def extract_skills(candidate: dict) -> dict:
    """Parse LinkedIn + GitHub → structured skill map with filtering"""
    skill_map = {}

    # 1. from LinkedIn work history
    for job in candidate.get("linkedin", {}).get("work_history", []):
        for bullet in job.get("bullets", []):
            tokens = normalize_text(bullet).split()
            joined = " ".join(tokens)

            # detect "ci cd"
            if "ci cd" in joined:
                skill_map.setdefault("ci/cd", 0.6)
                skill_map["ci/cd"] += 0.1

            for token in tokens:
                if token in STOPWORDS:
                    continue
                if token in VALID_SKILLS:
                    skill_map.setdefault(token, 0.5)
                    skill_map[token] += 0.2

    # 2. from GitHub repos
    for repo in candidate.get("github", {}).get("repos", []):
        for topic in repo.get("topics", []):
            token = normalize_text(topic)
            if token in VALID_SKILLS:
                skill_map.setdefault(token, 0.6)
                skill_map[token] += 0.1
        if repo.get("stars", 0) >= 10:
            for topic in repo.get("topics", []):
                token = normalize_text(topic)
                if token in VALID_SKILLS:
                    skill_map[token] = min(skill_map.get(token, 0.6) + 0.2, 0.95)

    # 3. build structured output
    return {
        skill: {
            "confidence": round(min(score, 0.95), 2),
            "category": VALID_SKILLS[skill]
        }
        for skill, score in skill_map.items()
    }

def career_progression(candidate: dict):
    """Build structured career history timeline"""
    history = candidate.get("linkedin", {}).get("work_history", [])
    progression = []
    for job in history:
        progression.append({
            "period": f"{job.get('start','?')} → {job.get('end','?')}",
            "title": job.get("title", ""),
            "company": job.get("company", "")
        })
    return progression

# ======================================================
# MAIN AGENT FUNCTION
# ======================================================

def talent_intelligence_report(name: str) -> dict:
    """Return structured Talent Intelligence Report for a candidate"""
    record = get_candidate_by_name(name)
    if not record:
        return {"error": f"Candidate {name} not found in DB."}

    candidate = record["profile"]

    # run analysis
    skills = extract_skills(candidate)
    progression = career_progression(candidate)

    # build career summary text
    summary = []
    if progression:
        summary.append(f"{record['name']} has worked in {len(progression)} role(s).")
        summary.append(f"Most recent role: {progression[-1]['title']} at {progression[-1]['company']}.")
    if skills:
        summary.append("Key strengths: " + ", ".join(list(skills.keys())[:5]))

    return {
        "name": record["name"],
        "target_role": record["headline"].split(" at ")[0],
        "career_summary": summary,
        "career_progression": progression,
        "skills": skills
    }
