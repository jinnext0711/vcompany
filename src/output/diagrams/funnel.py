"""ファネル図解。"""

from src.output.helpers import (
    _text_box, _rect, _triangle, _shape_text, _c, _safe, _fade_color, G,
    FS_HEADING, FS_LABEL, WHITE,
    PP_ALIGN,
)


def render_funnel(slide, rect, data, design):
    """ファネル図をゾーン内に描画する。"""
    items = data.get("funnel_items", [])
    if not items:
        return

    n = len(items)

    # ファネルエリアと説明エリアの分割
    funnel_ratio = 0.40
    desc_ratio = 0.55
    gap_ratio = 0.05

    f_left = rect.left
    f_width = rect.width * funnel_ratio
    lbl_l = rect.left + rect.width * (funnel_ratio + gap_ratio)
    lbl_w = _safe(rect.width * desc_ratio)

    at = rect.top + G
    ah = _safe(rect.height - G * 2)
    lh = ah / n
    fcx = f_left + f_width / 2

    # フォントサイズ適応
    fs_title = min(14, max(11, int(lh * 9)))
    fs_desc = min(FS_LABEL, max(11, int(lh * 7)))
    fs_value = min(FS_HEADING, max(12, int(lh * 10)))

    for i, item in enumerate(items):
        ly = at + i * lh
        ratio = 1.0 - (i / max(n, 1)) * 0.6
        bw = _safe(f_width * ratio)
        bx = fcx - bw / 2
        lc = _fade_color(design, i, n, fade_target=230, fade_strength=0.7)
        tc = WHITE if i / max(n - 1, 1) < 0.5 else _c(design, "primary")

        shape = _rect(slide, bx, ly + G * 0.5, bw, _safe(lh - G), lc)

        val = item.get("value", "")
        if val:
            _shape_text(shape, str(val), fs_value, True, tc)

        # ラベル
        title = item.get("title", item.get("label", ""))
        desc = item.get("description", item.get("detail", ""))

        title_h = min(0.35, lh * 0.45)
        _text_box(slide, lbl_l, ly + G * 0.5, lbl_w, title_h,
                  title, "Noto Sans JP", fs_title, True,
                  _c(design, "primary"), PP_ALIGN.LEFT)

        if desc:
            desc_h = _safe(lh - G - title_h - 0.05)
            _text_box(slide, lbl_l, ly + G * 0.5 + title_h, lbl_w, desc_h,
                      desc, "Noto Sans JP", fs_desc, False,
                      _c(design, "light_text"), PP_ALIGN.LEFT, line_spacing=1.2)

        # 矢印（最後以外）
        if i < n - 1:
            arrow_s = min(0.12, lh * 0.15)
            _triangle(slide, fcx - arrow_s, ly + lh - G * 0.3,
                      arrow_s * 2, arrow_s * 2,
                      _c(design, "highlight"), 180)
