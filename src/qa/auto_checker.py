"""Phase 5: 品質チェックモジュール - 自動チェック・修正

Claude Codeが品質チェックを実施し、修正済みコンテンツとレビュー結果を渡す。
"""


def create_qa_result(
    corrected_content: dict,
    auto_fixes: list = None,
    manual_review_items: list = None,
) -> dict:
    """品質チェック結果をデータ構造にまとめる。

    Args:
        corrected_content: 修正済みコンテンツ（contentと同じ構造）
        auto_fixes: 自動修正した項目のリスト
            各項目: {"item": 修正項目, "before": 修正前, "after": 修正後}
        manual_review_items: Owner確認が必要な項目のリスト
            各項目: {"item": 確認項目, "detail": 詳細, "section": 該当セクション}

    Returns:
        dict: 標準化された品質チェック結果
    """
    return {
        "corrected_content": corrected_content,
        "auto_fixes": auto_fixes or [],
        "manual_review_items": manual_review_items or [],
    }
