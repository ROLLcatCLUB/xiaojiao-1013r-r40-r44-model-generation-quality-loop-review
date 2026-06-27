from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT_DIR = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / "1013R_R40_model_quality_sandbox_gate"


def main() -> None:
    errors: list[str] = []
    result = json.loads((OUT_DIR / "R40_result.json").read_text(encoding="utf-8"))
    gate = result.get("gate", {})
    expected = {
        "provider_call_allowed": True,
        "model_call_allowed": True,
        "sandbox_only": True,
        "formal_apply_allowed": False,
        "save_allowed": False,
        "export_allowed": False,
        "database_write_allowed": False,
        "feishu_write_allowed": False,
        "memory_write_allowed": False,
        "overwrite_original_allowed": False,
    }
    for key, value in expected.items():
        if gate.get(key) is not value:
            errors.append(f"gate_mismatch:{key}")
    if "api_key" not in result.get("model_call_log_schema", {}).get("forbidden", []):
        errors.append("model_call_log_schema_does_not_forbid_api_key")
    if result.get("boundary", {}).get("formal_apply_performed"):
        errors.append("formal_apply_performed")
    if result.get("final_status") != "PASS_R40_MODEL_QUALITY_SANDBOX_GATE":
        errors.append("final_status_mismatch")
    if errors:
        raise SystemExit("FAIL: " + ", ".join(errors))
    print("PASS: 1013R_R40 model quality sandbox gate")


if __name__ == "__main__":
    main()
