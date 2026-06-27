from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013R_R43_generation_quality_evaluation"


def main() -> None:
    errors: list[str] = []
    result = json.loads((OUT_DIR / "R43_result.json").read_text(encoding="utf-8"))
    rubric = json.loads((OUT_DIR / "R43_quality_rubric.json").read_text(encoding="utf-8"))
    evaluations = result.get("evaluation_result", [])
    if len(evaluations) != 5:
        errors.append("evaluation_count_not_5")
    if rubric.get("basic_pass_line") != 24:
        errors.append("pass_line_not_24")
    for item in evaluations:
        if item.get("status") == "blocked":
            if not item.get("blocked_reason"):
                errors.append(f"blocked_reason_missing:{item.get('candidate_type')}")
            continue
        scores = item.get("scores", {})
        for key in rubric.get("dimensions", []):
            if key not in scores:
                errors.append(f"score_missing:{item.get('candidate_type')}:{key}")
        if item.get("scores", {}).get("hallucination_risk", 0) >= 4 and item.get("basic_quality_pass"):
            errors.append(f"high_hallucination_passed:{item.get('candidate_type')}")
        if item.get("scores", {}).get("source_alignment", 0) <= 2 and item.get("basic_quality_pass"):
            errors.append(f"low_source_alignment_passed:{item.get('candidate_type')}")
    if not result.get("human_review_focus"):
        errors.append("human_review_focus_missing")
    if result.get("final_status") != "PASS_R43_GENERATION_QUALITY_EVALUATION":
        errors.append("final_status_mismatch")
    if errors:
        raise SystemExit("FAIL: " + ", ".join(errors))
    print("PASS: 1013R_R43 generation quality evaluation")


if __name__ == "__main__":
    main()
