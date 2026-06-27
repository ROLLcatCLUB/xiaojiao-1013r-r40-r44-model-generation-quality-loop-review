from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT_ROOT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
R40_DIR = OUT_ROOT / "1013R_R40_model_quality_sandbox_gate"
R41_DIR = OUT_ROOT / "1013R_R41_real_model_single_case_generation"
R42_DIR = OUT_ROOT / "1013R_R42_multi_candidate_type_generation"
R43_DIR = OUT_ROOT / "1013R_R43_generation_quality_evaluation"
R44_DIR = OUT_ROOT / "1013R_R44_prompt_schema_adjustment_regeneration"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def report_header(stage: str, status: str) -> str:
    return f"""# {stage}

```text
stage_id={stage}
status={status}
generated_at={now()}
sandbox_only=true
formal_apply_allowed=false
save_performed=false
export_performed=false
archive_performed=false
database_written=false
feishu_written=false
memory_written=false
overwrite_original_allowed=false
```
"""


def r40_gate_md(r40: dict[str, Any]) -> str:
    gate = r40["gate"]
    return (
        report_header(r40["stage"], r40["final_status"])
        + f"""
## Gate

- provider_call_allowed={str(gate['provider_call_allowed']).lower()}
- model_call_allowed={str(gate['model_call_allowed']).lower()}
- sandbox_only={str(gate['sandbox_only']).lower()}
- formal_apply_allowed=false
- save_allowed=false
- export_allowed=false
- database_write_allowed=false
- feishu_write_allowed=false
- memory_write_allowed=false
- overwrite_original_allowed=false

API key 只从环境读取，不写入仓库。模型调用日志只保存 prompt_hash、状态、耗时和脱敏 provider_meta。
"""
    )


def r41_report_md(r41: dict[str, Any]) -> str:
    log = r41["model_call_log"]
    return (
        report_header(r41["stage"], r41["final_status"])
        + f"""
## Model Call

- provider_called={str(log.get('provider_called')).lower()}
- model_called={str(log.get('model_called')).lower()}
- status={log.get('status')}
- reason_code={log.get('reason_code', '')}
- latency_ms={log.get('latency_ms')}
- prompt_hash={log.get('prompt_hash')}

候选只进入 sandbox preview，不覆盖原教案。
"""
    )


def r42_report_md(r42: dict[str, Any]) -> str:
    lines = [report_header(r42["stage"], r42["final_status"]), "## Candidates", ""]
    for item in r42["candidates"]:
        lines.append(f"- {item['candidate_type']}: {item['status']} / {item['source']}")
    return "\n".join(lines) + "\n"


def r43_review_md(r43: dict[str, Any]) -> str:
    lines = [report_header(r43["stage"], r43["final_status"]), "## Quality Evaluation", ""]
    for item in r43["evaluation_result"]:
        if item.get("status") == "blocked":
            lines.append(f"- {item['candidate_type']}: blocked / {item.get('blocked_reason')}")
        else:
            lines.append(
                f"- {item['candidate_type']}: {item['total_score']}/35, basic_quality_pass={str(item['basic_quality_pass']).lower()}"
            )
    lines.extend(["", "## Human Review Focus", ""])
    lines.extend([f"- {item}" for item in r43["human_review_focus"]])
    return "\n".join(lines) + "\n"


def r43_panel_html(r43: dict[str, Any]) -> str:
    rows = []
    for item in r43["evaluation_result"]:
        if item.get("status") == "blocked":
            score = "blocked"
            passed = "false"
        else:
            score = f"{item['total_score']}/35"
            passed = str(item["basic_quality_pass"]).lower()
        rows.append(f"<tr><td>{item['candidate_type']}</td><td>{score}</td><td>{passed}</td><td>{item.get('requires_human_attention', True)}</td></tr>")
    return """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>R43 Quality Panel</title>
<style>body{font-family:Arial,'Microsoft YaHei',sans-serif;margin:24px;color:#183b35}table{border-collapse:collapse;width:100%}td,th{border:1px solid #cfe1d8;padding:8px}th{background:#edf7f2}</style></head>
<body data-sandbox-only="true" data-formal-apply-allowed="false">
<h1>R43 质量评分面板</h1>
<table><thead><tr><th>候选</th><th>分数</th><th>基础过关</th><th>人工重点看</th></tr></thead><tbody>
""" + "\n".join(rows) + """
</tbody></table></body></html>
"""


def r44_comparison_md(r44: dict[str, Any]) -> str:
    comparison = r44["quality_comparison"]
    return (
        report_header(r44["stage"], r44["final_status"])
        + f"""
## V1/V2 Comparison

- v1_candidate_score={comparison['v1_score']}
- v2_candidate_score={comparison['v2_score']}
- improved={str(comparison['improved']).lower()}
- improvement_delta={comparison['improvement_delta']}
- v2_basic_quality_pass={str(comparison['v2_basic_quality_pass']).lower()}

## Still Insufficient

{chr(10).join('- ' + item for item in comparison.get('still_insufficient') or [])}
"""
    )


def gpt_review_note(loop: dict[str, Any]) -> str:
    statuses = loop["stage_statuses"]
    return f"""# GPT Review Note

This R40-R44 package is for model generation quality testing, not formal apply.

```text
R40={statuses['R40']}
R41={statuses['R41']}
R42={statuses['R42']}
R43={statuses['R43']}
R44={statuses['R44']}
provider_called_in_sandbox={str(loop['provider_called_in_sandbox']).lower()}
model_called_in_sandbox={str(loop['model_called_in_sandbox']).lower()}
formal_apply=NO
real_write=NO
NEXT_STAGE=R45_USER_REVIEW_MODEL_QUALITY_AND_NEXT_SCOPE
```

Please review:

1. Whether generated candidates are useful enough for teacher second editing.
2. Whether courseware, big-screen, and worksheet candidates are concrete rather than empty slogans.
3. Whether the model fabricated textbook pages, materials, or student data.
4. Whether prompt/schema adjustment in R44 improved quality.

No formal lesson save, export, archive, database, Feishu, memory write, student private data use, original overwrite, or main repo push is authorized.
"""


def main() -> None:
    from backend.xiaobei_ai import prep_room_model_quality_loop_1013R_R40_R44 as loop

    r40 = loop.build_r40_gate()
    r41 = loop.build_r41_single_case_generation()
    r42 = loop.build_r42_multi_candidate_generation(r41)
    r43 = loop.build_r43_quality_evaluation(r42)
    r44 = loop.build_r44_regeneration(r41, r43)
    continuous = {
        "ok": all(item.get("ok") for item in [r40, r41, r42, r43, r44]),
        "stage": loop.STAGE_ID,
        "generated_at": now(),
        "stage_statuses": {
            "R40": r40["final_status"],
            "R41": r41["final_status"],
            "R42": r42["final_status"],
            "R43": r43["final_status"],
            "R44": r44["final_status"],
        },
        "provider_called_in_sandbox": any(item.get("boundary", {}).get("provider_called") for item in [r40, r41, r42, r43, r44]),
        "model_called_in_sandbox": any(item.get("boundary", {}).get("model_called") for item in [r40, r41, r42, r43, r44]),
        "formal_apply": "NO",
        "real_write": "NO",
        "next_stage": "R45_USER_REVIEW_MODEL_QUALITY_AND_NEXT_SCOPE",
    }

    write_json(R40_DIR / "R40_model_quality_sandbox_gate.json", r40)
    write_json(R40_DIR / "R40_result.json", r40)
    write_text(R40_DIR / "R40_model_quality_sandbox_gate.md", r40_gate_md(r40))

    write_json(R41_DIR / "R41_model_call_log.json", r41["model_call_log"])
    write_json(R41_DIR / "R41_single_case_candidate.json", r41["candidate"])
    write_json(R41_DIR / "R41_result.json", r41)
    write_text(R41_DIR / "R41_single_case_candidate.md", r41["candidate_markdown"])
    write_text(R41_DIR / "R41_report.md", r41_report_md(r41))
    write_text(R41_DIR / ".env.example", "MINIMAX_API_KEY=<set in environment only>\nMINIMAX_API_BASE=https://api.minimaxi.com/v1\nMINIMAX_MODEL=MiniMax-M3\n")

    write_json(R42_DIR / "R42_multi_candidate_generation_state.json", {"candidates": r42["candidates"], "model_call_log": r42["model_call_log"]})
    write_text(R42_DIR / "R42_multi_candidate_preview.html", r42["preview_html"])
    for item in r42["candidates"]:
        write_text(R42_DIR / f"R42_{item['candidate_type']}.md", loop._candidate_markdown({"candidate_id": item["candidate_id"], "candidate_type": item["candidate_type"], "source": item["source"], "provider_called": r42["model_call_log"].get("provider_called"), "model_called": r42["model_call_log"].get("model_called"), "before_text": item["before_or_context"], "after_text": item["candidate_content"], "xiaojiao_suggestion": item["xiaojiao_suggestion"]}))
    write_json(R42_DIR / "R42_result.json", {k: v for k, v in r42.items() if k != "preview_html"})
    write_text(R42_DIR / "R42_report.md", r42_report_md(r42))

    write_json(R43_DIR / "R43_quality_rubric.json", r43["quality_rubric"])
    write_json(R43_DIR / "R43_quality_evaluation_result.json", r43)
    write_text(R43_DIR / "R43_quality_review.md", r43_review_md(r43))
    write_text(R43_DIR / "R43_quality_panel.html", r43_panel_html(r43))
    write_json(R43_DIR / "R43_result.json", r43)

    write_text(R44_DIR / "R44_prompt_adjustment_plan.md", "\n".join(f"- {item}" for item in r44["prompt_adjustment_plan"]) + "\n")
    write_text(R44_DIR / "R44_prompt_v1.md", r44["prompt_v1"])
    write_text(R44_DIR / "R44_prompt_v2.md", r44["prompt_v2"])
    write_text(R44_DIR / "R44_schema_adjustment_notes.md", "\n".join(f"- {item}" for item in r44["schema_adjustment_notes"]) + "\n")
    write_json(R44_DIR / "R44_regeneration_result.json", r44)
    write_text(R44_DIR / "R44_quality_comparison.md", r44_comparison_md(r44))
    write_json(R44_DIR / "R44_result.json", r44)

    write_json(OUT_ROOT / "1013R_R40_R44_MODEL_GENERATION_QUALITY_LOOP_REVIEW_STAGING_RESULT.json", continuous)
    write_text(OUT_ROOT / "1013R_R40_R44_MODEL_GENERATION_QUALITY_LOOP_GPT_REVIEW_NOTE.md", gpt_review_note(continuous))
    if not continuous["ok"]:
        raise SystemExit("BLOCKED: one or more R40-R44 stages failed")
    print(json.dumps(continuous, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
