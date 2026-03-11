"""Phase 3: 執筆モジュール - 各セクションの本文作成"""

import json
import re

import anthropic


def compose_content(
    outline: dict, research_data: dict, output_format: str = "pptx"
) -> dict:
    """アウトラインとリサーチ結果から本文を作成する。

    Args:
        outline: アウトライン生成モジュールの出力
        research_data: リサーチモジュールの出力
        output_format: 出力形式

    Returns:
        dict: {
            "title": 資料タイトル,
            "sections": [
                {
                    "title": セクションタイトル,
                    "body": 本文,
                    "bullet_points": [箇条書きポイント],
                    "notes": スピーカーノート
                }
            ]
        }
    """
    client = anthropic.Anthropic()

    format_instructions = {
        "pptx": "各セクションはスライド1枚分。bullet_pointsは3〜5個、bodyは簡潔に。notesにスピーカーノートを記載。",
        "markdown": "各セクションは見出し1つ分。bodyに詳細な説明文を記載。bullet_pointsで要点をまとめる。",
        "pdf": "各セクションは章1つ分。bodyにフォーマルな文章を記載。",
        "html": "各セクションは1ブロック分。bodyに説明文、bullet_pointsで要点を記載。",
    }

    prompt = f"""あなたはプロのテクニカルライターです。以下のアウトラインとリサーチ結果から、資料の本文を作成してください。

タイトル: {outline.get("title", "")}
アウトライン: {json.dumps(outline.get("sections", []), ensure_ascii=False)}
リサーチ要約: {research_data.get("research_summary", "")}
参考情報: {json.dumps(research_data.get("sources", []), ensure_ascii=False)}

形式: {format_instructions.get(output_format, "")}

以下の形式でJSON出力してください（```json ブロックで囲んでください）:
{{
    "title": "資料タイトル",
    "sections": [
        {{
            "title": "セクションタイトル",
            "body": "本文テキスト",
            "bullet_points": ["ポイント1", "ポイント2"],
            "notes": "スピーカーノートや補足"
        }}
    ]
}}

重要:
- 正確で分かりやすい文章にすること
- 専門用語には必要に応じて補足を入れること
- 各セクションで一貫したトーンを維持すること"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )

    response_text = message.content[0].text
    json_match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))

    return json.loads(response_text)
