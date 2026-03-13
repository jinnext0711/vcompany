"""循環図解（サイクル / フライホイール）。"""

import math

from src.output.helpers import (
    _text_box, _rect, _circle, _triangle, _shape_text, _c, _safe, G,
    FS_SUB, FS_LABEL, WHITE,
    PP_ALIGN, MSO_ANCHOR,
)


def render_cycle(slide, rect, data, design):
    """循環図をゾーン内に描画する。"""
    items = data.get("cycle_items", [])
    if not items:
        return

    n = min(max(len(items), 3), 6)
    items = items[:n]
    center_label = data.get("cycle_center", "")

    acx = rect.left + rect.width / 2
    acy = rect.top + rect.height / 2

    # 半径をゾーンサイズに応じて計算（はみ出し防止）
    max_r_w = rect.width / 2 - 1.4
    max_r_h = rect.height / 2 - 0.8
    radius = _safe(min(max_r_w, max_r_h), 0.5)

    # 中央ラベル
    if center_label:
        center_r = min(0.55, radius * 0.35)
        _shape_text(
            _circle(slide, acx, acy, center_r, _c(design, "primary")),
            center_label, min(12, int(center_r * 18)), True, WHITE)

    # アイテムボックスサイズをゾーンと n に応じて調整
    iw = min(1.8, rect.width / (n * 0.7 + 1))
    ih = min(1.0, rect.height / (n * 0.5 + 1))

    # フォントサイズ適応
    fs_title = min(FS_SUB, max(11, int(iw * 7)))
    fs_desc = 11

    for i, item in enumerate(items):
        angle_deg = -90 + (360 / n) * i
        angle_rad = math.radians(angle_deg)
        ix = acx + radius * math.cos(angle_rad)
        iy = acy + radius * math.sin(angle_rad)

        # ボックス位置をゾーン内にクランプ
        ix = max(rect.left + iw / 2 + 0.05, min(ix, rect.left + rect.width - iw / 2 - 0.05))
        iy = max(rect.top + ih / 2 + 0.05, min(iy, rect.top + rect.height - ih / 2 - 0.05))

        box = _rect(slide, ix - iw / 2, iy - ih / 2, iw, ih,
                    _c(design, "light_bg"),
                    line_color=_c(design, "border"), line_width=1)
        # トップアクセント
        _rect(slide, ix - iw / 2, iy - ih / 2, iw, 3 / 72, _c(design, "highlight"))

        # タイトル
        title_h = 0.28
        _text_box(slide, ix - iw / 2 + 0.08, iy - ih / 2 + 0.06,
                  _safe(iw - 0.16), title_h,
                  item.get("title", ""), "Noto Sans JP", fs_title, True,
                  _c(design, "primary"), PP_ALIGN.CENTER,
                  anchor=MSO_ANCHOR.MIDDLE)

        # 説明（十分なスペースがある場合）
        desc = item.get("description", "")
        desc_avail = ih - title_h - 0.14
        if desc and desc_avail >= 0.25:
            # テキストが長すぎる場合は切り詰める
            max_chars = int((iw - 0.16) / (fs_desc / 72 * 0.8) * (desc_avail / (fs_desc * 1.1 / 72)))
            if len(desc) > max_chars:
                desc = desc[:max_chars - 1] + "…"
            _text_box(slide, ix - iw / 2 + 0.08, iy - ih / 2 + title_h + 0.08,
                      _safe(iw - 0.16), _safe(desc_avail),
                      desc, "Noto Sans JP", fs_desc, False,
                      _c(design, "text"), PP_ALIGN.CENTER, line_spacing=1.15)

        # 矢印
        mid_deg = angle_deg + (360 / n) / 2
        mid_rad = math.radians(mid_deg)
        ar = radius * 0.60
        ax_pos = acx + ar * math.cos(mid_rad)
        ay_pos = acy + ar * math.sin(mid_rad)
        arrow_size = min(0.18, radius * 0.12)
        _triangle(slide, ax_pos - arrow_size / 2, ay_pos - arrow_size / 2,
                  arrow_size, arrow_size,
                  _c(design, "highlight"), mid_deg + 90)
