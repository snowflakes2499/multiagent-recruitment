# agents/market.py
import requests

# --- Static fallback dataset with India-specific salaries (LPA) ---
# Each role now has bands for Fresher, Mid, Senior
STATIC_MARKET_DATA = {
    "Machine Learning Engineer": {
        "Role": "Machine Learning Engineer",
        "SalaryBands": {"Fresher": 6, "Mid": 18, "Senior": 35},
        "HotSkills": ["Python", "TensorFlow", "NLP", "Docker"],
        "BestChannels": ["LinkedIn", "GitHub", "Kaggle"],
        "Source": "static-fallback"
    },
    "Frontend Engineer": {
        "Role": "Frontend Engineer",
        "SalaryBands": {"Fresher": 4.5, "Mid": 14, "Senior": 28},
        "HotSkills": ["JavaScript", "React", "CSS", "TypeScript"],
        "BestChannels": ["GitHub", "LinkedIn", "StackOverflow"],
        "Source": "static-fallback"
    },
    "Backend Engineer": {
        "Role": "Backend Engineer",
        "SalaryBands": {"Fresher": 5, "Mid": 15, "Senior": 30},
        "HotSkills": ["Python", "Django", "SQL", "Docker"],
        "BestChannels": ["GitHub", "Reddit", "LinkedIn"],
        "Source": "static-fallback"
    },
    "Cloud Engineer": {
        "Role": "Cloud Engineer",
        "SalaryBands": {"Fresher": 6, "Mid": 16, "Senior": 32},
        "HotSkills": ["AWS", "Azure", "GCP", "Terraform"],
        "BestChannels": ["LinkedIn", "Medium", "Reddit"],
        "Source": "static-fallback"
    },
    "Data Scientist": {
        "Role": "Data Scientist",
        "SalaryBands": {"Fresher": 6.5, "Mid": 19, "Senior": 36},
        "HotSkills": ["Python", "Pandas", "Scikit-learn", "Deep Learning"],
        "BestChannels": ["Kaggle", "LinkedIn", "GitHub"],
        "Source": "static-fallback"
    },
    "DevOps Engineer": {
        "Role": "DevOps Engineer",
        "SalaryBands": {"Fresher": 5.5, "Mid": 17, "Senior": 33},
        "HotSkills": ["CI/CD", "Docker", "Kubernetes", "Linux"],
        "BestChannels": ["Reddit", "GitHub", "LinkedIn"],
        "Source": "static-fallback"
    },
    "Security Engineer": {
        "Role": "Security Engineer",
        "SalaryBands": {"Fresher": 6, "Mid": 18, "Senior": 34},
        "HotSkills": ["Penetration Testing", "Network Security", "SIEM", "Python"],
        "BestChannels": ["LinkedIn", "Reddit", "Security Forums"],
        "Source": "static-fallback"
    },
    "Full Stack Engineer": {
        "Role": "Full Stack Engineer",
        "SalaryBands": {"Fresher": 5, "Mid": 16, "Senior": 31},
        "HotSkills": ["JavaScript", "React", "Node.js", "SQL"],
        "BestChannels": ["GitHub", "LinkedIn", "StackOverflow"],
        "Source": "static-fallback"
    },
    "Product Manager": {
        "Role": "Product Manager",
        "SalaryBands": {"Fresher": 7, "Mid": 20, "Senior": 40},
        "HotSkills": ["Roadmapping", "Agile", "Stakeholder Management"],
        "BestChannels": ["LinkedIn", "Medium", "Product Hunt"],
        "Source": "static-fallback"
    },
    "AI Researcher": {
        "Role": "AI Researcher",
        "SalaryBands": {"Fresher": 8, "Mid": 22, "Senior": 45},
        "HotSkills": ["Deep Learning", "NLP", "PyTorch", "Research"],
        "BestChannels": ["Arxiv", "LinkedIn", "GitHub"],
        "Source": "static-fallback"
    },
}

def fetch_api_roles():
    """Try to fetch roles dynamically from Jobicy API."""
    try:
        resp = requests.get("https://jobicy.com/api/v2/remote-jobs", timeout=10)
        resp.raise_for_status()
        jobs = resp.json().get("jobs", [])
        roles = [j.get("jobTitle") for j in jobs if j.get("jobTitle")]
        return list(set(roles))
    except Exception:
        return []

def get_all_roles():
    """Return merged list of static + API roles."""
    api_roles = fetch_api_roles()
    merged = set(STATIC_MARKET_DATA.keys())
    merged.update(api_roles)
    return sorted(list(merged))

def analyze_market(role: str):
    """Return market intelligence for given role (static if available, else API)."""
    # 1. Check static dataset first
    if role in STATIC_MARKET_DATA:
        return STATIC_MARKET_DATA[role]

    # 2. Try API
    try:
        resp = requests.get(f"https://jobicy.com/api/v2/remote-jobs?search={role}", timeout=10)
        resp.raise_for_status()
        jobs = resp.json().get("jobs", [])
        if jobs:
            return {
                "Role": role,
                "SalaryBands": {"Fresher": 4, "Mid": 12, "Senior": 25},  # generic estimate
                "HotSkills": ["Remote", "Async", "Collaboration"],
                "BestChannels": ["LinkedIn", "Jobicy"],
                "Source": "jobicy-api"
            }
    except Exception:
        pass

    # 3. Fallback: minimal info
    return {
        "Role": role,
        "SalaryBands": {},
        "HotSkills": [],
        "BestChannels": [],
        "Source": "unknown"
    }
