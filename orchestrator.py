import json, pathlib
from agents.profiler import talent_intelligence_report
from agents.assessment import build_assessment_package
from agents.behavioral import analyze_text
from agents.market import analyze_market

BASE = pathlib.Path(__file__).parent
DATA = BASE / "data"
REPORTS = BASE / "reports"

def main():
    candidates = json.loads((DATA / "candidates.json").read_text())
    chats = json.loads((DATA / "chats.json").read_text())
    market = analyze_market(str(DATA / "market.csv"))

    for cand in candidates:
        tir = talent_intelligence_report(cand)
        assess = build_assessment_package(cand, cand["target_role"])
        beh = analyze_text(chats[cand["name"]])

        outdir = REPORTS / cand["name"].replace(" ", "_")
        outdir.mkdir(exist_ok=True)
        (outdir / "tir.json").write_text(json.dumps(tir, indent=2))
        (outdir / "assessment.json").write_text(json.dumps(assess, indent=2))
        (outdir / "behavior.json").write_text(json.dumps(beh, indent=2))
        (outdir / "market.json").write_text(json.dumps(market, indent=2))

if __name__ == "__main__":
    main()
