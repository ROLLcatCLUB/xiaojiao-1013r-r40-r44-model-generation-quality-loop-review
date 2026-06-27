from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from shutil import which
from typing import Any

from . import prep_room_page_copy_package_binding_1013R_R21 as r21_binding
from . import prep_room_teacher_visible_smoke_1013R_R34 as r34_smoke


STAGE_ID = "1013R_R35_R39_CONTINUOUS_PREP_ROOM_EXPERIENCE_TO_CANDIDATE_PREVIEW"
R35_STAGE_ID = "1013R_R35_COMPACT_TEACHER_EXPERIENCE_REVIEW_PACKAGE"
R36_STAGE_ID = "1013R_R36_RUNTIME_GATE_AUDIT_ONLY"
R37_STAGE_ID = "1013R_R37_READONLY_ENDPOINT_BRIDGE_CONTRACT"
R38_STAGE_ID = "1013R_R38_MODEL_SANDBOX_CONTRACT_MOCK_SINGLE_CASE"
R39_STAGE_ID = "1013R_R39_CANDIDATE_PREVIEW_BACKFILL"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def boundary_flags(stage: str = STAGE_ID) -> dict[str, bool | str]:
    return {
        "stage": stage,
        "review_package_only": True,
        "static_fixture_only": True,
        "preview_only": True,
        "readonly_contract_only": True,
        "candidate_preview_only": True,
        "runtime_connected": False,
        "endpoint_registered": False,
        "provider_called": False,
        "model_called": False,
        "database_written": False,
        "feishu_written": False,
        "memory_written": False,
        "vector_index_written": False,
        "student_data_read": False,
        "real_generation_performed": False,
        "formal_apply_performed": False,
        "save_performed": False,
        "export_performed": False,
        "archive_performed": False,
        "main_repo_pushed": False,
        "main_runtime_modified": False,
        "R40_requires_user_review": True,
    }


def _base_html() -> str:
    page = r21_binding.build_binding_sample_bundle()
    return str(page.get("html") or "")


def _inject_before_body_end(html: str, injection: str) -> str:
    marker = "</body>"
    if marker in html:
        return html.replace(marker, injection + "\n" + marker)
    return html + "\n" + injection


def build_r35_scenarios() -> list[dict[str, Any]]:
    return [
        {
            "user_input": "课件入口找不到",
            "xiaojiao_judgement": "老师在找课堂派生物入口，优先定位右侧课件制作入口。",
            "frame_level": 3,
            "problem_target": "3级课堂派生物入口",
            "diagnosis_entry": "右侧大屏草稿 / 课件制作入口",
            "room_id": "prep_room",
            "tool_id": "courseware_workspace",
            "slot_id": "courseware_entry",
            "visible_result": "定位到右侧大屏草稿里的课件制作入口，不再跳到左下角流程关系。",
            "blocked": False,
            "action_gate_required": False,
            "teacher_explanation": "这里先帮老师找到课件入口，只做入口定位，不生成正式课件。",
            "expected_ui_state": "右侧课堂派生物区域可见，课件制作入口处于普通产品态提示。",
        },
        {
            "user_input": "这段教案太乱",
            "xiaojiao_judgement": "这是内容组织问题，先由顶部小教判断区承接，再引导老师查看教学过程。",
            "frame_level": {"primary_frame_level": 4, "entry_frame_level": 1},
            "problem_target": "4级内容组织问题",
            "diagnosis_entry": "顶部小教状态/判断区",
            "room_id": "prep_room",
            "tool_id": "prep_notebook",
            "slot_id": "xiaojiao_task_state",
            "visible_result": "先定位到顶部小教状态/判断区，提示教学过程需要整理，再由老师决定具体跳到哪段。",
            "blocked": False,
            "action_gate_required": False,
            "teacher_explanation": "不能把内容混乱误判成平台壳层问题；入口在顶部，目标是4级教案正文组织。",
            "expected_ui_state": "顶部小教判断区给出整理方向，正文仍保持预览态，不自动改写。",
        },
        {
            "user_input": "帮我生成大屏",
            "xiaojiao_judgement": "老师想看课堂大屏候选，当前只允许预览草稿。",
            "frame_level": 3,
            "problem_target": "3级课堂派生物预览",
            "diagnosis_entry": "右侧大屏预览",
            "room_id": "prep_room",
            "tool_id": "classroom_display_preview",
            "slot_id": "classroom_display_screen",
            "visible_result": "定位到右侧大屏预览/大屏草稿；只展示预览态，不导出、不生成正式课件。",
            "blocked": False,
            "action_gate_required": False,
            "teacher_explanation": "这里可以看大屏草稿方向，但不触发真实生成和导出。",
            "expected_ui_state": "右侧大屏预览区域可见，状态为 preview_only=true。",
        },
        {
            "user_input": "评价表怎么没有",
            "xiaojiao_judgement": "评价维度缺失，需教师先确认评价依据。",
            "frame_level": 3,
            "problem_target": "3级依据与评价",
            "diagnosis_entry": "右侧评价表预览",
            "room_id": "prep_room",
            "tool_id": "source_evidence",
            "slot_id": "assessment_rubric",
            "visible_result": "定位到右侧评价表预览，并显示 blocked：评价维度需教师确认。",
            "blocked": True,
            "blocked_reason": "评价维度需教师确认",
            "action_gate_required": True,
            "teacher_explanation": "评价表不能凭空补齐；先显示缺口，再等老师确认维度。",
            "expected_ui_state": "评价表预览保留 blocked 说明，不能假装已生成。",
        },
        {
            "user_input": "我要保存这个课包",
            "xiaojiao_judgement": "这是正式动作请求，必须进入教师确认门，当前只显示已导出/保存说明样式。",
            "frame_level": 3,
            "problem_target": "动作门 / 保存导出归档",
            "diagnosis_entry": "右侧保存/导出确认门",
            "room_id": "prep_room",
            "tool_id": "teacher_action_gate",
            "slot_id": "package_save_gate",
            "visible_result": "定位到右侧保存/导出说明；当前只是预览说明，不能写入正式课包。",
            "blocked": True,
            "blocked_reason": "保存、导出、归档需要教师确认，formal_apply_allowed=false",
            "action_gate_required": True,
            "teacher_explanation": "这里不是实际保存，而是告诉老师当前课包仍在预览态，R40 前不能正式应用。",
            "expected_ui_state": "右侧动作门说明可见，保存按钮保持 blocked 或 preview_only。",
        },
    ]


def _product_mode_injection() -> str:
    return """
<style id="shiwei-r35-product-mode-style">
  body[data-shiwei-mode="product"] [data-shiwei-hide-after-review="true"] {
    display: none !important;
  }
  body[data-shiwei-mode="product"] .r35-product-panel,
  body[data-shiwei-mode="product"] .r39-candidate-preview-panel {
    border: 1px solid rgba(45, 120, 102, 0.22);
    background: rgba(247, 252, 249, 0.96);
    color: #183b35;
    border-radius: 8px;
    padding: 12px 14px;
    margin: 12px 0;
    box-shadow: 0 8px 22px rgba(26, 74, 64, 0.06);
  }
  body[data-shiwei-mode="product"] .r35-product-panel strong,
  body[data-shiwei-mode="product"] .r39-candidate-preview-panel strong {
    color: #247466;
  }
  body[data-shiwei-mode="product"] .r35-product-panel .blocked,
  body[data-shiwei-mode="product"] .r39-candidate-preview-panel .blocked {
    color: #8a5a10;
  }
</style>
<script id="shiwei-r35-product-mode-script">
  document.body.setAttribute("data-shiwei-mode", "product");
</script>
<section class="r35-product-panel" data-shiwei-product-retained="true" data-preview-only="true" data-formal-apply-allowed="false">
  <strong>小教判断区</strong>
  <p>当前空间：备课室。工具分组：备课设计 / 课堂派生物 / 依据与评价 / 动作门。</p>
  <p>产品态保留普通提示：课件入口、大屏预览、评价表预览、保存/导出确认门均可定位；红色删除层默认隐藏。</p>
  <p>preview_only=true；formal_apply_allowed=false；评价表 blocked：评价维度需教师确认；保存/导出确认门 blocked。</p>
</section>"""


def build_r35_review_mode_html() -> str:
    html = _base_html()
    return _inject_before_body_end(
        html,
        """
<script id="shiwei-r35-review-mode-script">
  document.body.setAttribute("data-shiwei-mode", "review");
</script>""",
    )


def build_r35_product_mode_html() -> str:
    html = _base_html()
    return _inject_before_body_end(html, _product_mode_injection())


def _textual_dom_smoke(html: str, mode: str) -> dict[str, Any]:
    common_checks = {
        "current_space_prep_room_visible": "备课室" in html,
        "tool_groups_visible": all(token in html for token in ["备课设计", "课堂派生物", "依据与评价", "动作门"]),
        "xiaojiao_judgement_visible": "小教判断" in html or "小教判断区" in html,
        "preview_area_visible": "预览" in html,
        "assessment_blocked_visible": "评价表" in html and "blocked" in html,
        "save_export_gate_visible": "保存" in html and "导出" in html and "formal_apply_allowed=false" in html,
        "preview_only_visible": "preview_only=true" in html or 'data-preview-only="true"' in html,
        "formal_apply_false_visible": "formal_apply_allowed=false" in html or 'data-formal-apply-allowed="false"' in html,
    }
    if mode == "review":
        mode_checks = {
            "red_review_markers_visible": 'data-shiwei-hide-after-review="true"' in html and "#b42323" in html,
            "review_mode_marker": 'data-shiwei-mode", "review"' in html,
        }
    else:
        mode_checks = {
            "hide_after_review_rule_present": '[data-shiwei-hide-after-review="true"]' in html and "display: none" in html,
            "product_mode_marker": 'data-shiwei-mode", "product"' in html,
            "product_retained_panel_visible": 'data-shiwei-product-retained="true"' in html,
        }
    checks = {**common_checks, **mode_checks}
    return {
        "mode": f"{mode}_html_textual_smoke",
        "pass": all(checks.values()),
        "checks": checks,
        "marker_counts": {
            "hide_after_review": html.count('data-shiwei-hide-after-review="true"'),
            "product_retained": html.count('data-shiwei-product-retained="true"'),
        },
    }


def build_r35_package() -> dict[str, Any]:
    review_html = build_r35_review_mode_html()
    product_html = build_r35_product_mode_html()
    review_smoke = _textual_dom_smoke(review_html, "review")
    product_smoke = _textual_dom_smoke(product_html, "product")
    screenshot_smoke = r34_smoke.screenshot_smoke_plan()
    screenshot_smoke = {
        **screenshot_smoke,
        "requested_files": [
            "product_default_prep_room_2k.png",
            "product_assessment_blocked_2k.png",
            "product_save_gate_2k.png",
            "review_mode_red_layers_2k.png",
        ],
        "truthful_status": "fallback" if not screenshot_smoke.get("available") else "available_but_not_captured_by_static_validator",
        "html_textual_smoke": True,
        "scenario_state_textual_smoke": True,
    }
    scenarios = build_r35_scenarios()
    ok = review_smoke["pass"] and product_smoke["pass"] and len(scenarios) == 5
    return {
        "ok": ok,
        "stage": R35_STAGE_ID,
        "generated_at": _now(),
        "review_mode_html": review_html,
        "product_mode_html": product_html,
        "teacher_experience_scenarios": scenarios,
        "review_dom_smoke": review_smoke,
        "product_dom_smoke": product_smoke,
        "screenshot_smoke": screenshot_smoke,
        "boundary": boundary_flags(R35_STAGE_ID),
        "final_status": "PASS_R35_COMPACT_TEACHER_EXPERIENCE_REVIEW_PACKAGE" if ok else "BLOCKED",
        "next_stage": "R36_RUNTIME_GATE_AUDIT_ONLY" if ok else "",
    }


def build_r36_audit_matrix() -> dict[str, Any]:
    rows = [
        ("大单元读取", "allow_readonly", "只读 viewmodel 可用于左侧目录和单元定位。"),
        ("单课 viewmodel 读取", "allow_readonly", "只读读取当前课时结构，不改写教案正文。"),
        ("课件 viewmodel 读取", "allow_readonly", "可读取课件草稿结构用于预览入口。"),
        ("大屏 viewmodel 读取", "allow_readonly", "可读取大屏草稿结构用于预览。"),
        ("资料索引读取", "allow_readonly", "可读资料索引，但不能写入资料库。"),
        ("评价维度读取", "allow_readonly", "可读已有维度；缺失时 blocked。"),
        ("候选生成", "allow_fixture_only", "R38 仅 mock candidate，不调用真实模型。"),
        ("候选预览", "allow_fixture_only", "R39 仅回填候选预览，不覆盖原文。"),
        ("保存备课本", "hold", "进入 R40 formal apply 决策前不得执行。"),
        ("导出课件", "hold", "需要教师确认和正式导出授权。"),
        ("导出学习单", "hold", "需要教师确认和正式导出授权。"),
        ("写数据库", "forbidden", "当前连续推进包禁止真实写入。"),
        ("写飞书", "forbidden", "当前连续推进包禁止真实外部写入。"),
        ("写记忆", "forbidden", "当前连续推进包禁止记忆写入。"),
        ("formal apply", "forbidden", "R40 前必须停止给用户审核。"),
        ("学生数据读取", "forbidden", "当前包不接真实学生数据。"),
    ]
    return {
        "ok": True,
        "stage": R36_STAGE_ID,
        "generated_at": _now(),
        "audit_matrix": [
            {
                "capability": capability,
                "decision": decision,
                "reason": reason,
                "teacher_confirmation_required": decision in {"hold", "forbidden"} or "候选" in capability,
            }
            for capability, decision, reason in rows
        ],
        "summary": {
            "allow_readonly": [capability for capability, decision, _ in rows if decision == "allow_readonly"],
            "allow_fixture_only": [capability for capability, decision, _ in rows if decision == "allow_fixture_only"],
            "hold": [capability for capability, decision, _ in rows if decision == "hold"],
            "forbidden": [capability for capability, decision, _ in rows if decision == "forbidden"],
        },
        "boundary": boundary_flags(R36_STAGE_ID),
        "final_status": "PASS_R36_RUNTIME_GATE_AUDIT_ONLY",
        "next_stage": "R37_READONLY_ENDPOINT_BRIDGE_CONTRACT",
    }


def build_r37_contract() -> dict[str, Any]:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "R37ReadonlyBridgeViewModel",
        "type": "object",
        "required": ["data_source", "write_allowed", "formal_apply_allowed", "viewmodels"],
        "properties": {
            "data_source": {"enum": ["fixture", "readonly_endpoint_placeholder"]},
            "write_allowed": {"const": False},
            "formal_apply_allowed": {"const": False},
            "viewmodels": {"type": "object"},
        },
    }
    fixture = {
        "data_source": "fixture",
        "write_allowed": False,
        "formal_apply_allowed": False,
        "viewmodels": {
            "lesson_viewmodel": {"lesson_id": "2-1", "title": "色彩的渐变", "readonly": True},
            "courseware_preview_viewmodel": {"status": "draft", "source": "fixture"},
            "classroom_display_preview_viewmodel": {"status": "draft", "source": "fixture"},
            "materials_index_viewmodel": {"status": "readonly_index"},
            "assessment_rubric_viewmodel": {"status": "blocked_until_teacher_dimension"},
            "action_gate_state_viewmodel": {"save": "blocked", "export": "blocked", "archive": "blocked"},
        },
        "blocked_objects": [
            "save_lesson",
            "export_courseware",
            "export_worksheet",
            "write_feishu",
            "write_memory",
            "formal_apply",
        ],
    }
    return {
        "ok": True,
        "stage": R37_STAGE_ID,
        "generated_at": _now(),
        "bridge_contract": {
            "input": "lesson_id + room_id + readonly feature flags",
            "output": "readonly viewmodel for prep-room preview",
            "allowed_sources": ["fixture", "readonly_endpoint_placeholder"],
            "write_allowed": False,
            "formal_apply_allowed": False,
        },
        "schema": schema,
        "fixture_viewmodel": fixture,
        "boundary": boundary_flags(R37_STAGE_ID),
        "final_status": "PASS_R37_READONLY_ENDPOINT_BRIDGE_CONTRACT",
        "next_stage": "R38_MODEL_SANDBOX_CONTRACT_AND_MOCK_SINGLE_CASE",
    }


def build_r38_mock_single_case() -> dict[str, Any]:
    prompt_schema = {
        "type": "object",
        "required": ["teacher_input", "lesson_context", "provider_call_allowed"],
        "properties": {
            "teacher_input": {"type": "string"},
            "lesson_context": {"type": "object"},
            "provider_call_allowed": {"const": False},
        },
    }
    output_schema = {
        "type": "object",
        "required": ["before_text", "after_text", "xiaojiao_suggestion", "teacher_confirmation_required"],
        "properties": {
            "before_text": {"type": "string"},
            "after_text": {"type": "string"},
            "xiaojiao_suggestion": {"type": "string"},
            "confidence": {"type": "number"},
            "risk_notes": {"type": "array", "items": {"type": "string"}},
            "teacher_confirmation_required": {"const": True},
            "formal_apply_allowed": {"const": False},
        },
    }
    candidate = {
        "source": "mock_candidate_fixture",
        "provider_call": False,
        "model_call": False,
        "teacher_input": "这段教案太乱，帮我整理教学过程。",
        "before_text": "看图渐变，比较明度，尝试调色，展示作品。",
        "after_text": "先观察自然与教材中的渐变，再比较同一颜色加入白色、黑色或灰色后的层次变化，随后用试色纸完成3到5格渐变，最后展示作品并说明颜色变化过程。",
        "xiaojiao_suggestion": "把教学过程整理成观察、比较、试色、表达四步，方便老师逐段确认。",
        "confidence": 0.72,
        "risk_notes": ["仅为 mock 候选", "不能覆盖原教案", "需要教师确认后才可进入 R40"],
        "teacher_confirmation_required": True,
        "formal_apply_allowed": False,
    }
    return {
        "ok": True,
        "stage": R38_STAGE_ID,
        "generated_at": _now(),
        "model_sandbox_contract": {
            "provider": "mock_provider_only",
            "provider_call_allowed": False,
            "model_call_allowed": False,
            "api_key_allowed": False,
            "candidate_patch_allowed": "preview_only",
        },
        "prompt_input_schema": prompt_schema,
        "model_output_schema": output_schema,
        "candidate_patch_schema": output_schema,
        "mock_candidate_fixture": candidate,
        "failure_strategy": [
            "schema invalid -> blocked preview",
            "provider required -> BLOCKED and request user authorization",
            "teacher confirmation missing -> do not apply",
        ],
        "boundary": boundary_flags(R38_STAGE_ID),
        "final_status": "PASS_R38_MODEL_SANDBOX_CONTRACT_MOCK_SINGLE_CASE",
        "next_stage": "R39_CANDIDATE_PREVIEW_BACKFILL",
    }


def _candidate_preview_injection(candidate: dict[str, Any]) -> str:
    return f"""
<section class="r39-candidate-preview-panel" data-shiwei-product-retained="true" data-candidate-source="mock_candidate_fixture" data-provider-call="false" data-formal-apply-allowed="false">
  <strong>小教候选预览</strong>
  <p>source=mock_candidate_fixture；provider_call=false；formal_apply_allowed=false。</p>
  <div><strong>修改前</strong><p>{candidate["before_text"]}</p></div>
  <div><strong>修改后</strong><p>{candidate["after_text"]}</p></div>
  <div><strong>小教建议</strong><p>{candidate["xiaojiao_suggestion"]}</p></div>
  <div><strong>风险提醒</strong><p>{"; ".join(candidate["risk_notes"])}</p></div>
  <p class="blocked">教师确认门：采纳候选=preview_only；保存=blocked；导出=blocked。</p>
</section>"""


def build_r39_candidate_preview() -> dict[str, Any]:
    candidate = build_r38_mock_single_case()["mock_candidate_fixture"]
    product_html = build_r35_product_mode_html()
    candidate_html = _inject_before_body_end(product_html, _candidate_preview_injection(candidate))
    checks = {
        "before_after_visible": "修改前" in candidate_html and "修改后" in candidate_html,
        "suggestion_visible": "小教建议" in candidate_html,
        "risk_visible": "风险提醒" in candidate_html,
        "teacher_gate_visible": "教师确认门" in candidate_html,
        "source_visible": "source=mock_candidate_fixture" in candidate_html,
        "provider_call_false_visible": "provider_call=false" in candidate_html,
        "formal_apply_false_visible": "formal_apply_allowed=false" in candidate_html,
        "save_export_blocked_visible": "保存=blocked" in candidate_html and "导出=blocked" in candidate_html,
    }
    return {
        "ok": all(checks.values()),
        "stage": R39_STAGE_ID,
        "generated_at": _now(),
        "candidate_preview_state": {
            "candidate": deepcopy(candidate),
            "ui_checks": checks,
            "does_not_overwrite_original_lesson": True,
            "write_allowed": False,
            "formal_apply_allowed": False,
        },
        "product_mode_candidate_preview_html": candidate_html,
        "boundary": boundary_flags(R39_STAGE_ID),
        "final_status": "PASS_R39_CANDIDATE_PREVIEW_BACKFILL" if all(checks.values()) else "BLOCKED",
        "next_stage": "R40_FORMAL_APPLY_DECISION_REQUIRES_USER_REVIEW" if all(checks.values()) else "",
    }


def build_continuous_result() -> dict[str, Any]:
    r35 = build_r35_package()
    r36 = build_r36_audit_matrix()
    r37 = build_r37_contract()
    r38 = build_r38_mock_single_case()
    r39 = build_r39_candidate_preview()
    stages = [r35, r36, r37, r38, r39]
    ok = all(stage.get("ok") for stage in stages)
    return {
        "ok": ok,
        "stage": STAGE_ID,
        "generated_at": _now(),
        "stage_statuses": {
            "R35": r35.get("final_status"),
            "R36": r36.get("final_status"),
            "R37": r37.get("final_status"),
            "R38": r38.get("final_status"),
            "R39": r39.get("final_status"),
        },
        "provider_model_call": "NO",
        "real_write": "NO",
        "formal_apply": "NO",
        "R40_decision": "requires_user_review",
        "boundary": boundary_flags(STAGE_ID),
        "next_stage": "R40_FORMAL_APPLY_DECISION_REQUIRES_USER_REVIEW",
    }
