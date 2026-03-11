"""Phase 3: 執筆モジュール - 各セクションの本文作成

Claude Codeが本文を執筆し、結果をこのモジュールのデータ形式で渡す。
"""


def create_content(title: str, sections: list) -> dict:
    """執筆済みコンテンツをデータ構造にまとめる。

    Args:
        title: 資料タイトル
        sections: セクションのリスト
            各セクション: {
                "title": セクションタイトル,
                "body": 本文,
                "bullet_points": [箇条書きポイント],
                "notes": スピーカーノート
            }

    Returns:
        dict: 標準化されたコンテンツデータ
    """
    return {
        "title": title,
        "sections": sections,
    }
