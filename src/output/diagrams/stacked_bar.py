"""積み上げ棒グラフ図解 — シェイプベース（Chart API互換性問題を回避）。"""

from pptx.dml.color import RGBColor

from src.output.helpers import (
    _text_box, _rect, _c, _safe, G,
    FS_LABEL, FS_BODY_SMALL, WHITE,
    PP_ALIGN, MSO_ANCHOR,
)

# チャートパレット（最大8系列）
_PALETTE = [
    (26, 26, 46),     # primary dark
    (83, 134, 139),   # teal
    (230, 126, 34),   # orange
    (46, 204, 113),   # green
    (155, 89, 182),   # purple
    (52, 152, 219),   # blue
    (241, 196, 15),   # yellow
    (231, 76, 60),    # red
]


def render_stacked_bar(slide, rect, data, design):
    """積み上げ棒グラフをゾーン内に描画する。"""
    sd = data.get("stacked_bar_data", data.get("stacked_data", data))
    cats = sd.get("categories", [])
    series_list = sd.get("series", [])
    if not cats or not series_list:
        return

    n_cats = len(cats)
    n_series = len(series_list)

    # エリア計算
    label_w = min(2.0, rect.width * 0.22)
    legend_h = 0.45
    bar_left = rect.left + label_w + 0.1
    bar_max_w = _safe(rect.width - label_w - 0.5)

    chart_top = rect.top + G
    chart_h = _safe(rect.height - G * 2 - legend_h)

    bar_pitch = chart_h / n_cats
    bar_h = _safe(bar_pitch * 0.55, 0.15)
    bar_gap = (bar_pitch - bar_h) / 2

    # 各カテゴリの合計値を算出
    cat_totals = []
    for ci in range(n_cats):
        total = sum(
            s.get("values", [])[ci] if ci < len(s.get("values", [])) else 0
            for s in series_list
        )
        cat_totals.append(total)
    max_total = max(cat_totals) if cat_totals else 1
    if max_total == 0:
        max_total = 1

    # 系列色
    series_colors = []
    for si in range(n_series):
        try:
            rgb = design.get_chart_color_rgb(si)
            series_colors.append(RGBColor(*rgb))
        except (AttributeError, IndexError):
            p = _PALETTE[si % len(_PALETTE)]
            series_colors.append(RGBColor(*p))

    # バー描画
    fs_label = min(FS_BODY_SMALL, max(11, int(bar_h * 14)))

    for ci, cat in enumerate(cats):
        y = chart_top + ci * bar_pitch + bar_gap

        # カテゴリラベル
        _text_box(slide, rect.left, y, label_w, bar_h,
                  cat, "Noto Sans JP", fs_label, False,
                  _c(design, "text"), PP_ALIGN.RIGHT,
                  anchor=MSO_ANCHOR.MIDDLE)

        # 積み上げバー
        x_offset = 0
        for si, s in enumerate(series_list):
            vals = s.get("values", [])
            v = vals[ci] if ci < len(vals) else 0
            seg_w = _safe(bar_max_w * v / max_total, 0.01) if v > 0 else 0

            if seg_w > 0.01:
                _rect(slide, bar_left + x_offset, y, seg_w, bar_h,
                      series_colors[si])

                # セグメント内のラベル（十分な幅がある場合のみ）
                if seg_w >= 0.5:
                    _text_box(slide, bar_left + x_offset, y, seg_w, bar_h,
                              str(v), "Noto Sans JP", 11, True,
                              WHITE, PP_ALIGN.CENTER,
                              anchor=MSO_ANCHOR.MIDDLE)

            x_offset += seg_w

        # 合計値（右端）
        _text_box(slide, bar_left + x_offset + 0.05, y, 0.5, bar_h,
                  str(cat_totals[ci]), "Noto Sans JP", 11, True,
                  _c(design, "text"), PP_ALIGN.LEFT,
                  anchor=MSO_ANCHOR.MIDDLE)

    # 凡例（下部）
    legend_y = rect.top + rect.height - legend_h + G
    legend_item_w = min(2.0, (rect.width - 0.4) / n_series)

    for si, s in enumerate(series_list):
        lx = rect.left + 0.2 + si * legend_item_w
        # 色ボックス
        _rect(slide, lx, legend_y + 0.05, 0.20, 0.20, series_colors[si])
        # ラベル
        _text_box(slide, lx + 0.28, legend_y, _safe(legend_item_w - 0.35), 0.30,
                  s.get("name", f"Series {si + 1}"), "Noto Sans JP", 11, False,
                  _c(design, "text"), PP_ALIGN.LEFT,
                  anchor=MSO_ANCHOR.MIDDLE)
