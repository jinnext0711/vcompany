"""PDF出力エクスポーター"""

from pathlib import Path

from src.output.html_exporter import export_html


def export_pdf(content: dict, output_path: str, css_path: str = None) -> str:
    """コンテンツをPDFファイルとして出力する。

    HTML経由でPDFに変換する。weasyprint が必要。

    Args:
        content: 執筆モジュールの出力（QA済み）
        output_path: 出力ファイルパス
        css_path: カスタムCSSファイルのパス

    Returns:
        str: 出力ファイルのパス
    """
    from weasyprint import HTML

    # まずHTMLを生成（一時ファイル）
    html_path = output_path.replace(".pdf", "_temp.html")
    export_html(content, html_path, css_path)

    # HTML → PDF変換
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    HTML(filename=html_path).write_pdf(output_path)

    # 一時HTMLファイルを削除
    Path(html_path).unlink(missing_ok=True)

    return output_path
