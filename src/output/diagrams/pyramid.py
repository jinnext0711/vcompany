"""ピラミッド図解 — 階層構造。"""

from src.output.helpers import (
    _text_box, _rect, _shape_text, _c, _safe, _fade_color, G,
    FS_SUB, FS_LABEL, WHITE,
    PP_ALIGN,
)


def render_pyramid(slide, rect, data, design):
    """ピラミッド図をゾーン内に描画する。"""
    levels = data.get("pyramid_levels", [])
    if not levels:
        return

    n = len(levels)

    # ピラミッドエリアと説明エリアの分割
    pyramid_ratio = 0.45  # ピラミッド部分の幅比率
    desc_ratio = 0.50
    gap_ratio = 0.05

    p_left = rect.left
    p_width = rect.width * pyramid_ratio
    desc_left = rect.left + rect.width * (pyramid_ratio + gap_ratio)
    desc_width = _safe(rect.width * desc_ratio)

    at = rect.top + G
    ah = _safe(rect.height - G * 2)
    lh = ah / n

    pcx = p_left + p_width / 2

    # フォントサイズ適応
    fs_title = min(14, max(11, int(lh * 10)))
    fs_desc = min(FS_SUB, max(11, int(lh * 8)))

    for i, level in enumerate(levels):
        ly = at + i * lh

        # ピラミッド形状: 上が狭く、下が広い
        top_ratio = (i + 0.5) / (n + 0.5)
        bot_ratio = (i + 1.5) / (n + 0.5)
        top_w = p_width * top_ratio
        bot_w = p_width * bot_ratio
        avg_w = (top_w + bot_w) / 2

        trap_x = pcx - avg_w / 2
        lc = _fade_color(design, i, n)
        text_c = WHITE if i / max(n - 1, 1) < 0.5 else _c(design, "primary")

        shape = _rect(slide, trap_x, ly + 0.03, _safe(avg_w), _safe(lh - 0.06), lc)
        _shape_text(shape, level.get("title", ""), fs_title, True, text_c)

        # 説明テキスト
        desc = level.get("description", "")
        if desc:
            _text_box(slide, desc_left, ly + 0.05, desc_width, _safe(lh - 0.10),
                      desc, "Noto Sans JP", fs_desc, False,
                      _c(design, "text"), PP_ALIGN.LEFT, line_spacing=1.2)
