"""フロー図解 — コンサルティング品質プロセスステップ + シェブロン矢印。"""

from src.output.helpers import (
    _text_box, _rect, _circle, _shape_text, _c, _safe,
    FS_BODY, FS_BODY_SMALL, FS_LABEL,
    WHITE, G, PP_ALIGN, MSO_ANCHOR, MSO_SHAPE,
    Inches, Pt, RGBColor,
)


def _rounded_rect(slide, left, top, width, height, fill_color, *,
                  line_color=None, line_width=None):
    """角丸矩形シェイプを追加する。"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top),
        Inches(_safe(width)), Inches(_safe(height)),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width or 1)
    else:
        shape.line.fill.background()
    return shape


def _chevron(slide, left, top, width, height, fill_color):
    """シェブロン矢印シェイプを追加する。"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.CHEVRON, Inches(left), Inches(top),
        Inches(_safe(width)), Inches(_safe(height)),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape


def render_flow(slide, rect, data, design):
    """プロセスフロー図をゾーン内に描画する。"""
    steps = data.get("flow_steps", [])
    descs = data.get("flow_descriptions", [])
    details = data.get("flow_details", [])
    if not steps:
        return

    n = len(steps)
    has_details = bool(details)

    # --- ゾーン幅からの逆算レイアウト ---
    # シェブロン幅とギャップを n に応じてスケーリング
    chevron_w = min(0.25, rect.width / (n * 6))
    gap = min(0.12, rect.width / (n * 8))

    # ボックス幅 = (ゾーン幅 - 全シェブロン幅 - 全ギャップ) / n
    total_non_box = (n - 1) * (chevron_w + gap * 2)
    box_w = _safe((rect.width - total_non_box) / n, 0.8)

    # 合計幅がゾーンを超えないようクランプ
    total_w = n * box_w + total_non_box
    if total_w > rect.width:
        box_w = _safe((rect.width - total_non_box) / n, 0.8)
        total_w = n * box_w + total_non_box

    # フォントサイズをステップ数に応じて調整
    if n <= 3:
        fs_step = FS_BODY      # 14pt
        fs_desc = FS_BODY_SMALL  # 12pt
        fs_detail = 11
    elif n <= 4:
        fs_step = FS_BODY_SMALL  # 12pt
        fs_desc = 11
        fs_detail = 11
    else:
        fs_step = 11
        fs_desc = 11
        fs_detail = 11

    # ボックス高さ — ゾーン高さから逆算
    circle_r = 0.16
    circle_gap = 0.10
    top_section = circle_r * 2 + circle_gap  # ナンバーサークル分
    bottom_reserve = 0.0

    if has_details:
        # details がある場合: ボックス + detail + desc を縦に配置
        box_h = min(0.75, (rect.height - top_section) * 0.20)
        remaining = rect.height - top_section - box_h - 0.2
        detail_max_h = remaining * 0.65
        desc_max_h = remaining * 0.30
    elif descs:
        box_h = min(1.0, (rect.height - top_section) * 0.30)
        detail_max_h = 0
        desc_max_h = (rect.height - top_section - box_h) * 0.60
    else:
        box_h = min(1.2, (rect.height - top_section) * 0.50)
        detail_max_h = 0
        desc_max_h = 0

    # 垂直位置
    y_circle_center = rect.top + circle_r + 0.1
    y_box = y_circle_center + circle_r + circle_gap

    # 水平中央揃え
    x_start = rect.left + max(0, (rect.width - total_w) / 2)

    for i, step in enumerate(steps):
        x = x_start + i * (box_w + chevron_w + gap * 2) if i > 0 else x_start
        if i > 0:
            x = x_start + i * box_w + i * (chevron_w + gap * 2)
        box_cx = x + box_w / 2

        # --- ステップ番号サークル ---
        _shape_text(
            _circle(slide, box_cx, y_circle_center, circle_r,
                    _c(design, "highlight")),
            str(i + 1), 12, True, WHITE,
        )

        # --- ステップボックス ---
        is_first = (i == 0)
        fill = _c(design, "primary") if is_first else _c(design, "light_bg")
        text_c = WHITE if is_first else _c(design, "primary")
        border_c = _c(design, "primary")

        box = _rounded_rect(
            slide, x, y_box, box_w, box_h, fill,
            line_color=border_c, line_width=1.5,
        )
        _shape_text(box, step, fs_step, True, text_c)

        # --- Detail items below box ---
        detail_y = y_box + box_h + 0.06
        actual_detail_h = 0
        if i < len(details) and details[i] and detail_max_h > 0:
            detail_items = details[i]
            if isinstance(detail_items, list):
                # アイテム数をスペースに応じて制限
                max_detail_items = max(int(detail_max_h / 0.20), 1)
                detail_items = detail_items[:max_detail_items]
                detail_text = "\n".join(f"• {d}" for d in detail_items)
            else:
                detail_text = str(detail_items)
                # 長文テキストをボックス幅に応じて切り詰め
                max_chars_per_line = max(int((box_w - 0.06) / (fs_detail / 72 * 0.8)), 5)
                max_lines = max(int(detail_max_h / (fs_detail * 1.2 / 72)), 1)
                max_chars = max_chars_per_line * max_lines
                if len(detail_text) > max_chars:
                    detail_text = detail_text[:max_chars - 1] + "…"
            lines = detail_text.count("\n") + max(1, -(-len(detail_text) // max(int((box_w - 0.06) / (fs_detail / 72 * 0.8)), 5)))
            actual_detail_h = min(lines * (fs_detail * 1.2 / 72), detail_max_h)
            _text_box(
                slide, x + 0.03, detail_y, _safe(box_w - 0.06), actual_detail_h,
                detail_text, "Noto Sans JP", fs_detail, False,
                _c(design, "text"), PP_ALIGN.LEFT, line_spacing=1.2,
            )

        # --- Description below details ---
        if i < len(descs) and descs[i] and desc_max_h > 0:
            desc_y = detail_y + actual_detail_h + 0.04
            _text_box(
                slide, x, desc_y, _safe(box_w), min(0.50, desc_max_h),
                descs[i], "Noto Sans JP", fs_desc, False,
                _c(design, "text"), PP_ALIGN.CENTER, line_spacing=1.2,
            )

        # --- Chevron arrow ---
        if i < n - 1:
            chev_x = x + box_w + gap
            chev_y = y_box + box_h / 2 - 0.12
            _chevron(
                slide, chev_x, chev_y, chevron_w, 0.24,
                _c(design, "highlight"),
            )
