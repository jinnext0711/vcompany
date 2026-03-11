"""PowerPoint出力エクスポーター"""

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from src.design.builder import DesignConfig


def export_pptx(
    content: dict, output_path: str, design: DesignConfig = None
) -> str:
    """コンテンツをPowerPointファイルとして出力する。

    Args:
        content: 執筆モジュールの出力（QA済み）
        output_path: 出力ファイルパス
        design: デザイン設定（省略時はデフォルト）

    Returns:
        str: 出力ファイルのパス
    """
    if design is None:
        design = DesignConfig()

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    title = content.get("title", "無題")
    sections = content.get("sections", [])

    # タイトルスライド
    _add_title_slide(prs, title, design)

    # 各セクションのスライド
    for section in sections:
        _add_content_slide(prs, section, design)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    prs.save(output_path)

    return output_path


def _add_title_slide(prs: Presentation, title: str, design: DesignConfig):
    """タイトルスライドを追加する。"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 白紙レイアウト

    # 背景色
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*design.get_color_rgb("primary"))

    # タイトルテキスト
    left = Inches(1)
    top = Inches(2.5)
    width = Inches(11.333)
    height = Inches(2)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER


def _add_content_slide(
    prs: Presentation, section: dict, design: DesignConfig
):
    """コンテンツスライドを追加する。"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 白紙レイアウト

    section_title = section.get("title", "")
    body = section.get("body", "")
    bullet_points = section.get("bullet_points", [])
    notes = section.get("notes", "")

    # ヘッダーバー
    from pptx.util import Emu
    header = slide.shapes.add_shape(
        1,  # Rectangle
        Inches(0), Inches(0),
        prs.slide_width, Inches(1.2),
    )
    header.fill.solid()
    header.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("primary"))
    header.line.fill.background()

    # セクションタイトル
    left = Inches(0.8)
    top = Inches(0.15)
    width = Inches(11.733)
    height = Inches(0.9)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = section_title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # 本文エリア
    content_top = Inches(1.6)
    content_left = Inches(0.8)
    content_width = Inches(11.733)
    content_height = Inches(5.4)
    txBox = slide.shapes.add_textbox(
        content_left, content_top, content_width, content_height
    )
    tf = txBox.text_frame
    tf.word_wrap = True

    # 本文テキスト
    if body:
        p = tf.paragraphs[0]
        p.text = body
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(*design.get_color_rgb("text"))
        p.space_after = Pt(12)

    # 箇条書き
    for point in bullet_points:
        p = tf.add_paragraph()
        p.text = f"  {point}"
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(*design.get_color_rgb("text"))
        p.space_before = Pt(6)

    # スピーカーノート
    if notes:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = notes
