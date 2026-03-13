"""自動資料作成パイプライン — 全フェーズを統括する

Claude Code方式: 各フェーズの知的作業はClaude Codeが実行し、
各モジュールはプロンプト生成・データ検証・出力整形を担当する。

パイプラインフロー:
  Phase 1: リサーチ → research/collector.py
  Phase 2: アウトライン → outline/generator.py
  Phase 3: 執筆 → writer/composer.py
  Phase 4: デザイン → design/builder.py (既存)
  Phase 5: QA → qa/auto_checker.py
  Phase 6: 出力 → output/pptx_exporter.py (既存)

各フェーズは以下のAPIを提供:
  - get_xxx_prompt(): Claude Codeが実行するためのプロンプト
  - validate_xxx(): 出力データの検証
  - create_xxx(): データ構造の生成

中間成果物は output/ に JSON として保存され、中断・再開が可能。
"""

import os
import json
from datetime import datetime
from pathlib import Path

from src.research.collector import (
    get_research_prompt, create_research_data, validate_research,
)
from src.outline.generator import (
    get_outline_prompt, create_outline, validate_outline,
)
from src.writer.composer import (
    get_writer_prompt, create_content, validate_content,
    evaluate_slides, get_refinement_prompt,
)
from src.qa.auto_checker import run_qa, format_qa_report
from src.qa.visual_validator import run_visual_validation, format_visual_report
from src.design.builder import DesignConfig
from src.output.pptx_exporter import export_pptx
from src.output.markdown_exporter import export_markdown
from src.output.html_exporter import export_html
from src.output.pdf_exporter import export_pdf


SUPPORTED_FORMATS = ["markdown", "html", "pdf", "pptx"]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# フェーズ別API（Claude Codeが順次呼び出す）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def phase1_prompt(theme, audience="経営層", objective=None):
    """Phase 1: リサーチプロンプトを生成する。"""
    if objective is None:
        objective = f"「{theme}」の全体像を理解し、意思決定に必要な情報を提供する"
    return get_research_prompt(theme, audience, objective)


def phase1_validate(research_data, output_dir="output"):
    """Phase 1: リサーチデータを検証し、中間ファイルに保存する。"""
    is_valid, issues = validate_research(research_data)
    if output_dir:
        _save_intermediate(research_data, output_dir, "phase1_research.json")
    return is_valid, issues


def phase2_prompt(research_data):
    """Phase 2: アウトラインプロンプトを生成する。"""
    return get_outline_prompt(research_data)


def phase2_validate(outline_data, output_dir="output"):
    """Phase 2: アウトラインデータを検証し、中間ファイルに保存する。"""
    is_valid, issues = validate_outline(outline_data)
    if output_dir:
        _save_intermediate(outline_data, output_dir, "phase2_outline.json")
    return is_valid, issues


def phase3_prompt(outline_data, research_data):
    """Phase 3: ライタープロンプトを生成する。"""
    return get_writer_prompt(outline_data, research_data)


def phase3_validate(content_data, output_dir="output"):
    """Phase 3: コンテンツデータを検証し、中間ファイルに保存する。"""
    is_valid, issues = validate_content(content_data)
    if output_dir:
        _save_intermediate(content_data, output_dir, "phase3_content.json")
    return is_valid, issues


def phase3_evaluate(content_data):
    """Phase 3 評価: コンテンツの各スライド品質を評価する。

    Returns:
        dict: スライド評価結果（slide_evaluations, weak_slide_indices,
              average_score, overall_grade）
    """
    return evaluate_slides(content_data)


def phase3_refine_prompt(content_data, evaluation, research_data):
    """Phase 3 改善: 弱いスライドの改善プロンプトを生成する。

    Args:
        content_data: 現在のコンテンツデータ
        evaluation: phase3_evaluate() の返り値
        research_data: Phase 1 のリサーチデータ

    Returns:
        str: 改善プロンプト文字列
    """
    return get_refinement_prompt(content_data, evaluation, research_data)


def phase5_check(content_data, output_dir="output"):
    """Phase 5: QAチェックを実行し、修正済みコンテンツを返す。"""
    qa_result = run_qa(content_data)
    if output_dir:
        # QAレポートを保存
        report = {
            "qa_report": qa_result["qa_report"],
            "auto_fixes": qa_result["auto_fixes"],
            "summary": qa_result["summary"],
            "manual_review_items": qa_result["manual_review_items"],
        }
        _save_intermediate(report, output_dir, "phase5_qa_report.json")
        # 修正済みコンテンツも保存
        _save_intermediate(
            qa_result["corrected_content"], output_dir, "phase5_corrected_content.json"
        )
    return qa_result


def phase6_export(content_data, output_dir="output", output_formats=None,
                  design=None):
    """Phase 6: 出力ファイルを生成する。"""
    if output_formats is None:
        output_formats = ["pptx"]
    if design is None:
        design = DesignConfig()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    title_slug = content_data.get("title", "doc")[:20].replace(" ", "_")
    base_name = f"{title_slug}_{timestamp}"

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    outputs = {}
    extensions = {"markdown": "md", "html": "html", "pdf": "pdf", "pptx": "pptx"}

    for fmt in output_formats:
        if fmt not in SUPPORTED_FORMATS:
            raise ValueError(f"未対応の出力形式: {fmt}")
        output_path = os.path.join(output_dir, f"{base_name}.{extensions[fmt]}")
        if fmt == "markdown":
            outputs[fmt] = export_markdown(content_data, output_path)
        elif fmt == "html":
            outputs[fmt] = export_html(content_data, output_path)
        elif fmt == "pdf":
            outputs[fmt] = export_pdf(content_data, output_path)
        elif fmt == "pptx":
            outputs[fmt] = export_pptx(content_data, output_path, design)

    return outputs


def phase6_5_visual_check(pptx_path, design=None, output_dir="output"):
    """Phase 6.5: 視覚品質検証 — PPTXレンダリング結果を再読み込みしてチェック。

    Phase 6（PPTX出力）の後に実行し、レンダリング結果の視覚的品質を検証する。
    QA（Phase 5）はJSON構造のみチェックするため、テキスト重複・溢れ・空スライド等の
    視覚的問題はこのフェーズで初めて検出される。

    Returns:
        dict: issues, summary, per_slide, report_text
    """
    result = run_visual_validation(pptx_path, design)
    report_text = format_visual_report(result)

    if output_dir:
        _save_intermediate({
            "pptx_path": pptx_path,
            "summary": result["summary"],
            "issues": result["issues"],
            "report": report_text,
        }, output_dir, "phase6_5_visual_report.json")

    result["report_text"] = report_text
    return result


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# レガシー互換（既存の generate_document）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_document(content, output_formats=None, output_dir="output",
                      design=None):
    """コンテンツデータから各形式のファイルを生成する（レガシー互換）。"""
    outputs = phase6_export(content, output_dir, output_formats, design)
    return {"outputs": outputs}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 中間ファイル管理
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _save_intermediate(data, output_dir, filename):
    """中間成果物をJSONファイルとして保存する。"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def load_intermediate(output_dir, filename):
    """中間成果物をJSONファイルから読み込む。"""
    path = os.path.join(output_dir, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
