"""PowerPoint出力エクスポーター

デザインルール準拠:
- Noto Sans JP フォント使用（デフォルトフォント禁止）
- フラットカラーのみ（グラデーション禁止）
- アニメーションなし
- 余白を活かしたすっきりしたレイアウト（8pxグリッド基準）
- 1スライド最大5箇条書き、本文最大3行
- WCAG AA コントラスト比準拠
- テキスト左揃え（均等揃え禁止）
- 行間: フォントサイズの1.2〜1.5倍

対応レイアウト:
- heading_bullets: 見出し + 箇条書き
- table: 見出し + テーブル
- flow: フロー図
- kpi: 数値ハイライト
- summary: まとめスライド
"""

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
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

    _add_title_slide(prs, title, design)

    for section in sections:
        slide_layout = section.get("layout", "heading_bullets")
        if slide_layout == "table":
            _add_table_slide(prs, section, design)
        elif slide_layout == "flow":
            _add_flow_slide(prs, section, design)
        elif slide_layout == "kpi":
            _add_kpi_slide(prs, section, design)
        elif slide_layout == "summary":
            _add_summary_slide(prs, section, design)
        else:
            _add_content_slide(prs, section, design)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    prs.save(output_path)

    return output_path


def _add_slide_accent_bar(slide, prs, design):
    """左サイドのアクセントバー（全コンテンツスライド共通）。"""
    bar = slide.shapes.add_shape(
        1, Inches(0), Inches(0), Pt(6), prs.slide_height,
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("highlight"))
    bar.line.fill.background()


def _add_slide_heading(slide, title, design, layout):
    """スライド見出し（全コンテンツスライド共通）。返り値はコンテンツ開始Y座標。"""
    margin_left = layout["margin_left"]
    margin_top = layout["margin_top"]
    content_width = layout["slide_width"] - margin_left - layout["margin_right"]

    heading_font = design.get_font("heading")
    txBox = slide.shapes.add_textbox(
        Inches(margin_left), Inches(margin_top),
        Inches(content_width), Inches(0.8),
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = heading_font["name"]
    p.font.size = Pt(heading_font["size"])
    p.font.bold = heading_font["bold"]
    p.font.color.rgb = RGBColor(*design.get_color_rgb("primary"))

    separator_top = margin_top + 0.9
    sep = slide.shapes.add_shape(
        1, Inches(margin_left), Inches(separator_top),
        Inches(3), Pt(2),
    )
    sep.fill.solid()
    sep.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("highlight"))
    sep.line.fill.background()

    return separator_top + 0.5


def _add_title_slide(prs, title, design):
    """タイトルスライド。"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*design.get_color_rgb("primary"))

    line = slide.shapes.add_shape(
        1, Inches(2), Inches(2.2), Inches(9.333), Pt(3),
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("highlight"))
    line.line.fill.background()

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

    line2 = slide.shapes.add_shape(
        1, Inches(2), Inches(4.8), Inches(9.333), Pt(3),
    )
    line2.fill.solid()
    line2.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("highlight"))
    line2.line.fill.background()


def _add_content_slide(prs, section, design):
    """見出し + 箇条書きスライド。"""
    layout = design.LAYOUT
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_slide_accent_bar(slide, prs, design)

    content_top = _add_slide_heading(slide, section.get("title", ""), design, layout)

    margin_left = layout["margin_left"]
    content_width = layout["slide_width"] - margin_left - layout["margin_right"]
    body_font = design.get_font("body")
    body = section.get("body", "")
    bullet_points = section.get("bullet_points", [])

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

    if bullet_points:
        limited = bullet_points[:layout["max_bullet_items"]]
        txBox = slide.shapes.add_textbox(
            Inches(margin_left + 0.2), Inches(content_top),
            Inches(content_width - 0.2), Inches(4.0),
        )
        tf = txBox.text_frame
        tf.word_wrap = True
        for i, point in enumerate(limited):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = f"—  {point}"
            p.font.name = body_font["name"]
            p.font.size = Pt(body_font["size"])
            p.font.color.rgb = RGBColor(*design.get_color_rgb("text"))
            p.space_before = Pt(10)
            p.space_after = Pt(10)

    if section.get("notes"):
        slide.notes_slide.notes_text_frame.text = section["notes"]


def _add_table_slide(prs, section, design):
    """見出し + テーブルスライド。"""
    layout = design.LAYOUT
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_slide_accent_bar(slide, prs, design)

    content_top = _add_slide_heading(slide, section.get("title", ""), design, layout)

    table_data = section.get("table", {})
    headers = table_data.get("headers", [])
    rows = table_data.get("rows", [])

    if not headers:
        return

    margin_left = layout["margin_left"]
    content_width = layout["slide_width"] - margin_left - layout["margin_right"]
    num_rows = len(rows) + 1
    num_cols = len(headers)
    row_height = 0.5
    table_height = row_height * num_rows

    table_shape = slide.shapes.add_table(
        num_rows, num_cols,
        Inches(margin_left), Inches(content_top),
        Inches(content_width), Inches(table_height),
    )
    table = table_shape.table

    body_font = design.get_font("body")

    # ヘッダー行
    for col_idx, header in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("primary"))
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.name = body_font["name"]
            paragraph.font.size = Pt(14)
            paragraph.font.bold = True
            paragraph.font.color.rgb = RGBColor(255, 255, 255)

    # データ行
    for row_idx, row_data in enumerate(rows):
        for col_idx, cell_text in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = cell_text
            if row_idx % 2 == 1:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("light_bg"))
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.name = body_font["name"]
                paragraph.font.size = Pt(14)
                paragraph.font.color.rgb = RGBColor(*design.get_color_rgb("text"))

    if section.get("notes"):
        slide.notes_slide.notes_text_frame.text = section["notes"]


def _add_flow_slide(prs, section, design):
    """フロー図スライド。"""
    layout = design.LAYOUT
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_slide_accent_bar(slide, prs, design)

    content_top = _add_slide_heading(slide, section.get("title", ""), design, layout)

    steps = section.get("flow_steps", [])
    descriptions = section.get("flow_descriptions", [])

    if not steps:
        return

    margin_left = layout["margin_left"]
    content_width = layout["slide_width"] - margin_left - layout["margin_right"]
    num_steps = len(steps)
    step_width = content_width / num_steps
    box_width = step_width * 0.7
    box_height = 1.2
    arrow_width = step_width * 0.3

    body_font = design.get_font("body")
    heading_font = design.get_font("subheading")

    y_center = content_top + 0.8

    for i, step in enumerate(steps):
        x = margin_left + (step_width * i) + (step_width - box_width) / 2

        # ステップボックス
        box = slide.shapes.add_shape(
            5,  # Rounded Rectangle
            Inches(x), Inches(y_center),
            Inches(box_width), Inches(box_height),
        )
        box.fill.solid()
        if i == 0:
            box.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("primary"))
            text_color = RGBColor(255, 255, 255)
        else:
            box.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("light_bg"))
            text_color = RGBColor(*design.get_color_rgb("primary"))
        box.line.color.rgb = RGBColor(*design.get_color_rgb("highlight"))
        box.line.width = Pt(1.5)

        # ステップ番号 + 名前
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{i + 1}. {step}"
        p.font.name = heading_font["name"]
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = text_color
        p.alignment = PP_ALIGN.CENTER

        # 説明テキスト
        if i < len(descriptions):
            desc_box = slide.shapes.add_textbox(
                Inches(x - 0.1), Inches(y_center + box_height + 0.3),
                Inches(box_width + 0.2), Inches(1.2),
            )
            tf = desc_box.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = descriptions[i]
            p.font.name = body_font["name"]
            p.font.size = Pt(12)
            p.font.color.rgb = RGBColor(*design.get_color_rgb("text"))
            p.alignment = PP_ALIGN.CENTER

        # 矢印（最後のステップ以外）
        if i < num_steps - 1:
            arrow_x = x + box_width
            arrow_y = y_center + box_height / 2
            arrow = slide.shapes.add_shape(
                1,  # Rectangle as arrow line
                Inches(arrow_x + 0.05), Inches(arrow_y),
                Inches(arrow_width - 0.1), Pt(3),
            )
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("highlight"))
            arrow.line.fill.background()

            # 矢印の三角
            tri = slide.shapes.add_shape(
                7,  # Triangle (right-pointing via rotation isn't ideal, use chevron)
                Inches(arrow_x + arrow_width - 0.2), Inches(arrow_y - 0.08),
                Inches(0.16), Inches(0.2),
            )
            tri.fill.solid()
            tri.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("highlight"))
            tri.line.fill.background()
            tri.rotation = 90.0

    if section.get("notes"):
        slide.notes_slide.notes_text_frame.text = section["notes"]


def _add_kpi_slide(prs, section, design):
    """数値ハイライトスライド（KPI表示）。"""
    layout = design.LAYOUT
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_slide_accent_bar(slide, prs, design)

    content_top = _add_slide_heading(slide, section.get("title", ""), design, layout)

    kpi_items = section.get("kpi_items", [])

    if not kpi_items:
        return

    margin_left = layout["margin_left"]
    content_width = layout["slide_width"] - margin_left - layout["margin_right"]
    num_items = len(kpi_items)
    item_width = content_width / num_items
    card_width = item_width * 0.85
    card_height = 2.5

    data_font = design.get_font("data")
    body_font = design.get_font("body")

    y = content_top + 0.5

    for i, item in enumerate(kpi_items):
        x = margin_left + (item_width * i) + (item_width - card_width) / 2

        # カード背景
        card = slide.shapes.add_shape(
            5,  # Rounded Rectangle
            Inches(x), Inches(y),
            Inches(card_width), Inches(card_height),
        )
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("light_bg"))
        card.line.color.rgb = RGBColor(*design.get_color_rgb("border"))
        card.line.width = Pt(1)

        # 数値
        val_box = slide.shapes.add_textbox(
            Inches(x), Inches(y + 0.4),
            Inches(card_width), Inches(1.2),
        )
        tf = val_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = item.get("value", "")
        p.font.name = data_font["name"]
        p.font.size = Pt(data_font["size"])
        p.font.bold = data_font["bold"]
        p.font.color.rgb = RGBColor(*design.get_color_rgb("primary"))
        p.alignment = PP_ALIGN.CENTER

        # ラベル
        label_box = slide.shapes.add_textbox(
            Inches(x + 0.2), Inches(y + 1.5),
            Inches(card_width - 0.4), Inches(0.8),
        )
        tf = label_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = item.get("label", "")
        p.font.name = body_font["name"]
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(*design.get_color_rgb("text"))
        p.alignment = PP_ALIGN.CENTER

    if section.get("notes"):
        slide.notes_slide.notes_text_frame.text = section["notes"]


def _add_summary_slide(prs, section, design):
    """まとめスライド — キーメッセージを強調表示。"""
    layout = design.LAYOUT
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 背景を Primary に
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*design.get_color_rgb("primary"))

    margin_left = layout["margin_left"]
    content_width = layout["slide_width"] - margin_left - layout["margin_right"]

    heading_font = design.get_font("heading")
    body_font = design.get_font("body")

    # タイトル
    txBox = slide.shapes.add_textbox(
        Inches(margin_left), Inches(0.8),
        Inches(content_width), Inches(1.0),
    )
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = section.get("title", "まとめ")
    p.font.name = heading_font["name"]
    p.font.size = Pt(heading_font["size"])
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # 区切り線
    sep = slide.shapes.add_shape(
        1, Inches(margin_left), Inches(1.8),
        Inches(3), Pt(3),
    )
    sep.fill.solid()
    sep.fill.fore_color.rgb = RGBColor(*design.get_color_rgb("highlight"))
    sep.line.fill.background()

    # キーメッセージ
    bullet_points = section.get("bullet_points", [])
    y = 2.4

    for i, point in enumerate(bullet_points[:3]):
        # 番号
        num_box = slide.shapes.add_textbox(
            Inches(margin_left), Inches(y),
            Inches(0.6), Inches(0.6),
        )
        tf = num_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"{i + 1}"
        p.font.name = body_font["name"]
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = RGBColor(*design.get_color_rgb("highlight"))

        # テキスト
        msg_box = slide.shapes.add_textbox(
            Inches(margin_left + 0.7), Inches(y + 0.05),
            Inches(content_width - 0.7), Inches(0.6),
        )
        tf = msg_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = point
        p.font.name = body_font["name"]
        p.font.size = Pt(18)
        p.font.color.rgb = RGBColor(255, 255, 255)

        y += 1.2

    if section.get("notes"):
        slide.notes_slide.notes_text_frame.text = section["notes"]
