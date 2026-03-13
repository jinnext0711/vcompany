"""マトリクス図解 — 2x2ポジショニング。"""

from pptx.dml.color import RGBColor

from src.output.helpers import (
    _text_box, _rect, _circle, _c, _safe, G,
    FS_SUB, FS_LABEL, FS_BODY_SMALL,
    PP_ALIGN,
)


def render_matrix(slide, rect, data, design):
    """2x2マトリクスをゾーン内に描画する。"""
    x_label = data.get("x_label", "")
    y_label = data.get("y_label", "")
    q_labels = data.get("quadrant_labels", ["", "", "", ""])
    items = data.get("items", [])

    # マトリクスエリア計算（ラベル用スペースを確保）
    label_margin = 0.7
    axis_label_h = 0.35
    al = rect.left + label_margin
    at = rect.top + 0.2
    aw = _safe(rect.width - label_margin - 0.3)
    ah = _safe(rect.height - 0.2 - axis_label_h - 0.1)
    cx = al + aw / 2
    cy = at + ah / 2

    # 軸線
    _rect(slide, al, cy, aw, 2 / 72, _c(design, "border"))
    _rect(slide, cx, at, 2 / 72, ah, _c(design, "border"))

    # 軸ラベル
    if x_label:
        _text_box(slide, al, at + ah + 0.08, aw, axis_label_h,
                  x_label, "Noto Sans JP", FS_SUB, True,
                  _c(design, "primary"), PP_ALIGN.CENTER)
    if y_label:
        _text_box(slide, rect.left, cy - 0.5, label_margin - 0.05, 1.0,
                  y_label, "Noto Sans JP", FS_LABEL, True,
                  _c(design, "primary"), PP_ALIGN.CENTER)

    # 象限ラベル（コントラスト改善: #999999 に変更）
    q_color = RGBColor(153, 153, 153)
    qw = aw / 2 - 0.3
    q_positions = [
        (al + 0.15, at + 0.08),          # 左上
        (cx + 0.15, at + 0.08),          # 右上
        (al + 0.15, cy + 0.08),          # 左下
        (cx + 0.15, cy + 0.08),          # 右下
    ]
    for qi, (qx, qy) in enumerate(q_positions):
        if qi < len(q_labels) and q_labels[qi]:
            _text_box(slide, qx, qy, _safe(qw), 0.30,
                      q_labels[qi], "Noto Sans JP", 11, False,
                      q_color, PP_ALIGN.LEFT)

    # ドット + ラベル
    colors = [
        _c(design, "highlight"), _c(design, "primary"),
        RGBColor(100, 180, 100), RGBColor(200, 130, 60),
        RGBColor(150, 100, 180), RGBColor(180, 80, 80),
    ]
    # ドットサイズをゾーンに応じて調整
    dot_r = min(0.20, aw / 20, ah / 15)
    label_w = min(2.0, aw / 3)

    for idx, item in enumerate(items):
        ix_val = item.get("x", 0.5)
        iy_val = item.get("y", 0.5)
        # ドット位置をマトリクス内にクランプ
        px = al + max(0.05, min(ix_val, 0.95)) * aw
        py = at + max(0.05, min(1.0 - iy_val, 0.95)) * ah
        c = colors[idx % len(colors)]
        _circle(slide, px, py, dot_r, c)

        # ラベルがマトリクスからはみ出ないよう調整
        lbl_x = px + dot_r + 0.05
        if lbl_x + label_w > al + aw:
            lbl_x = px - dot_r - label_w - 0.05  # 左側に配置
        _text_box(slide, lbl_x, py - 0.15, label_w, 0.30,
                  item.get("name", ""), "Noto Sans JP", FS_LABEL, True,
                  _c(design, "text"), PP_ALIGN.LEFT)
