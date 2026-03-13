"""KPIカード図解 — 大きな数値 + ラベル + トレンド。"""

from pptx.dml.color import RGBColor

from src.output.helpers import (
    _text_box, _rect, _c, _safe, G,
    FS_KPI, FS_LABEL, WHITE,
    PP_ALIGN, MSO_ANCHOR,
)


def render_kpi_card(slide, rect, data, design):
    """KPIカードをゾーン内に描画する。"""
    kpi_items = data.get("kpi_items")
    if kpi_items:
        _render_kpi_multi(slide, rect, kpi_items, data.get("insight", ""), design)
        return

    value = data.get("value", "")
    label = data.get("label", "")
    trend = data.get("trend", "")
    if not value:
        return

    # カードサイズをゾーンに適応
    card_h = min(2.4, rect.height - G * 2)
    card_w = min(rect.width, 4.0)
    x = rect.left + (rect.width - card_w) / 2
    y = rect.top + (rect.height - card_h) / 2

    # カード
    _rect(slide, x, y, _safe(card_w), card_h, WHITE,
          line_color=_c(design, "border"), line_width=1)
    _rect(slide, x, y, _safe(card_w), 4 / 72, _c(design, "highlight"))

    # KPI値 — フォントサイズをカード幅に適応
    fs_kpi = min(FS_KPI, int(card_w * 12))
    _text_box(slide, x, y + card_h * 0.10, card_w, card_h * 0.40,
              value, "Noto Sans JP", fs_kpi, True,
              _c(design, "primary"), PP_ALIGN.CENTER,
              anchor=MSO_ANCHOR.MIDDLE)

    # ラベル
    _text_box(slide, x + 0.10, y + card_h * 0.52, _safe(card_w - 0.20), card_h * 0.25,
              label, "Noto Sans JP", 12, False,
              _c(design, "text"), PP_ALIGN.CENTER, line_spacing=1.3)

    # トレンド
    if trend:
        _text_box(slide, x + 0.10, y + card_h * 0.78, _safe(card_w - 0.20), card_h * 0.18,
                  trend, "Noto Sans JP", FS_LABEL, False,
                  _c(design, "highlight"), PP_ALIGN.CENTER)


def _render_kpi_multi(slide, rect, items, insight, design):
    """複数KPIカードをゾーン内に横並びで描画する。"""
    n = len(items)
    insight_reserve = 0.50 if insight else 0
    avail_h = rect.height - insight_reserve

    # カードサイズ計算
    card_w = min(rect.width * 0.28, (rect.width - G * (n + 1)) / n)
    card_w = _safe(card_w, 1.5)
    total_w = card_w * n
    gap = _safe((rect.width - total_w) / max(n + 1, 2), G)
    card_h = min(2.4, avail_h - G * 2)

    y = rect.top + (avail_h - card_h) / 2

    for i, item in enumerate(items):
        x = rect.left + gap + i * (card_w + gap)

        _rect(slide, x, y, _safe(card_w), card_h, WHITE,
              line_color=_c(design, "border"), line_width=1)
        _rect(slide, x, y, _safe(card_w), 4 / 72, _c(design, "highlight"))

        fs_kpi = min(FS_KPI, int(card_w * 12))
        _text_box(slide, x, y + card_h * 0.10, card_w, card_h * 0.40,
                  item.get("value", ""), "Noto Sans JP", fs_kpi, True,
                  _c(design, "primary"), PP_ALIGN.CENTER,
                  anchor=MSO_ANCHOR.MIDDLE)

        _text_box(slide, x + 0.10, y + card_h * 0.52, _safe(card_w - 0.20),
                  card_h * 0.25,
                  item.get("label", ""), "Noto Sans JP", 12, False,
                  _c(design, "text"), PP_ALIGN.CENTER, line_spacing=1.3)

        trend = item.get("trend", "")
        if trend:
            _text_box(slide, x + 0.10, y + card_h * 0.78,
                      _safe(card_w - 0.20), card_h * 0.18,
                      trend, "Noto Sans JP", FS_LABEL, False,
                      _c(design, "highlight"), PP_ALIGN.CENTER)

    if insight:
        iy = rect.top + rect.height - insight_reserve + 0.03
        _text_box(slide, rect.left, iy, _safe(rect.width), 0.40,
                  insight, "Noto Sans JP", FS_LABEL, False,
                  _c(design, "light_text"), PP_ALIGN.LEFT)
