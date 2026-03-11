"""自動資料作成パイプライン - 全フェーズを統括する

Claude Code方式: 各フェーズの知的作業はClaude Codeが実行し、
ファイル出力のみPythonで処理する。
将来的にAPI方式への切り替えも可能。
"""

import os
from datetime import datetime
from pathlib import Path

from src.output.markdown_exporter import export_markdown
from src.output.html_exporter import export_html
from src.output.pdf_exporter import export_pdf
from src.output.pptx_exporter import export_pptx
from src.design.builder import DesignConfig


SUPPORTED_FORMATS = ["markdown", "html", "pdf", "pptx"]


def generate_document(
    content: dict,
    output_formats: list = None,
    output_dir: str = "output",
    design: DesignConfig = None,
) -> dict:
    """コンテンツデータから各形式のファイルを生成する。

    Claude Codeが作成したコンテンツデータを受け取り、
    指定された形式でファイルを出力する。

    Args:
        content: コンテンツデータ
            {
                "title": "資料タイトル",
                "sections": [
                    {
                        "title": "セクションタイトル",
                        "body": "本文",
                        "bullet_points": ["ポイント1", "ポイント2"],
                        "notes": "スピーカーノート"
                    }
                ]
            }
        output_formats: 出力形式のリスト（省略時はpptxのみ）
        output_dir: 出力先ディレクトリ
        design: デザイン設定（省略時はデフォルト）

    Returns:
        dict: {"outputs": {形式: ファイルパス}}
    """
    if output_formats is None:
        output_formats = ["pptx"]

    if design is None:
        design = DesignConfig()

    for fmt in output_formats:
        if fmt not in SUPPORTED_FORMATS:
            raise ValueError(
                f"未対応の出力形式: {fmt}（対応形式: {SUPPORTED_FORMATS}）"
            )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    title_slug = content.get("title", "doc")[:20].replace(" ", "_")
    base_name = f"{title_slug}_{timestamp}"

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    outputs = {}
    extensions = {"markdown": "md", "html": "html", "pdf": "pdf", "pptx": "pptx"}

    for fmt in output_formats:
        output_path = os.path.join(output_dir, f"{base_name}.{extensions[fmt]}")

        if fmt == "markdown":
            outputs[fmt] = export_markdown(content, output_path)
        elif fmt == "html":
            outputs[fmt] = export_html(content, output_path)
        elif fmt == "pdf":
            outputs[fmt] = export_pdf(content, output_path)
        elif fmt == "pptx":
            outputs[fmt] = export_pptx(content, output_path, design)

    return {"outputs": outputs}
