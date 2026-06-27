from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013R_R44_prompt_schema_adjustment_regeneration"


def main() -> None:
    errors: list[str] = []
    result = json.loads((OUT_DIR / "R44_result.json").read_text(encoding="utf-8"))
    comparison = result.get("quality_comparison", {})
    for path in [
        OUT_DIR / "R44_prompt_adjustment_plan.md",
        OUT_DIR / "R44_prompt_v1.md",
        OUT_DIR / "R44_prompt_v2.md",
        OUT_DIR / "R44_schema_adjustment_notes.md",
        OUT_DIR / "R44_quality_comparison.md",
    ]:
        if not path.exists() or not path.read_text(encoding="utf-8", errors="ignore").strip():
            errors.append(f"missing_or_empty:{path.name}")
    if "v1_score" not in comparison or "v2_score" not in comparison:
        errors.append("comparison_scores_missing")
    if "improved" not in comparison:
        errors.append("comparison_improved_missing")
    v2 = result.get("v2_candidate", {})
    if not v2.get("candidate_content"):
        errors.append("v2_candidate_content_missing")
    if v2.get("formal_apply_allowed") is not False:
        errors.append("v2_formal_apply_not_false")
    if v2.get("overwrite_original_allowed") is not False:
        errors.append("v2_overwrite_not_false")
    for flag in ["database_written", "feishu_written", "memory_written", "save_performed", "export_performed", "formal_apply_performed", "original_lesson_overwritten"]:
        if result.get("boundary", {}).get(flag):
            errors.append(f"boundary_broken:{flag}")
    if result.get("next_stage") != "R45_USER_REVIEW_MODEL_QUALITY_AND_NEXT_SCOPE":
        errors.append("next_stage_not_R45")
    if result.get("final_status") != "PASS_R44_PROMPT_SCHEMA_ADJUSTMENT_REGENERATION":
        errors.append("final_status_mismatch")
    if errors:
        raise SystemExit("FAIL: " + ", ".join(errors))
    print("PASS: 1013R_R44 prompt schema adjustment regeneration")


if __name__ == "__main__":
    main()
