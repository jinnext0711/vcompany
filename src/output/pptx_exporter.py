"""PowerPoint出力エクスポーター

デザインルール準拠:
- Noto Sans JP フォント使用（デフォルトフォント禁止）
- フラットカラーのみ（グラデーション禁止）
- アニメーションなし
- 余白を活かしたすっきりしたレイアウト
- 1スライド最大5箇条書き
"""

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from src.design.builder import DesignConfig


def export_pptx(
    content: dict, output_path: str, design: DesignConfig = None
) -> str:
    """コンテンツをPowerPointファイルとして出力する。"""
    if design is None:
        design = DesignConfig()

    layout = design.LAYOUT
    prs = Presentation()
    prs.slide_width = Inches(layout["slide_width"])
    prs.slide_height = Inches(layout["slide_height"])

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
    """タイトルスライド — 中央配置、すっきりしたデザイン。"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 白紙

    # 背景: フラットカラー（グラデーション禁止）
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*design.get_color_rgb("primary"))

    # 上部のアクセントライン
    line = slide.shapes.add_shape(
        1, Inches(2), Inches(2.2), Inches(9.333), Pt(3),
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("highlight"))
    line.line.fill.background()

    # タイトルテキスト
    font_config = design.get_font("title")
    txBox = slide.shapes.add_textbox(
        Inches(2), Inches(2.5), Inches(9.333), Inches(2),
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = font_config["name"]
    p.font.size = Pt(font_config["size"])
    p.font.bold = font_config["bold"]
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.LEFT

    # 下部のアクセントライン
    line2 = slide.shapes.add_shape(
        1, Inches(2), Inches(4.8), Inches(9.333), Pt(3),
    )
    line2.fill.solid()
    line2.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("highlight"))
    line2.line.fill.background()


def _add_content_slide(
    prs: Presentation, section: dict, design: DesignConfig
):
    """コンテンツスライド — 余白を活かしたすっきりしたレイアウト。"""
    layout = design.LAYOUT
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 白紙

    section_title = section.get("title", "")
    body = section.get("body", "")
    bullet_points = section.get("bullet_points", [])
    notes = section.get("notes", "")

    margin_left = layout["margin_left"]
    margin_top = layout["margin_top"]
    content_width = layout["slide_width"] - margin_left - layout["margin_right"]

    # 左サイドのアクセントバー（細いライン）
    bar = slide.shapes.add_shape(
        1,
        Inches(0), Inches(0),
        Pt(6), prs.slide_height,
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("highlight"))
    bar.line.fill.background()

    # セクションタイトル
    heading_font = design.get_font("heading")
    txBox = slide.shapes.add_textbox(
        Inches(margin_left), Inches(margin_top),
        Inches(content_width), Inches(0.8),
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = section_title
    p.font.name = heading_font["name"]
    p.font.size = Pt(heading_font["size"])
    p.font.bold = heading_font["bold"]
    p.font.color.rgb = RGBColor(*design.get_color_rgb("primary"))

    # タイトル下の区切り線
    separator_top = margin_top + 0.9
    sep = slide.shapes.add_shape(
        1,
        Inches(margin_left), Inches(separator_top),
        Inches(3), Pt(2),
    )
    sep.fill.solid()
    sep.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("highlight"))
    sep.line.fill.background()

    # 本文エリア
    body_font = design.get_font("body")
    content_top = separator_top + 0.4

    if body:
        txBox = slide.shapes.add_textbox(
            Inches(margin_left), Inches(content_top),
            Inches(content_width), Inches(1.0),
        )
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = body
        p.font.name = body_font["name"]
        p.font.size = Pt(body_font["size"])
        p.font.color.rgb = RGBColor(*design.get_color_rgb("text"))
        p.space_after = Pt(12)
        content_top += 1.2

    # 箇条書き（最大5項目）
    if bullet_points:
        limited_points = bullet_points[:layout["max_bullet_items"]]
        txBox = slide.shapes.add_textbox(
            Inches(margin_left + 0.2), Inches(content_top),
            Inches(content_width - 0.2), Inches(4.0),
        )
        tf = txBox.text_frame
        tf.word_wrap = True

        for i, point in enumerate(limited_points):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = f"—  {point}"
            p.font.name = body_font["name"]
            p.font.size = Pt(body_font["size"])
            p.font.color.rgb = RGBColor(*design.get_color_rgb("text"))
            p.space_before = Pt(10)
            p.space_after = Pt(10)

    # スピーカーノート
    if notes:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = notes
