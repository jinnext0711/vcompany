"""HTML出力エクスポーター"""

from pathlib import Path

import markdown


def export_html(content: dict, output_path: str, css_path: str = None) -> str:
    """コンテンツをHTMLファイルとして出力する。

    Args:
        content: 執筆モジュールの出力（QA済み）
        output_path: 出力ファイルパス
        css_path: カスタムCSSファイルのパス（省略時はデフォルトスタイル）

    Returns:
        str: 出力ファイルのパス
    """
    # まずMarkdownに変換
    md_lines = []
    title = content.get("title", "無題")
    md_lines.append(f"# {title}\n")

    for section in content.get("sections", []):
        md_lines.append(f"## {section.get('title', '')}\n")
        if section.get("body"):
            md_lines.append(f"{section['body']}\n")
        for point in section.get("bullet_points", []):
            md_lines.append(f"- {point}")
        md_lines.append("")

    md_content = "\n".join(md_lines)

    # Markdown → HTML変換
    html_body = markdown.markdown(md_content, extensions=["tables", "fenced_code"])

    # CSSの読み込み
    if css_path and Path(css_path).exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
    else:
        css = DEFAULT_CSS

    html_full = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{css}</style>
</head>
<body>
    <div class="container">
        {html_body}
    </div>
</body>
</html>"""

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_full)

    return output_path


DEFAULT_CSS = """
body {
    font-family: 'Yu Gothic', 'Hiragino Sans', sans-serif;
    line-height: 1.8;
    color: #333;
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px;
    background: #fff;
}
h1 {
    color: #1F4E79;
    border-bottom: 3px solid #1F4E79;
    padding-bottom: 10px;
    margin-bottom: 30px;
}
h2 {
    color: #2E75B6;
    border-bottom: 1px solid #ddd;
    padding-bottom: 5px;
    margin-top: 30px;
}
ul { padding-left: 20px; }
li { margin-bottom: 5px; }
.container { padding: 20px; }
"""
