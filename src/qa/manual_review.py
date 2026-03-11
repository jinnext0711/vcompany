"""Phase 5b: 手動レビューモジュール - Owner確認が必要な項目の提示"""


def present_review_items(qa_result: dict) -> list:
    """Owner確認が必要な項目をフォーマットして返す。

    Args:
        qa_result: auto_checkerの出力

    Returns:
        list: 確認項目のリスト
    """
    items = qa_result.get("manual_review_items", [])

    if not items:
        return []

    formatted = []
    for i, item in enumerate(items, 1):
        formatted.append(
            {
                "number": i,
                "item": item.get("item", ""),
                "detail": item.get("detail", ""),
                "section": item.get("section", ""),
            }
        )

    return formatted


def format_review_report(review_items: list) -> str:
    """レビュー項目を人間が読みやすい形式にフォーマットする。

    Args:
        review_items: present_review_itemsの出力

    Returns:
        str: フォーマット済みレポート
    """
    if not review_items:
        return "自動チェックで全項目クリアしました。Owner確認が必要な項目はありません。"

    lines = ["## Owner確認が必要な項目\n"]
    for item in review_items:
        lines.append(f"### {item['number']}. {item['item']}")
        lines.append(f"- **該当セクション:** {item['section']}")
        lines.append(f"- **詳細:** {item['detail']}")
        lines.append("")

    return "\n".join(lines)
