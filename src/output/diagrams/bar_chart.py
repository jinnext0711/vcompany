"""横棒グラフ図解 — シェイプベース（Chart API互換性問題を回避）。"""

from pptx.dml.color import RGBColor

from src.output.helpers import (
    _text_box, _rect, _hline, _c, _safe, G,
    FS_LABEL, FS_BODY_SMALL,
    PP_ALIGN, MSO_ANCHOR,
)


def render_bar_chart(slide, rect, data, design):
    """横棒グラフをゾーン内に描画する。"""
    items = data.get("items", [])
    insight = data.get("insight", "")
    highlight_label = data.get("highlight", "")
    if not items:
        return

    n = len(items)

    # エリア計算
    label_w = min(2.2, rect.width * 0.25)  # ラベル用幅
    value_label_w = 0.6  # 値表示用幅
    bar_left = rect.left + label_w + 0.1
    bar_max_w = _safe(rect.width - label_w - value_label_w - 0.3)

    insight_h = 0.55 if insight else 0
    chart_top = rect.top + G
    chart_h = _safe(rect.height - G * 2 - insight_h)

    bar_pitch = chart_h / n
    bar_h = _safe(bar_pitch * 0.60, 0.15)
    bar_gap = (bar_pitch - bar_h) / 2

    # 最大値を算出
    values = [item.get("value", 0) for item in items]
    max_val = max(values) if values else 1
    if max_val == 0:
        max_val = 1

    # フォントサイズ適応
    fs_label = min(FS_BODY_SMALL, max(11, int(bar_h * 14)))
    fs_value = min(FS_BODY_SMALL, max(11, int(bar_h * 12)))

    primary_c = _c(design, "primary")
    highlight_c = _c(design, "highlight")

    # 背景グリッドライン（4分割）
    for i in range(5):
        gx = bar_left + bar_max_w * i / 4
        _rect(slide, gx, chart_top, 1 / 72, chart_h,
              _c(design, "border"))

    for i, item in enumerate(items):
        v = item.get("value", 0)
        label = item.get("label", "")
        y = chart_top + i * bar_pitch + bar_gap

        # ハイライト判定
        is_highlight = (
            (highlight_label and label == highlight_label) or
            item.get("highlight", False)
        )
        bar_color = highlight_c if is_highlight else primary_c

        # バー
        bw = _safe(bar_max_w * abs(v) / max_val, 0.05)
        _rect(slide, bar_left, y, bw, bar_h, bar_color)

        # ラベル（左側）
        _text_box(slide, rect.left, y, label_w, bar_h,
                  label, "Noto Sans JP", fs_label, False,
                  _c(design, "text"), PP_ALIGN.RIGHT,
                  anchor=MSO_ANCHOR.MIDDLE)

        # 値（バーの右側）
        _text_box(slide, bar_left + bw + 0.05, y, value_label_w, bar_h,
                  str(v), "Noto Sans JP", fs_value, True,
                  _c(design, "text"), PP_ALIGN.LEFT,
                  anchor=MSO_ANCHOR.MIDDLE)

    # insight テキスト
    if insight:
        iy = rect.top + rect.height - insight_h
        _rect(slide, rect.left, iy, _safe(rect.width), _safe(insight_h),
              _c(design, "light_bg"))
        _text_box(slide, rect.left + 0.15, iy + 0.06,
                  _safe(rect.width - 0.30), _safe(insight_h - 0.12),
                  insight, "Noto Sans JP", 11, False,
                  _c(design, "light_text"), PP_ALIGN.LEFT, line_spacing=1.2)
