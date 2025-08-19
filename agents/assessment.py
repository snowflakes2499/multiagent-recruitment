# agents/assessment.py
import random
from utils.db import get_candidate_by_name

def build_assessment_package(candidate_name: str, target_role: str = ""):
    """
    Generate a role-specific assessment package for a candidate.
    Includes tasks, rubric, and bias mitigation protocol.
    """
    record = get_candidate_by_name(candidate_name)
    profile = record.get("profile", {}) if record else {}

    # --- Role extraction (clean without company name) ---
    if target_role:
        role = target_role
    else:
        headline = record.get("headline", "")
        role = headline.split(" at ")[0] if " at " in headline else headline

    # --- Experience level (rough heuristic) ---
    level = "junior"
    if "senior" in role.lower() or "lead" in role.lower():
        level = "senior"
    elif "intern" in role.lower() or "junior" in role.lower():
        level = "junior"
    else:
        level = "mid"

    # --- Extract top skills (fallback heuristics) ---
    skills = []
    if "skills" in profile:
        skills = sorted(profile["skills"].keys(), key=lambda x: profile["skills"][x]["confidence"], reverse=True)[:5]
    else:
        skills = ["python", "sql", "docker"]

    # --- Example tasks ---
    tasks = [
        f"Write a function or small script (30-60 min) that solves a common problem relevant to {role}. Use {', '.join(skills[:3])} where appropriate.",
        "Fix a small bug: given a failing unit test, identify the issue and provide a corrected implementation and tests.",
        f"Explain, in 300 words, the trade-offs between two simple approaches to a typical problem for {role}."
    ]

    # --- Rubric ---
    rubric = {
        "Problem Solving": 0.4,
        "Code Quality": 0.3,
        "Communication": 0.3
    }

    # --- Bias mitigation protocol ---
    bias_protocol = [
        "Ignore name, gender, age, ethnicity, and educational institution.",
        "Evaluate only on observable outputs (code, design diagrams, answers).",
        "Use the provided rubric; require a short rationale for each score to aid auditability.",
        "Normalize scores when comparing across multiple assessors."
    ]

    return {
        "role": role,   # ✅ now clean (no 'at Company')
        "level": level,
        "tasks": tasks,
        "rubric": rubric,
        "bias_protocol": bias_protocol,
        "notes": f"Deterministic fallback assessment generated for level='{level}'. "
                 f"Top inferred skills: {skills} (heuristic fallback used)"
    }
