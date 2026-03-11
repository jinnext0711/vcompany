"""Phase 1: リサーチモジュール - テーマに基づく材料収集"""

import anthropic


def collect_materials(theme: str, additional_context: str = "") -> dict:
    """テーマに基づいてリサーチを行い、材料を収集する。

    Args:
        theme: 資料のテーマ
        additional_context: 追加のコンテキスト情報

    Returns:
        dict: {
            "theme": テーマ,
            "key_points": 主要ポイントのリスト,
            "research_summary": リサーチ要約,
            "sources": 参考情報のリスト
        }
    """
    client = anthropic.Anthropic()

    prompt = f"""あなたはリサーチの専門家です。以下のテーマについて、資料作成に必要な材料を収集・整理してください。

テーマ: {theme}
{"追加コンテキスト: " + additional_context if additional_context else ""}

以下の形式でJSON出力してください（```json ブロックで囲んでください）:
{{
    "theme": "テーマ",
    "key_points": ["主要ポイント1", "主要ポイント2", ...],
    "research_summary": "リサーチの要約（500文字程度）",
    "sources": ["参考情報1", "参考情報2", ...]
}}

重要:
- 正確で信頼性の高い情報を提供すること
- 主要ポイントは5〜10個程度
- 資料作成に直接使える具体的な情報を含めること"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    import json
    import re

    response_text = message.content[0].text
    json_match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))

    # JSONブロックがない場合、直接パースを試みる
    return json.loads(response_text)
