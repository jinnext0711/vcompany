"""ウォーターフォール図解。"""

from pptx.dml.color import RGBColor

from src.output.helpers import (
    _text_box, _rect, _hline, _c, _safe, G,
    FS_LABEL, FS_BODY_SMALL,
    PP_ALIGN,
)


def render_waterfall(slide, rect, data, design):
    """ウォーターフォール図をゾーン内に描画する。"""
    items = data.get("waterfall_items", [])
    if not items:
        return

    n = len(items)
    padding = 0.25
    al = rect.left + padding
    aw = _safe(rect.width - padding * 2)
    label_h = 0.35
    value_h = 0.28
    at = rect.top + value_h + 0.15
    ab = rect.top + rect.height - label_h - 0.08
    ch = _safe(ab - at)

    btw = aw / n
    bw = btw * 0.60
    bgap = btw * 0.20

    # フォントサイズ適応
    fs_value = min(FS_BODY_SMALL, max(11, int(btw * 5)))
    fs_label = min(11, max(11, int(btw * 4)))

    running = 0
    positions = []
    all_vals = []
    for item in items:
        v = item.get("value", 0)
        t = item.get("type", "increase")
        if t in ("start", "total"):
            bb, bt_val = 0, v
        elif t == "increase":
            bb, bt_val = running, running + v
            running += v
        elif t == "decrease":
            bt_val, bb = running, running - abs(v)
            running -= abs(v)
        else:
            bb, bt_val = 0, v
        positions.append((bb, bt_val))
        all_vals.extend([bb, bt_val])

    mn = min(all_vals) if all_vals else 0
    mx_v = max(all_vals) if all_vals else 1
    vr = (mx_v - mn) or 1

    def v2y(v):
        return ab - ((v - mn) / vr) * ch

    # ゼロ線
    if mn <= 0 <= mx_v:
        _hline(slide, al - 0.05, v2y(0), aw + 0.1, _c(design, "border"), 1)

    inc_c = RGBColor(80, 170, 100)
    dec_c = RGBColor(200, 90, 90)
    prev_top_y = None

    for i, item in enumerate(items):
        v = item.get("value", 0)
        t = item.get("type", "increase")
        bb, bt_val = positions[i]
        bx = al + i * btw + bgap
        by_t = v2y(bt_val)
        by_b = v2y(bb)
        bh = _safe(abs(by_b - by_t), 0.03)

        if t in ("start", "total"):
            bc = _c(design, "primary")
        elif t == "increase":
            bc = inc_c
        else:
            bc = dec_c

        _rect(slide, bx, min(by_t, by_b), _safe(bw), bh, bc)

        # 値ラベル
        _text_box(slide, bx - 0.08, min(by_t, by_b) - value_h,
                  _safe(bw + 0.16), value_h,
                  str(v), "Noto Sans JP", fs_value, True,
                  _c(design, "text"), PP_ALIGN.CENTER)

        # カテゴリラベル
        _text_box(slide, bx - 0.15, ab + 0.05,
                  _safe(bw + 0.30), label_h,
                  item.get("label", ""), "Noto Sans JP", fs_label, False,
                  _c(design, "text"), PP_ALIGN.CENTER)

        # コネクタ線
        if prev_top_y is not None and t not in ("start", "total"):
            cx_s = bx - bgap + bw
            cx_e = bx
            if cx_e > cx_s:
                _rect(slide, cx_s, prev_top_y, _safe(cx_e - cx_s), 1 / 72,
                      _c(design, "border"))

        prev_top_y = v2y(bt_val)
