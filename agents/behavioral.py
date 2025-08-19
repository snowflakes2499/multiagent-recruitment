# agents/behavioral.py
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# --- Expanded keyword dictionaries ---
TEAMWORK_KEYWORDS = [
    "team", "collaborated", "collaboration", "together", "helped", "supported",
    "worked with", "others", "colleagues", "cross-functional", "partnered"
]

PROBLEM_SOLVING_KEYWORDS = [
    "solved", "fixed", "resolved", "debugged", "optimized", "improved",
    "reduced", "streamlined", "analyzed", "designed", "developed",
    "implemented", "ownership", "innovated"
]

COMMUNICATION_KEYWORDS = [
    "documented", "presented", "explained", "communicated", "shared",
    "reported", "wrote", "summarized", "clarified"
]

ACHIEVEMENT_KEYWORDS = [
    "increased", "reduced", "improved", "saved", "achieved", "boosted",
    "delivered", "successfully", "%", "faster", "slower", "more efficient"
]


def analyze_text(text: str) -> dict:
    try:
        # --- Sentiment analysis ---
        sentiment = analyzer.polarity_scores(text)

        # Heuristic adjustment: boost if achievement words present
        if sentiment["compound"] < 0.2:  # mostly neutral
            if any(word in text.lower() for word in ACHIEVEMENT_KEYWORDS):
                sentiment["compound"] += 0.3
                sentiment["pos"] += 0.2
                sentiment["neu"] -= 0.2 if sentiment["neu"] >= 0.2 else 0

        # --- Observed traits detection ---
        observed_traits = {
            "teamwork": any(re.search(rf"\b{kw}\b", text, re.I) for kw in TEAMWORK_KEYWORDS),
            "problem_solving": any(re.search(rf"\b{kw}\b", text, re.I) for kw in PROBLEM_SOLVING_KEYWORDS),
            "communication": any(re.search(rf"\b{kw}\b", text, re.I) for kw in COMMUNICATION_KEYWORDS),
        }

        # --- Collect evidence (which keywords matched) ---
        evidence = {}
        for trait, keywords in {
            "teamwork": TEAMWORK_KEYWORDS,
            "problem_solving": PROBLEM_SOLVING_KEYWORDS,
            "communication": COMMUNICATION_KEYWORDS,
        }.items():
            hits = [kw for kw in keywords if re.search(rf"\b{kw}\b", text, re.I)]
            if hits:
                evidence[trait] = hits

        # --- Insights ---
        insights = []
        if observed_traits["teamwork"]:
            insights.append("Candidate demonstrates teamwork and collaboration.")
        if observed_traits["problem_solving"]:
            insights.append("Shows strong problem-solving and ownership skills.")
        if observed_traits["communication"]:
            insights.append("Communication skills evident (documentation, sharing, presenting).")
        if not insights:
            insights.append("No strong behavioral signals detected.")

        # --- Bias mitigation ---
        bias_protocol = [
            "Do not infer or judge based on name, gender, age, or background.",
            "Focus only on behavioral evidence (teamwork, communication, problem-solving).",
            "If unsure, mark as 'Not Observed' rather than making assumptions."
        ]

        return {
            "sentiment": sentiment,
            "observed_traits": observed_traits,
            "insights": insights,
            "evidence": evidence,
            "bias_protocol": bias_protocol
        }

    except Exception as e:
        return {"error": str(e)}
