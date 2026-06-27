from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013R_R42_multi_candidate_type_generation"


def main() -> None:
    errors: list[str] = []
    result = json.loads((OUT_DIR / "R42_result.json").read_text(encoding="utf-8"))
    state = json.loads((OUT_DIR / "R42_multi_candidate_generation_state.json").read_text(encoding="utf-8"))
    html = (OUT_DIR / "R42_multi_candidate_preview.html").read_text(encoding="utf-8", errors="ignore")
    candidates = state.get("candidates", [])
    if len(candidates) != 5:
        errors.append("candidate_count_not_5")
    types = {item.get("candidate_type") for item in candidates}
    for needed in ["teaching_process_cleanup", "courseware_script_candidate", "classroom_display_candidate", "worksheet_candidate", "assessment_rubric_candidate"]:
        if needed not in types:
            errors.append(f"candidate_type_missing:{needed}")
    generated_or_fallback = [item for item in candidates if item.get("status") in {"generated", "fallback"}]
    if len(generated_or_fallback) < 3:
        errors.append("less_than_3_generated_or_fallback")
    for item in candidates:
        if item.get("teacher_confirmation_required") is not True:
            errors.append(f"teacher_confirmation_missing:{item.get('candidate_type')}")
        if item.get("formal_apply_allowed") is not False:
            errors.append(f"formal_apply_not_false:{item.get('candidate_type')}")
    if "data-formal-apply-allowed=\"false\"" not in html:
        errors.append("preview_html_formal_apply_marker_missing")
    for flag in ["database_written", "feishu_written", "memory_written", "save_performed", "export_performed", "formal_apply_performed"]:
        if result.get("boundary", {}).get(flag):
            errors.append(f"boundary_broken:{flag}")
    if result.get("final_status") != "PASS_R42_MULTI_CANDIDATE_TYPE_GENERATION":
        errors.append("final_status_mismatch")
    if errors:
        raise SystemExit("FAIL: " + ", ".join(errors))
    print("PASS: 1013R_R42 multi candidate type generation")


if __name__ == "__main__":
    main()
