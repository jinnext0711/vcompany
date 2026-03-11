"""Markdown出力エクスポーター"""

from pathlib import Path


def export_markdown(content: dict, output_path: str) -> str:
    """コンテンツをMarkdownファイルとして出力する。

    Args:
        content: 執筆モジュールの出力（QA済み）
        output_path: 出力ファイルパス

    Returns:
        str: 出力ファイルのパス
    """
    lines = []

    # タイトル
    title = content.get("title", "無題")
    lines.append(f"# {title}")
    lines.append("")

    # 各セクション
    for section in content.get("sections", []):
        section_title = section.get("title", "")
        body = section.get("body", "")
        bullet_points = section.get("bullet_points", [])

        lines.append(f"## {section_title}")
        lines.append("")

        if body:
            lines.append(body)
            lines.append("")

        if bullet_points:
            for point in bullet_points:
                lines.append(f"- {point}")
            lines.append("")

    md_content = "\n".join(lines)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return output_path
