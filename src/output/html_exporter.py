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
/* vCompany デザインルール準拠 CSS
   - Noto Sans JP のみ使用
   - フラットカラー、グラデーション禁止
   - WCAG AA コントラスト比準拠
   - 8pxグリッド基準スペーシング
   - 左揃え（均等揃え禁止）
*/
body {
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 16px;
    font-weight: 400;
    line-height: 1.8;
    color: #2D2D2D;                   /* text: コントラスト比 12.6:1 AAA */
    max-width: 720px;                 /* ≒日本語40文字/行 */
    margin: 0 auto;
    padding: 48px 24px;               /* spacing-09, spacing-06 */
    background: #FFFFFF;
    text-align: left;                 /* 均等揃え禁止 */
}
h1 {
    color: #1A1A2E;                   /* primary: コントラスト比 15.4:1 AAA */
    border-bottom: 2px solid #53868B;
    padding-bottom: 16px;             /* spacing-05 */
    margin-bottom: 48px;              /* spacing-09 */
    margin-top: 0;
    font-size: 32px;
    font-weight: 700;
    line-height: 1.2;
}
h2 {
    color: #1A1A2E;
    border-left: 4px solid #53868B;
    padding-left: 16px;              /* spacing-05 */
    padding-bottom: 4px;             /* spacing-02 */
    margin-top: 48px;                /* spacing-09 */
    margin-bottom: 24px;             /* spacing-06 */
    font-size: 24px;
    font-weight: 700;
    line-height: 1.3;
}
h3 {
    color: #16213E;                  /* secondary */
    margin-top: 32px;               /* spacing-07 */
    margin-bottom: 16px;            /* spacing-05 */
    font-size: 18px;
    font-weight: 500;
    line-height: 1.3;
}
p {
    margin-bottom: 32px;            /* フォントサイズ16px × 2 = 段落間スペース */
    line-height: 1.8;
}
ul {
    padding-left: 24px;             /* spacing-06 */
    list-style: none;
    margin-bottom: 32px;            /* spacing-07 */
}
li {
    margin-bottom: 8px;             /* spacing-03 */
    padding-left: 24px;             /* spacing-06 */
    position: relative;
    line-height: 1.8;
}
li::before {
    content: "—";
    position: absolute;
    left: 0;
    color: #53868B;                 /* highlight */
}
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 32px;            /* spacing-07 */
}
th {
    background: #1A1A2E;            /* primary */
    color: #FFFFFF;
    font-weight: 700;
    padding: 12px 16px;             /* spacing-04, spacing-05 */
    text-align: left;
}
td {
    padding: 12px 16px;
    border-bottom: 1px solid #E0E0E0; /* border */
}
tr:nth-child(even) {
    background: #F5F5F5;            /* light_bg */
}
figcaption, .caption {
    color: #6B6B6B;                 /* light_text: コントラスト比 5.0:1 AA */
    font-size: 12px;
    line-height: 1.5;
    margin-top: 8px;                /* spacing-03 */
}
.container {
    padding: 24px;                  /* spacing-06 */
}
"""
