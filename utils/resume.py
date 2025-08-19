# utils/resume.py
from PyPDF2 import PdfReader
import re

def parse_resume(file) -> dict:
    try:
        pdf = PdfReader(file)
        text = " ".join([page.extract_text() or "" for page in pdf.pages])

        # crude name extraction (first line or bold pattern)
        name_match = re.search(r"([A-Z][a-z]+ [A-Z][a-z]+)", text)
        name = name_match.group(1) if name_match else "Unknown Candidate"

        # crude role inference
        role_match = re.search(r"(Engineer|Developer|Analyst|Manager)", text)
        target_role = role_match.group(1) + " Candidate" if role_match else "Candidate from Resume"

        # extract skills keywords
        skills = {}
        keywords = ["python", "java", "c++", "javascript", "sql",
                    "django", "flask", "react", "angular",
                    "docker", "postgres", "mysql"]
        for kw in keywords:
            if re.search(kw, text, re.IGNORECASE):
                skills[kw] = {"confidence": 0.8, "category": "programming" if kw in ["python", "java", "c++", "javascript", "sql"] else "framework"}

        # simple summary bullets
        summary = []
        if "Experience" in text:
            summary.append("Has professional or internship experience.")
        if "Project" in text:
            summary.append("Has worked on projects during studies or career.")
        if "Hackathon" in text or "Winner" in text:
            summary.append("Achieved recognition in competitions or hackathons.")

        return {
            "name": name,
            "target_role": target_role,
            "career_summary": summary,
            "career_progression": [],  # can expand later
            "skills": skills,
            "profile": {"resume_text": text}
        }
    except Exception as e:
        return {"error": str(e)}
