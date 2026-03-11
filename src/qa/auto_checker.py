"""Phase 5: 品質チェックモジュール - 自動チェック・修正"""

import json
import re

import anthropic


def auto_check(content: dict, output_format: str = "pptx") -> dict:
    """コンテンツの品質を自動チェックし、修正可能な項目は修正する。

    Args:
        content: 執筆モジュールの出力
        output_format: 出力形式

    Returns:
        dict: {
            "corrected_content": 修正済みコンテンツ,
            "auto_fixes": [自動修正した項目のリスト],
            "manual_review_items": [Owner確認が必要な項目のリスト]
        }
    """
    client = anthropic.Anthropic()

    prompt = f"""あなたは品質管理の専門家です。以下の資料コンテンツを品質チェックし、修正してください。

コンテンツ:
{json.dumps(content, ensure_ascii=False, indent=2)}

出力形式: {output_format}

## 自動修正すべき項目（修正して返してください）
- 誤字・脱字
- 文章の統一性（語尾の統一、敬体/常体の混在）
- 箇条書きの体裁統一（句点の有無など）
- 冗長な表現の簡潔化
- セクション間の分量バランス

## Owner確認が必要な項目（指摘のみ）
- 内容の正確性に疑問がある箇所
- メッセージの妥当性
- 全体のストーリーラインの評価
- 機密情報が含まれていないか

以下の形式でJSON出力してください（```json ブロックで囲んでください）:
{{
    "corrected_content": {{修正済みのコンテンツ（元と同じ構造）}},
    "auto_fixes": [
        {{"item": "修正項目", "before": "修正前", "after": "修正後"}}
    ],
    "manual_review_items": [
        {{"item": "確認項目", "detail": "詳細", "section": "該当セクション"}}
    ]
}}"""

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
