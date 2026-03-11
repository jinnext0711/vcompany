"""自動資料作成パイプライン - 全フェーズを統括する"""

import os
from datetime import datetime
from pathlib import Path

from src.research.collector import collect_materials
from src.outline.generator import generate_outline
from src.writer.composer import compose_content
from src.qa.auto_checker import auto_check
from src.qa.manual_review import present_review_items, format_review_report
from src.output.markdown_exporter import export_markdown
from src.output.html_exporter import export_html
from src.output.pdf_exporter import export_pdf
from src.output.pptx_exporter import export_pptx
from src.design.builder import DesignConfig


class DocumentPipeline:
    """自動資料作成パイプライン。

    全部門が共通で利用できる汎用ツール。
    テーマを入力すると、リサーチ → 構成 → 執筆 → 品質チェック → 出力
    を一気通貫で実行する。
    """

    SUPPORTED_FORMATS = ["markdown", "html", "pdf", "pptx"]

    def __init__(
        self,
        output_dir: str = "output",
        design: DesignConfig = None,
    ):
        self.output_dir = output_dir
        self.design = design or DesignConfig()
        self._state = {}

    def run(
        self,
        theme: str,
        output_formats: list = None,
        additional_context: str = "",
    ) -> dict:
        """パイプラインを実行する。

        Args:
            theme: 資料のテーマ
            output_formats: 出力形式のリスト（省略時は全形式）
            additional_context: 追加コンテキスト

        Returns:
            dict: {
                "outputs": {形式: ファイルパス},
                "auto_fixes": [自動修正リスト],
                "manual_review": レビューレポート文字列,
                "manual_review_items": [確認項目リスト]
            }
        """
        if output_formats is None:
            output_formats = self.SUPPORTED_FORMATS

        # 出力形式のバリデーション
        for fmt in output_formats:
            if fmt not in self.SUPPORTED_FORMATS:
                raise ValueError(
                    f"未対応の出力形式: {fmt}（対応形式: {self.SUPPORTED_FORMATS}）"
                )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"doc_{timestamp}"

        print(f"【Secretary】パイプラインを開始します。テーマ: {theme}")

        # Phase 1: リサーチ
        print("【企画部】Phase 1: リサーチを実施中...")
        research_data = collect_materials(theme, additional_context)
        self._state["research"] = research_data
        print(f"  → 主要ポイント {len(research_data.get('key_points', []))} 件を収集")

        # Phase 2: アウトライン生成（主要形式で生成）
        primary_format = output_formats[0]
        print(f"【企画部】Phase 2: アウトラインを生成中... (形式: {primary_format})")
        outline = generate_outline(research_data, primary_format)
        self._state["outline"] = outline
        print(f"  → {len(outline.get('sections', []))} セクションの構成を作成")

        # Phase 3: 執筆
        print("【広報部】Phase 3: 本文を執筆中...")
        content = compose_content(outline, research_data, primary_format)
        self._state["content"] = content
        print(f"  → {len(content.get('sections', []))} セクションの本文を作成")

        # Phase 5: 品質チェック
        print("【品質管理部】Phase 5: 品質チェックを実施中...")
        qa_result = auto_check(content, primary_format)
        corrected_content = qa_result.get("corrected_content", content)
        auto_fixes = qa_result.get("auto_fixes", [])
        self._state["qa_result"] = qa_result

        if auto_fixes:
            print(f"  → {len(auto_fixes)} 件の自動修正を適用")
        else:
            print("  → 自動修正なし")

        # 手動レビュー項目の確認
        review_items = present_review_items(qa_result)
        review_report = format_review_report(review_items)

        if review_items:
            print(f"  → {len(review_items)} 件のOwner確認項目あり")

        # Phase 7: 出力
        print("【開発部】Phase 7: 資料を出力中...")
        outputs = {}
        output_base = os.path.join(self.output_dir, base_name)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        for fmt in output_formats:
            output_path = f"{output_base}.{_get_extension(fmt)}"
            print(f"  → {fmt} 形式で出力中...")

            if fmt == "markdown":
                outputs[fmt] = export_markdown(corrected_content, output_path)
            elif fmt == "html":
                outputs[fmt] = export_html(corrected_content, output_path)
            elif fmt == "pdf":
                outputs[fmt] = export_pdf(corrected_content, output_path)
            elif fmt == "pptx":
                outputs[fmt] = export_pptx(
                    corrected_content, output_path, self.design
                )

        print("【CEO】パイプライン完了。Ownerへご報告します。")

        return {
            "outputs": outputs,
            "auto_fixes": auto_fixes,
            "manual_review": review_report,
            "manual_review_items": review_items,
        }


def _get_extension(fmt: str) -> str:
    """出力形式からファイル拡張子を返す。"""
    extensions = {
        "markdown": "md",
        "html": "html",
        "pdf": "pdf",
        "pptx": "pptx",
    }
    return extensions.get(fmt, fmt)
