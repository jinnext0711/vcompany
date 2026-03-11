"""Phase 2: アウトライン生成モジュール - 資料の構成設計"""

import json
import re

import anthropic


def generate_outline(research_data: dict, output_format: str = "pptx") -> dict:
    """リサーチ結果からアウトラインを生成する。

    Args:
        research_data: リサーチモジュールの出力
        output_format: 出力形式 ("pptx", "markdown", "pdf", "html")

    Returns:
        dict: {
            "title": 資料タイトル,
            "sections": [
                {
                    "title": セクションタイトル,
                    "content_points": [内容ポイント],
                    "notes": 補足情報
                }
            ]
        }
    """
    client = anthropic.Anthropic()

    format_guidance = {
        "pptx": "スライド形式（1セクション = 1スライド、各スライドのポイントは3〜5個）",
        "markdown": "ドキュメント形式（階層的な見出し構成、詳細な説明を含む）",
        "pdf": "レポート形式（章立て構成、フォーマルな構成）",
        "html": "Web形式（セクション分け、視覚的な構成）",
    }

    prompt = f"""あなたは資料構成の専門家です。以下のリサーチ結果から、{format_guidance.get(output_format, "一般的な")}資料のアウトラインを作成してください。

テーマ: {research_data.get("theme", "")}
主要ポイント: {json.dumps(research_data.get("key_points", []), ensure_ascii=False)}
リサーチ要約: {research_data.get("research_summary", "")}

以下の形式でJSON出力してください（```json ブロックで囲んでください）:
{{
    "title": "資料タイトル",
    "sections": [
        {{
            "title": "セクションタイトル",
            "content_points": ["ポイント1", "ポイント2", "ポイント3"],
            "notes": "補足情報やスピーカーノート"
        }}
    ]
}}

重要:
- 論理的な流れを意識した構成にすること
- 導入 → 本論 → まとめ の基本構成を守ること
- セクション数は8〜15程度
- 各セクションのポイントは簡潔かつ具体的に"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    response_text = message.content[0].text
    json_match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))

    return json.loads(response_text)
