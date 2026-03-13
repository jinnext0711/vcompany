"""箇条書きリスト図解 — カードベースの番号付きアイテム。"""

from src.output.helpers import (
    _text_box, _rect, _circle, _shape_text, _c, _safe,
    FS_BODY, FS_BODY_SMALL, FS_HEADING,
    WHITE, G, PP_ALIGN, MSO_ANCHOR,
)

_ACCENT_W = 4 / 72
_CIRCLE_R = 0.18


def render_bullet_list(slide, rect, data, design):
    """カードベースの箇条書きリストをゾーン内に描画する。"""
    items = data.get("items", [])
    heading = data.get("heading", "")
    if not items and not heading:
        return

    y = rect.top + G

    # 見出し
    heading_h = 0.0
    if heading:
        heading_h = 0.50
        _text_box(slide, rect.left + 0.1, y, _safe(rect.width - 0.2), heading_h,
                  heading, "Noto Sans JP", FS_HEADING, True,
                  _c(design, "primary"), PP_ALIGN.LEFT)
        y += heading_h + G * 0.5

    # アイテム数をゾーンに合わせて制限
    avail_h = _safe(rect.height - heading_h - G * 2)
    min_card_h = 0.50
    max_items = max(int(avail_h / min_card_h), 1)
    items = items[:min(max_items, 6)]
    n = len(items)
    if n == 0:
        return

    card_h = _safe((avail_h - G * (n - 1)) / n, min_card_h)

    # フォントサイズ適応
    if card_h >= 1.0:
        fs_item, fs_detail = 13, 12
    elif card_h >= 0.7:
        fs_item, fs_detail = 12, 11
    else:
        fs_item, fs_detail = 11, 11

    highlight = _c(design, "highlight")
    light_bg = _c(design, "light_bg")
    text_color = _c(design, "text")
    primary_color = _c(design, "primary")

    for i, item_data in enumerate(items):
        # カード背景
        _rect(slide, rect.left, y, _safe(rect.width), card_h, light_bg)

        # 左アクセントバー
        _rect(slide, rect.left, y, _ACCENT_W, card_h, highlight)

        # 番号サークル
        circle_cx = rect.left + 0.35
        circle_cy = y + card_h / 2
        circle_shape = _circle(slide, circle_cx, circle_cy, _CIRCLE_R,
                               highlight)
        _shape_text(circle_shape, str(i + 1), 11, True, WHITE)

        # テキスト
        text_left = rect.left + 0.35 + _CIRCLE_R * 2 + 0.12
        text_w = _safe(rect.width - (text_left - rect.left) - 0.15)

        if isinstance(item_data, dict):
            title_text = item_data.get("title", "")
            detail_text = item_data.get("detail", "")

            if title_text and detail_text:
                title_h = card_h * 0.42
                _text_box(slide, text_left, y + G * 0.3, text_w, title_h,
                          title_text, "Noto Sans JP", fs_item, True,
                          primary_color, PP_ALIGN.LEFT,
                          anchor=MSO_ANCHOR.BOTTOM)
                _text_box(slide, text_left, y + title_h, text_w,
                          _safe(card_h - title_h - G * 0.3),
                          detail_text, "Noto Sans JP", fs_detail, False,
                          text_color, PP_ALIGN.LEFT,
                          anchor=MSO_ANCHOR.TOP, line_spacing=1.2)
            elif title_text:
                _text_box(slide, text_left, y, text_w, card_h,
                          title_text, "Noto Sans JP", fs_item, True,
                          primary_color, PP_ALIGN.LEFT,
                          anchor=MSO_ANCHOR.MIDDLE)
            else:
                _text_box(slide, text_left, y, text_w, card_h,
                          detail_text, "Noto Sans JP", fs_item, False,
                          text_color, PP_ALIGN.LEFT,
                          anchor=MSO_ANCHOR.MIDDLE)
        else:
            _text_box(slide, text_left, y, text_w, card_h,
                      str(item_data), "Noto Sans JP", fs_item, False,
                      text_color, PP_ALIGN.LEFT,
                      anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.2)

        y += card_h + G
