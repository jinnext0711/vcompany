"""Phase 1: リサーチモジュール - テーマに基づく材料収集

Claude Codeがリサーチを実施し、結果をこのモジュールのデータ形式で渡す。
"""


def create_research_data(
    theme: str,
    key_points: list,
    research_summary: str,
    sources: list = None,
) -> dict:
    """リサーチ結果をデータ構造にまとめる。

    Args:
        theme: 資料のテーマ
        key_points: 主要ポイントのリスト
        research_summary: リサーチ要約
        sources: 参考情報のリスト

    Returns:
        dict: 標準化されたリサーチデータ
    """
    return {
        "theme": theme,
        "key_points": key_points,
        "research_summary": research_summary,
        "sources": sources or [],
    }
