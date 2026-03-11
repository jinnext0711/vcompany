"""PowerPoint出力エクスポーター — コンサルティング品質

3層構造: ヘッダー（アクションタイトル）+ ボディ（図表/構造化テキスト）+ フッター（出典）
1-1-1ルール: 1スライド → 1メッセージ → 1支持構造
配色: 70%ベース / 25%メイン / 5%アクセント
"""

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from src.design.builder import DesignConfig

# レイアウト定数
SLIDE_W = 13.333
SLIDE_H = 7.5
MARGIN_L = 0.8
MARGIN_R = 0.8
MARGIN_T = 0.6
BODY_TOP = 1.6
BODY_BOTTOM = 6.8
FOOTER_TOP = 7.0
CONTENT_W = SLIDE_W - MARGIN_L - MARGIN_R


def export_pptx(content, output_path, design=None):
    if design is None:
        design = DesignConfig()

    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)

    _add_title_slide(prs, content, design)

    for section in content.get("sections", []):
        layout = section.get("layout", "structured_text")
        if layout == "table":
            _add_table_slide(prs, section, design)
        elif layout == "flow":
            _add_flow_slide(prs, section, design)
        elif layout == "kpi":
            _add_kpi_slide(prs, section, design)
        elif layout == "summary":
            _add_summary_slide(prs, section, design)
        elif layout == "two_column":
            _add_two_column_slide(prs, section, design)
        else:
            _add_structured_text_slide(prs, section, design)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    prs.save(output_path)
    return output_path


# ──────────────────────────────────────────────
# 共通パーツ
# ──────────────────────────────────────────────

def _c(design, key):
    return RGBColor(*design.get_color_rgb(key))

WHITE = RGBColor(255, 255, 255)

def _add_action_title(slide, title_text, design):
    """ヘッダー: アクションタイトル（主張文）。"""
    # 背景バー
    bar = slide.shapes.add_shape(
        1, Inches(0), Inches(0), Inches(SLIDE_W), Inches(1.3),
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = _c(design, "primary")
    bar.line.fill.background()

    # アクセントライン
    line = slide.shapes.add_shape(
        1, Inches(0), Inches(1.3), Inches(SLIDE_W), Pt(3),
    )
    line.fill.solid()
    line.fill.fore_color.rgb = _c(design, "highlight")
    line.line.fill.background()

    # タイトルテキスト
    txBox = slide.shapes.add_textbox(
        Inches(MARGIN_L), Inches(0.25), Inches(CONTENT_W), Inches(0.95),
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Noto Sans JP"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.LEFT


def _add_footer(slide, source_text, design, page_num=None):
    """フッター: 出典・ページ番号。"""
    # 区切り線
    line = slide.shapes.add_shape(
        1, Inches(MARGIN_L), Inches(FOOTER_TOP),
        Inches(CONTENT_W), Pt(0.75),
    )
    line.fill.solid()
    line.fill.fore_color.rgb = _c(design, "border")
    line.line.fill.background()

    # 出典テキスト
    if source_text:
        txBox = slide.shapes.add_textbox(
            Inches(MARGIN_L), Inches(FOOTER_TOP + 0.05),
            Inches(CONTENT_W), Inches(0.35),
        )
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"出典: {source_text}"
        p.font.name = "Noto Sans JP"
        p.font.size = Pt(9)
        p.font.color.rgb = _c(design, "light_text")


def _add_left_accent(slide, design):
    """左サイドの細いアクセントバー。"""
    bar = slide.shapes.add_shape(
        1, Inches(0), Inches(1.35), Pt(4), Inches(SLIDE_H - 1.35),
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = _c(design, "highlight")
    bar.line.fill.background()


# ──────────────────────────────────────────────
# タイトルスライド
# ──────────────────────────────────────────────

def _add_title_slide(prs, content, design):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = _c(design, "primary")

    # アクセントライン上
    _shape_line(slide, 1.5, 2.6, 10.333, design)

    # タイトル
    _text_box(slide, 1.5, 2.8, 10.333, 1.5,
              content.get("title", ""), "Noto Sans JP", 40, True, WHITE, PP_ALIGN.LEFT)

    # サブタイトル
    subtitle = content.get("subtitle", "")
    if subtitle:
        _text_box(slide, 1.5, 4.4, 10.333, 0.8,
                  subtitle, "Noto Sans JP", 18, False, _c(design, "highlight"), PP_ALIGN.LEFT)

    # アクセントライン下
    _shape_line(slide, 1.5, 5.4, 10.333, design)


# ──────────────────────────────────────────────
# 構造化テキストスライド（太字KW + 補足）
# ──────────────────────────────────────────────

def _add_structured_text_slide(prs, section, design):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_left_accent(slide, design)
    _add_action_title(slide, section.get("title", ""), design)

    items = section.get("structured_items", [])
    y = BODY_TOP + 0.2
    item_height = min(1.4, (BODY_BOTTOM - BODY_TOP - 0.4) / max(len(items), 1))

    for item in items[:3]:
        # キーワードカード背景
        card = slide.shapes.add_shape(
            5, Inches(MARGIN_L), Inches(y),
            Inches(CONTENT_W), Inches(item_height - 0.15),
        )
        card.fill.solid()
        card.fill.fore_color.rgb = _c(design, "light_bg")
        card.line.fill.background()

        # キーワード（太字）
        _text_box(slide, MARGIN_L + 0.3, y + 0.12, 3.5, 0.5,
                  item.get("keyword", ""), "Noto Sans JP", 16, True,
                  _c(design, "primary"), PP_ALIGN.LEFT)

        # 詳細テキスト
        _text_box(slide, MARGIN_L + 4.0, y + 0.12, CONTENT_W - 4.3, 0.9,
                  item.get("detail", ""), "Noto Sans JP", 13, False,
                  _c(design, "text"), PP_ALIGN.LEFT)

        y += item_height

    _add_footer(slide, section.get("source", ""), design)
    if section.get("notes"):
        slide.notes_slide.notes_text_frame.text = section["notes"]


# ──────────────────────────────────────────────
# テーブルスライド
# ──────────────────────────────────────────────

def _add_table_slide(prs, section, design):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_left_accent(slide, design)
    _add_action_title(slide, section.get("title", ""), design)

    table_data = section.get("table", {})
    headers = table_data.get("headers", [])
    rows = table_data.get("rows", [])
    if not headers:
        return

    num_rows = len(rows) + 1
    num_cols = len(headers)
    table_height = min(0.45 * num_rows, BODY_BOTTOM - BODY_TOP - 0.3)

    shape = slide.shapes.add_table(
        num_rows, num_cols,
        Inches(MARGIN_L), Inches(BODY_TOP + 0.1),
        Inches(CONTENT_W), Inches(table_height),
    )
    table = shape.table

    # ヘッダー
    for ci, h in enumerate(headers):
        cell = table.cell(0, ci)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = _c(design, "primary")
        _style_cell(cell, 12, True, WHITE)

    # データ
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = table.cell(ri + 1, ci)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = (
                _c(design, "light_bg") if ri % 2 == 1
                else RGBColor(255, 255, 255)
            )
            bold = (ci == 0)
            _style_cell(cell, 11, bold, _c(design, "text"))

    _add_footer(slide, section.get("source", ""), design)
    if section.get("notes"):
        slide.notes_slide.notes_text_frame.text = section["notes"]


# ──────────────────────────────────────────────
# フロー図スライド
# ──────────────────────────────────────────────

def _add_flow_slide(prs, section, design):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_left_accent(slide, design)
    _add_action_title(slide, section.get("title", ""), design)

    steps = section.get("flow_steps", [])
    descs = section.get("flow_descriptions", [])
    if not steps:
        return

    n = len(steps)
    total_w = CONTENT_W
    box_w = total_w * 0.18
    gap = (total_w - box_w * n) / max(n - 1, 1)
    box_h = 1.0
    y = BODY_TOP + 0.8

    for i, step in enumerate(steps):
        x = MARGIN_L + i * (box_w + gap)

        # ステップ番号円
        circle = slide.shapes.add_shape(
            9,  # Oval
            Inches(x + box_w / 2 - 0.25), Inches(y - 0.6),
            Inches(0.5), Inches(0.5),
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = _c(design, "highlight")
        circle.line.fill.background()
        _shape_text(circle, str(i + 1), 14, True, WHITE)

        # ステップボックス
        box = slide.shapes.add_shape(
            5, Inches(x), Inches(y),
            Inches(box_w), Inches(box_h),
        )
        box.fill.solid()
        box.fill.fore_color.rgb = _c(design, "primary") if i == 0 else _c(design, "light_bg")
        box.line.color.rgb = _c(design, "border")
        box.line.width = Pt(1)
        text_c = WHITE if i == 0 else _c(design, "primary")
        _shape_text(box, step, 16, True, text_c)

        # 説明
        if i < len(descs):
            _text_box(slide, x - 0.1, y + box_h + 0.25, box_w + 0.2, 1.0,
                      descs[i], "Noto Sans JP", 11, False,
                      _c(design, "text"), PP_ALIGN.CENTER)

        # 矢印線
        if i < n - 1:
            ax = x + box_w + 0.05
            aw = gap - 0.1
            ay = y + box_h / 2
            arrow_line = slide.shapes.add_shape(
                1, Inches(ax), Inches(ay), Inches(aw), Pt(2),
            )
            arrow_line.fill.solid()
            arrow_line.fill.fore_color.rgb = _c(design, "highlight")
            arrow_line.line.fill.background()
            # 矢印ヘッド
            tri = slide.shapes.add_shape(
                7, Inches(ax + aw - 0.05), Inches(ay - 0.07),
                Inches(0.14), Inches(0.16),
            )
            tri.fill.solid()
            tri.fill.fore_color.rgb = _c(design, "highlight")
            tri.line.fill.background()
            tri.rotation = 90.0

    _add_footer(slide, section.get("source", ""), design)
    if section.get("notes"):
        slide.notes_slide.notes_text_frame.text = section["notes"]


# ──────────────────────────────────────────────
# KPIスライド
# ──────────────────────────────────────────────

def _add_kpi_slide(prs, section, design):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_left_accent(slide, design)
    _add_action_title(slide, section.get("title", ""), design)

    items = section.get("kpi_items", [])
    if not items:
        return

    n = len(items)
    card_w = CONTENT_W * 0.28
    total_cards_w = card_w * n
    gap = (CONTENT_W - total_cards_w) / max(n + 1, 2)
    card_h = 3.0
    y = BODY_TOP + 0.6

    for i, item in enumerate(items):
        x = MARGIN_L + gap + i * (card_w + gap)

        # カード
        card = slide.shapes.add_shape(
            5, Inches(x), Inches(y),
            Inches(card_w), Inches(card_h),
        )
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card.line.color.rgb = _c(design, "border")
        card.line.width = Pt(1)

        # 上部アクセントバー
        top_bar = slide.shapes.add_shape(
            1, Inches(x), Inches(y),
            Inches(card_w), Pt(4),
        )
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = _c(design, "highlight")
        top_bar.line.fill.background()

        # 数値
        _text_box(slide, x, y + 0.5, card_w, 1.2,
                  item.get("value", ""), "Noto Sans JP", 44, True,
                  _c(design, "primary"), PP_ALIGN.CENTER)

        # ラベル
        _text_box(slide, x + 0.2, y + 1.8, card_w - 0.4, 1.0,
                  item.get("label", ""), "Noto Sans JP", 12, False,
                  _c(design, "text"), PP_ALIGN.CENTER)

    _add_footer(slide, section.get("source", ""), design)
    if section.get("notes"):
        slide.notes_slide.notes_text_frame.text = section["notes"]


# ──────────────────────────────────────────────
# 2カラムスライド
# ──────────────────────────────────────────────

def _add_two_column_slide(prs, section, design):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_left_accent(slide, design)
    _add_action_title(slide, section.get("title", ""), design)

    col_w = CONTENT_W / 2 - 0.3
    y = BODY_TOP + 0.1

    for col_idx, (col_key, x_offset) in enumerate([
        ("left_column", MARGIN_L),
        ("right_column", MARGIN_L + col_w + 0.6),
    ]):
        col = section.get(col_key, {})
        heading = col.get("heading", "")
        items = col.get("items", [])

        # カラム背景
        bg = slide.shapes.add_shape(
            5, Inches(x_offset), Inches(y),
            Inches(col_w), Inches(BODY_BOTTOM - BODY_TOP - 0.2),
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = _c(design, "light_bg")
        bg.line.fill.background()

        # カラム見出し
        heading_bar = slide.shapes.add_shape(
            1, Inches(x_offset), Inches(y),
            Inches(col_w), Inches(0.55),
        )
        heading_bar.fill.solid()
        heading_bar.fill.fore_color.rgb = _c(design, "primary")
        heading_bar.line.fill.background()
        _text_box(slide, x_offset + 0.2, y + 0.08, col_w - 0.4, 0.4,
                  heading, "Noto Sans JP", 16, True, WHITE, PP_ALIGN.LEFT)

        # カラムアイテム
        iy = y + 0.75
        for item_text in items[:5]:
            _text_box(slide, x_offset + 0.3, iy, col_w - 0.6, 0.5,
                      f"—  {item_text}", "Noto Sans JP", 13, False,
                      _c(design, "text"), PP_ALIGN.LEFT)
            iy += 0.55

    _add_footer(slide, section.get("source", ""), design)
    if section.get("notes"):
        slide.notes_slide.notes_text_frame.text = section["notes"]


# ──────────────────────────────────────────────
# まとめスライド
# ──────────────────────────────────────────────

def _add_summary_slide(prs, section, design):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = _c(design, "primary")

    # タイトル
    _text_box(slide, MARGIN_L, 0.6, CONTENT_W, 0.8,
              section.get("title", "まとめ"), "Noto Sans JP", 28, True,
              WHITE, PP_ALIGN.LEFT)

    # 区切り線
    _shape_line(slide, MARGIN_L, 1.5, 4, design)

    points = section.get("bullet_points", [])
    y = 2.2

    for i, point in enumerate(points[:3]):
        # 番号円
        circle = slide.shapes.add_shape(
            9, Inches(MARGIN_L), Inches(y),
            Inches(0.5), Inches(0.5),
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = _c(design, "highlight")
        circle.line.fill.background()
        _shape_text(circle, str(i + 1), 16, True, WHITE)

        # メッセージ
        _text_box(slide, MARGIN_L + 0.7, y + 0.02, CONTENT_W - 0.9, 0.7,
                  point, "Noto Sans JP", 16, False, WHITE, PP_ALIGN.LEFT)

        y += 1.3

    if section.get("notes"):
        slide.notes_slide.notes_text_frame.text = section["notes"]


# ──────────────────────────────────────────────
# ヘルパー関数
# ──────────────────────────────────────────────

def _text_box(slide, left, top, width, height, text, font_name, size, bold, color, align):
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height),
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = font_name
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    return txBox


def _shape_line(slide, left, top, width, design):
    line = slide.shapes.add_shape(
        1, Inches(left), Inches(top), Inches(width), Pt(3),
    )
    line.fill.solid()
    line.fill.fore_color.rgb = _c(design, "highlight")
    line.line.fill.background()
    return line


def _shape_text(shape, text, size, bold, color):
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = "Noto Sans JP"
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = PP_ALIGN.CENTER


def _style_cell(cell, size, bold, color):
    for p in cell.text_frame.paragraphs:
        p.font.name = "Noto Sans JP"
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
