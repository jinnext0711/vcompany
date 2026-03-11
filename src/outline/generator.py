"""Phase 2: アウトライン生成モジュール - 資料の構成設計

Claude Codeが構成を設計し、結果をこのモジュールのデータ形式で渡す。
"""


def create_outline(title: str, sections: list) -> dict:
    """アウトラインデータを構造化する。

    Args:
        title: 資料タイトル
        sections: セクションのリスト
            各セクション: {
                "title": セクションタイトル,
                "content_points": [内容ポイント],
                "notes": 補足情報
            }

    Returns:
        dict: 標準化されたアウトラインデータ
    """
    return {
        "title": title,
        "sections": sections,
    }
