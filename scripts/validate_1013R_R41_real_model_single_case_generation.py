from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013R_R41_real_model_single_case_generation"


def _contains_secret_text(text: str) -> bool:
    lowered = text.lower()
    return "bearer " in lowered or "sk-" in lowered or "api_key=" in lowered


def main() -> None:
    errors: list[str] = []
    result = json.loads((OUT_DIR / "R41_result.json").read_text(encoding="utf-8"))
    candidate = json.loads((OUT_DIR / "R41_single_case_candidate.json").read_text(encoding="utf-8"))
    log = json.loads((OUT_DIR / "R41_model_call_log.json").read_text(encoding="utf-8"))
    for key in ["candidate_id", "before_text", "after_text", "xiaojiao_suggestion", "risk_notes"]:
        if not candidate.get(key):
            errors.append(f"candidate_field_missing:{key}")
    if candidate.get("sandbox_only") is not True:
        errors.append("sandbox_only_not_true")
    if candidate.get("formal_apply_allowed") is not False:
        errors.append("formal_apply_not_false")
    if candidate.get("overwrite_original_allowed") is not False:
        errors.append("overwrite_original_not_false")
    if log.get("provider_called") and not log.get("model_called"):
        errors.append("provider_called_without_model_called")
    if not log.get("prompt_hash"):
        errors.append("prompt_hash_missing")
    combined = json.dumps(result, ensure_ascii=False) + json.dumps(log, ensure_ascii=False)
    if _contains_secret_text(combined):
        errors.append("secret_like_text_in_logs")
    for flag in ["database_written", "feishu_written", "memory_written", "save_performed", "export_performed", "formal_apply_performed", "original_lesson_overwritten"]:
        if result.get("boundary", {}).get(flag):
            errors.append(f"boundary_broken:{flag}")
    if not str(result.get("final_status", "")).startswith("PASS_R41_REAL_MODEL_SINGLE_CASE_GENERATION"):
        errors.append("final_status_mismatch")
    if errors:
        raise SystemExit("FAIL: " + ", ".join(errors))
    print("PASS: 1013R_R41 real model single case generation")


if __name__ == "__main__":
    main()
