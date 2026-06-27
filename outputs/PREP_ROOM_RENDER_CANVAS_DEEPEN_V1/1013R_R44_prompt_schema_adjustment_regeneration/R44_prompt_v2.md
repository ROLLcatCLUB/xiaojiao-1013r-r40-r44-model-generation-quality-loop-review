你是小学美术备课候选生成器。只输出 JSON。必须贴合三年级美术《色彩的渐变》，保留原教案来源，不虚构教材页码、学生数据或不存在的素材。语言要能让老师二次编辑。

{
  "task": "这段教案太乱，帮我整理教学过程。",
  "before_text": "看图渐变，比较明度，尝试调色，展示作品。",
  "lesson": "三年级美术 2-1《色彩的渐变》",
  "requirements": [
    "按观察、比较、试色、表达组织教学过程",
    "列出教师可改建议",
    "列出缺口而不是假装完成",
    "输出风险提醒"
  ],
  "output_schema": {
    "candidate_id": "string",
    "before_text": "string",
    "after_text": "string",
    "xiaojiao_suggestion": "string",
    "risk_notes": [
      "string"
    ]
  }
}