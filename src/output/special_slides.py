"""特殊スライド — コンサルティング品質の固定形式スライド。

consulting-slide-master-spec.md §4 準拠。
title, agenda, section_divider, executive_summary, summary の5種。
"""

from pptx.oxml.ns import qn

from src.output.helpers import (
    _text_box, _rect, _circle, _hline, _shape_text,
    _accent_line, _add_header, _add_footer, _add_left_accent, _add_notes,
    _blank_slide, _c,
    SLIDE_W, SLIDE_H, MARGIN_L, MARGIN_R, CONTENT_W,
    HEADER_TOP, HEADER_HEIGHT, ACCENT_LINE_TOP,
    HEADER_TITLE_TOP, HEADER_MSG_TOP, HEADER_BOTTOM,
    BODY_TOP, BODY_BOTTOM, BODY_H, FOOTER_TOP, FOOTER_H, G,
    FS_TITLE, FS_ACTION_TITLE, FS_SECTION_TITLE, FS_SECTION_NUMBER,
    FS_SUBTITLE, FS_HEADING, FS_BODY, FS_BODY_SMALL,
    FS_SLIDE_TITLE, FS_MESSAGE, FS_SECTION_HEADING,
    FS_SUB, FS_LABEL, FS_FOOTER, FS_KPI, FS_CAPTION,
    WHITE,
    PP_ALIGN, MSO_ANCHOR, RGBColor,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Title Slide — spec §4-1 McKinsey風統合版
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def add_title_slide(prs, content, design):
    """表紙スライド — 濃紺背景 + 白テキスト。

    spec §4-1:
      背景: Primary色ベタ塗り
      メインタイトル: top=2.0, 36pt Bold, White
      区切り線: top=3.5, width=3.0, Accent色
      サブタイトル: top=3.7, 18pt, White 80%
      日付: top=5.0, 14pt, White 60%
    """
    slide = _blank_slide(prs)
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = _c(design, "primary")

    # メインタイトル
    _text_box(slide, 1.0, 2.0, 11.333, 1.5,
              content.get("title", ""), "Noto Sans JP", FS_TITLE, True,
              WHITE, PP_ALIGN.LEFT, line_spacing=1.2)

    # 区切り線（アクセントカラー）
    _hline(slide, 1.0, 3.5, 3.0, _c(design, "highlight"), 2.0)

    # サブタイトル
    subtitle = content.get("subtitle", "")
    if subtitle:
        _text_box(slide, 1.0, 3.7, 11.333, 0.8,
                  subtitle, "Noto Sans JP", FS_SUBTITLE, False,
                  RGBColor(0xCC, 0xCC, 0xCC), PP_ALIGN.LEFT)

    # 日付
    date_text = content.get("date", "")
    if date_text:
        _text_box(slide, 1.0, 5.0, 5.0, 0.4,
                  date_text, "Noto Sans JP", 14, False,
                  RGBColor(0x99, 0x99, 0x99), PP_ALIGN.LEFT)

    # 機密表示
    _text_box(slide, 1.0, 6.8, 5.0, 0.3,
              "CONFIDENTIAL", "Noto Sans JP", 10, False,
              RGBColor(0x66, 0x66, 0x66), PP_ALIGN.LEFT)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Agenda — spec §4-2
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def add_agenda_slide(prs, section, design):
    """アジェンダスライド — 番号付きリスト。

    spec §4-2:
      タイトル "Agenda": 22pt Bold
      各項目: 番号(Primary色) + テキスト(16pt Bold + 14pt Regular)
      現在セクション: アクセントカラー
      他セクション: Light Gray でグレーアウト
    """
    slide = _blank_slide(prs)

    # ヘッダー
    _add_header(slide, {
        "slide_title": "",
        "title": section.get("title", "Agenda"),
    }, design)

    items = section.get("agenda_items", section.get("bullet_points", []))
    current = section.get("current_section", -1)
    y = 1.50  # spec §4-2: 項目開始位置
    item_h = min(0.70, (BODY_BOTTOM - 1.50) / max(len(items), 1))

    for i, item in enumerate(items[:7]):
        if isinstance(item, dict):
            main_text = item.get("title", "")
            sub_text = item.get("description", "")
        else:
            main_text, sub_text = str(item), ""

        is_current = (i == current)
        num_color = _c(design, "highlight") if is_current else RGBColor(0xCC, 0xCC, 0xCC)
        text_color = _c(design, "primary") if is_current else RGBColor(0xCC, 0xCC, 0xCC)

        # 番号 (01, 02, ...)
        _text_box(slide, MARGIN_L, y, 0.8, item_h,
                  f"{i + 1:02d}", "Noto Sans JP", 24, True,
                  num_color, PP_ALIGN.RIGHT,
                  anchor=MSO_ANCHOR.TOP)

        # メインテキスト
        _text_box(slide, MARGIN_L + 1.0, y + 0.02, CONTENT_W - 1.2, 0.35,
                  main_text, "Noto Sans JP", FS_HEADING, True,
                  text_color, PP_ALIGN.LEFT)

        # サブテキスト
        if sub_text:
            sub_color = _c(design, "text") if is_current else RGBColor(0xCC, 0xCC, 0xCC)
            _text_box(slide, MARGIN_L + 1.0, y + 0.38, CONTENT_W - 1.2, 0.28,
                      sub_text, "Noto Sans JP", FS_BODY, False,
                      sub_color, PP_ALIGN.LEFT)

        y += item_h

    _add_footer(slide, section.get("source", ""), design)
    _add_notes(slide, section)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Section Divider — spec §4-3 McKinsey式
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def add_section_divider_slide(prs, section, design):
    """セクション区切り — 濃紺背景 + 白テキスト。

    spec §4-3:
      背景: Primary色
      セクション番号: top=2.5, 48pt Bold, Accent色
      セクション名:   top=3.3, 32pt Bold, White
      サブテキスト:   top=4.6, 16pt Regular, White 70%
    """
    slide = _blank_slide(prs)
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = _c(design, "primary")

    section_num = section.get("section_number", "")
    section_title = section.get("title", "")
    sub_text = section.get("body", section.get("subtitle", ""))

    # 垂直中央配置 — コンテンツ全体をスライド中央に寄せる
    content_h = 1.2 + (0.7 if sub_text else 0)
    base_y = (SLIDE_H - content_h) / 2 - 0.3

    # セクション番号
    if section_num:
        _text_box(slide, 1.0, base_y, 2.0, 0.8,
                  str(section_num).zfill(2), "Noto Sans JP",
                  FS_SECTION_NUMBER, True,
                  _c(design, "highlight"), PP_ALIGN.LEFT,
                  anchor=MSO_ANCHOR.MIDDLE)

    # セクション名
    title_left = 1.0 + (2.3 if section_num else 0)
    _text_box(slide, title_left, base_y + 0.8, SLIDE_W - title_left - 1.0, 1.2,
              section_title, "Noto Sans JP", FS_SECTION_TITLE, True,
              WHITE, PP_ALIGN.LEFT, line_spacing=1.2,
              anchor=MSO_ANCHOR.TOP)

    # サブテキスト
    if sub_text:
        _text_box(slide, title_left, base_y + 2.0, SLIDE_W - title_left - 1.0, 0.6,
                  sub_text, "Noto Sans JP", FS_HEADING, False,
                  RGBColor(0xB0, 0xB0, 0xB0), PP_ALIGN.LEFT)

    # フッター（簡易版: ページ番号のみ）
    _text_box(slide, SLIDE_W - 2.5, FOOTER_TOP, 2.0, FOOTER_H,
              "", "Noto Sans JP", FS_FOOTER, False,
              RGBColor(0x99, 0x99, 0x99), PP_ALIGN.RIGHT)

    _add_notes(slide, section)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Executive Summary — spec §4-9 McKinsey/BCG式
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def add_executive_summary_slide(prs, section, design):
    """エグゼクティブサマリー — 結論 + 番号付きメッセージカード。

    spec §4-9:
      各メッセージの左端に番号インジケーター（丸数字）
      太字の1行キーメッセージ + Regular の2-3行補足
      左側に色付きの縦バー（幅0.04"）を配置してメッセージを区切る
    """
    slide = _blank_slide(prs)

    # ヘッダー
    _add_header(slide, {
        "slide_title": section.get("slide_title", "Executive Summary"),
        "title": section.get("title", ""),
    }, design)

    # 結論帯（ハイライト背景）
    conclusion = section.get("conclusion", "")
    y = BODY_TOP
    if conclusion:
        _rect(slide, MARGIN_L, y, CONTENT_W, 0.70,
              _c(design, "light_bg"))
        _text_box(slide, MARGIN_L + 0.15, y + 0.10, CONTENT_W - 0.30, 0.50,
                  conclusion, "Noto Sans JP", FS_BODY, True,
                  _c(design, "primary"), PP_ALIGN.LEFT, line_spacing=1.3)
        y += 0.85

    # メッセージカード（spec §4-9: 番号 + 縦バー + テキスト）
    points = section.get("key_points", section.get("bullet_points", []))
    available_h = BODY_BOTTOM - y - 0.5  # Next Step 用のスペース確保
    card_h = min(1.20, available_h / max(len(points[:4]), 1))

    for i, point in enumerate(points[:4]):
        if isinstance(point, dict):
            title = point.get("title", "")
            detail = point.get("detail", "")
        else:
            title, detail = str(point), ""

        # 左側の縦バー（spec: 幅0.04"）
        _rect(slide, MARGIN_L, y, 0.04, card_h - 0.10,
              _c(design, "highlight"))

        # 番号インジケーター
        num_circle = _circle(slide, MARGIN_L + 0.30, y + 0.25, 0.18,
                             _c(design, "highlight"))
        _shape_text(num_circle, str(i + 1), 12, True, WHITE)

        # キーメッセージ（太字1行）
        _text_box(slide, MARGIN_L + 0.65, y + 0.05, CONTENT_W - 0.85, 0.30,
                  title, "Noto Sans JP", FS_HEADING, True,
                  _c(design, "text"), PP_ALIGN.LEFT)

        # 補足テキスト（Regular 2-3行）
        if detail:
            _text_box(slide, MARGIN_L + 0.65, y + 0.38, CONTENT_W - 0.85, 0.70,
                      detail, "Noto Sans JP", FS_BODY, False,
                      _c(design, "text"), PP_ALIGN.LEFT, line_spacing=1.3)

        y += card_h

    # Next Step（オプション）— カードの下に配置、衝突防止
    next_step = section.get("next_step", "")
    if next_step:
        ns_h = 0.42
        ns_y = min(y + G, BODY_BOTTOM - ns_h)  # カードの下、ただしボディ下端を超えない
        _rect(slide, MARGIN_L, ns_y, CONTENT_W, ns_h,
              _c(design, "primary"))
        _text_box(slide, MARGIN_L + 0.15, ns_y + 0.05, CONTENT_W - 0.30, 0.32,
                  f"Next Step: {next_step}", "Noto Sans JP", FS_BODY, True,
                  WHITE, PP_ALIGN.LEFT)

    _add_footer(slide, section.get("source", ""), design)
    _add_notes(slide, section)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Summary + Next Steps — spec §4-10 (2カラム)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def add_summary_slide(prs, section, design):
    """まとめスライド — 左: Key Takeaways + 右: Next Steps。

    spec §4-10:
      左カラム: Key Takeaways (6.0" wide)
      右カラム: Next Steps (6.0" wide)
    """
    slide = _blank_slide(prs)
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = _c(design, "primary")

    # タイトル
    _text_box(slide, MARGIN_L, 0.40, CONTENT_W, 0.70,
              section.get("slide_title", section.get("title", "まとめ")),
              "Noto Sans JP", 28, True,
              WHITE, PP_ALIGN.LEFT)

    # アクセントライン
    _hline(slide, MARGIN_L, 1.20, 3.0, _c(design, "highlight"), 2.0)

    # 左カラム: Key Takeaways
    col_w = 5.8
    left_x = MARGIN_L
    right_x = MARGIN_L + col_w + 0.733

    _text_box(slide, left_x, 1.50, col_w, 0.35,
              "Key Takeaways", "Noto Sans JP", FS_HEADING, True,
              _c(design, "highlight"), PP_ALIGN.LEFT)

    points = section.get("bullet_points", section.get("key_takeaways", []))
    y = 2.00
    for i, point in enumerate(points[:3]):
        text = point if isinstance(point, str) else point.get("text", str(point))
        # 番号付き丸
        num_c = _circle(slide, left_x + 0.20, y + 0.20, 0.20,
                        _c(design, "highlight"))
        _shape_text(num_c, str(i + 1), 14, True, WHITE)
        # テキスト
        _text_box(slide, left_x + 0.55, y, col_w - 0.55, 0.80,
                  text, "Noto Sans JP", FS_BODY, False,
                  WHITE, PP_ALIGN.LEFT, line_spacing=1.3)
        y += 1.10

    # 右カラム: Next Steps
    _text_box(slide, right_x, 1.50, col_w, 0.35,
              "Next Steps", "Noto Sans JP", FS_HEADING, True,
              _c(design, "highlight"), PP_ALIGN.LEFT)

    next_steps = section.get("next_steps", [])
    y = 2.00
    for j, ns in enumerate(next_steps[:4]):
        text = ns if isinstance(ns, str) else ns.get("text", str(ns))
        # 矢印マーカー
        _text_box(slide, right_x, y, 0.35, 0.35,
                  "→", "Noto Sans JP", FS_HEADING, False,
                  _c(design, "highlight"), PP_ALIGN.CENTER)
        _text_box(slide, right_x + 0.40, y + 0.02, col_w - 0.40, 0.70,
                  text, "Noto Sans JP", FS_BODY, False,
                  RGBColor(0xE0, 0xE0, 0xE0), PP_ALIGN.LEFT, line_spacing=1.3)
        y += 0.90

    _add_notes(slide, section)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# レジストリ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPECIAL_SLIDE_HANDLERS = {
    "title": None,  # タイトルは content レベルで呼ばれるため別扱い
    "agenda": add_agenda_slide,
    "section_divider": add_section_divider_slide,
    "executive_summary": add_executive_summary_slide,
    "summary": add_summary_slide,
}
