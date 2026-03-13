"""比較パネル図解 — 見出し付きリスト（2カラム比較のパネル部分）。"""

from src.output.helpers import (
    _text_box, _rect, _c, _safe, G,
    FS_HEADING, FS_BODY, WHITE,
    PP_ALIGN,
)


def render_comparison_panel(slide, rect, data, design):
    """比較パネル（タイトルバー + 箇条書き）をゾーン内に描画する。"""
    heading = data.get("heading", "")
    items = data.get("items", [])
    accent_key = data.get("accent", "highlight")

    # 背景
    _rect(slide, rect.left, rect.top, _safe(rect.width), _safe(rect.height),
          _c(design, "light_bg"))
    # トップアクセント
    _rect(slide, rect.left, rect.top, _safe(rect.width), 4 / 72,
          _c(design, accent_key))

    # 見出し
    heading_h = 0.55
    _text_box(slide, rect.left + 0.15, rect.top + 0.12,
              _safe(rect.width - 0.3), 0.40,
              heading, "Noto Sans JP", 18, True,
              _c(design, "primary"), PP_ALIGN.CENTER)

    # アイテム — ゾーンの高さに合わせて配置
    avail_h = _safe(rect.height - heading_h - G)
    max_items = max(int(avail_h / 0.45), 1)
    items = items[:min(max_items, 6)]
    n = len(items)
    if n == 0:
        return

    item_h = min(avail_h / n, 0.65)
    iy = rect.top + heading_h + G * 0.5

    for t in items:
        _text_box(slide, rect.left + 0.25, iy,
                  _safe(rect.width - 0.5), item_h - G * 0.5,
                  f"—  {t}", "Noto Sans JP", FS_BODY, False,
                  _c(design, "text"), PP_ALIGN.LEFT, line_spacing=1.3)
        iy += item_h
