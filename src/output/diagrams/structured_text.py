"""構造化テキスト図解 — キーワード + 詳細のカード形式。

改善版: ゾーンサイズ適応、テキスト階層、ドロップシャドウ。
"""

from pptx.dml.color import RGBColor

from src.output.helpers import (
    _text_box, _rect, _c, _safe, G,
    PP_ALIGN, MSO_ANCHOR,
)

_ACCENT_W = 4 / 72  # ~4pt


def render_structured_text(slide, rect, data, design):
    """構造化テキスト（太字KW + 補足）をゾーン内に描画する。"""
    items = data.get("structured_items", [])
    bottom_note = data.get("bottom_note", "")
    if not items:
        return

    items = items[:5]
    n = len(items)

    # ボトムノート用スペース確保
    note_h = 0.50 if bottom_note else 0.0
    avail_h = _safe(rect.height - G * 2 - note_h)

    # カードサイズ計算
    card_gap = G
    card_h = _safe((avail_h - card_gap * (n - 1)) / n, 0.4)

    # フォントサイズをカード高さに応じて適応
    if card_h >= 2.0:
        fs_kw, fs_detail, fs_sub = 18, 13, 11
    elif card_h >= 1.2:
        fs_kw, fs_detail, fs_sub = 15, 13, 11
    elif card_h >= 0.8:
        fs_kw, fs_detail, fs_sub = 14, 12, 11
    else:
        fs_kw, fs_detail, fs_sub = 13, 11, 11

    y = rect.top + G

    for item in items:
        kw = item.get("keyword", "")
        detail = item.get("detail", "")
        sub = item.get("sub_detail", "")

        # カード背景
        _rect(slide, rect.left, y, _safe(rect.width), card_h,
              _c(design, "light_bg"))

        # 左アクセントバー
        _rect(slide, rect.left, y, _ACCENT_W, card_h,
              _c(design, "highlight"))

        # テキストレイアウト — 常に縦積み（keyword上 → detail下）
        text_left = rect.left + 0.25
        text_w = _safe(rect.width - 0.40)
        inner_y = y + G * 0.7

        # キーワード行
        kw_h = min(0.35, card_h * 0.30)
        _text_box(slide, text_left, inner_y, text_w, kw_h,
                  kw, "Noto Sans JP", fs_kw, True,
                  _c(design, "primary"), PP_ALIGN.LEFT)
        inner_y += kw_h

        # 残り高さをdetailとsub_detailに配分
        remain_h = _safe(card_h - kw_h - G * 1.2)

        if detail:
            detail_h = remain_h * (0.65 if sub else 1.0)
            # テキストが溢れないよう切り詰め
            max_chars_line = max(int(text_w / (fs_detail / 72 * 0.8)), 5)
            max_lines = max(int(detail_h / (fs_detail * 1.3 / 72)), 1)
            max_chars = max_chars_line * max_lines
            if len(detail) > max_chars:
                detail = detail[:max_chars - 1] + "…"
            _text_box(slide, text_left, inner_y, text_w, detail_h,
                      detail, "Noto Sans JP", fs_detail, False,
                      _c(design, "text"), PP_ALIGN.LEFT,
                      line_spacing=1.3)
            inner_y += detail_h

        if sub:
            sub_h = _safe(remain_h * 0.30)
            _text_box(slide, text_left, inner_y + G * 0.3, text_w, sub_h,
                      sub, "Noto Sans JP", fs_sub, False,
                      _c(design, "light_text"), PP_ALIGN.LEFT,
                      line_spacing=1.2)

        y += card_h + card_gap

    # ボトムノート
    if bottom_note:
        note_y = rect.top + rect.height - note_h
        _rect(slide, rect.left, note_y, _safe(rect.width), note_h,
              _c(design, "light_bg"))
        _text_box(slide, rect.left + 0.15, note_y + 0.06,
                  _safe(rect.width - 0.30), _safe(note_h - 0.12),
                  bottom_note, "Noto Sans JP", 11, False,
                  _c(design, "light_text"), PP_ALIGN.LEFT)
