"""タイムライン図解。"""

from src.output.helpers import (
    _text_box, _rect, _shape_text, _c, _safe, G,
    FS_LABEL, FS_BODY_SMALL, WHITE,
    PP_ALIGN,
)


def render_timeline(slide, rect, data, design):
    """タイムラインをゾーン内に描画する。"""
    items = data.get("timeline_items", [])
    if not items:
        return

    n = len(items)
    padding = 0.15
    al = rect.left + padding
    aw = _safe(rect.width - padding * 2)

    # バーの位置と高さ
    bar_y = rect.top + 0.9
    bar_h = 0.42
    seg_w = aw / n

    # フォントサイズ適応
    fs_phase = min(12, max(11, int(seg_w * 5)))
    fs_dur = min(FS_LABEL, max(11, int(seg_w * 4)))

    # ベースバー
    _rect(slide, al, bar_y, aw, bar_h, _c(design, "light_bg"))

    for i, item in enumerate(items):
        sx = al + i * seg_w
        highlight = item.get("highlight", False)
        sc = _c(design, "highlight") if highlight else _c(design, "primary")

        # セグメント
        seg = _rect(slide, sx + 0.02, bar_y + 0.02,
                    _safe(seg_w - 0.04), bar_h - 0.04, sc)
        _shape_text(seg, item.get("phase", ""), fs_phase, True, WHITE)

        # 期間ラベル（上）
        dur = item.get("duration", "")
        if dur:
            _text_box(slide, sx, bar_y - 0.35, _safe(seg_w), 0.30,
                      dur, "Noto Sans JP", fs_dur, False,
                      _c(design, "light_text"), PP_ALIGN.CENTER)

        # タスク一覧（下）
        tasks = item.get("tasks", [])
        ty = bar_y + bar_h + 0.15
        avail_task_h = _safe(rect.top + rect.height - ty - G)
        max_tasks = max(int(avail_task_h / 0.25), 1)

        # タスクテキストをセグメント幅に応じて切り詰め
        fs_task = 11
        max_chars = max(int((seg_w - 0.06) / (fs_task / 72 * 0.8)), 8)
        task_line_h = max(0.22, avail_task_h / max(len(tasks[:min(max_tasks, 4)]), 1))
        task_line_h = min(task_line_h, 0.30)

        for ti, task in enumerate(tasks[:min(max_tasks, 4)]):
            display_task = task if len(task) <= max_chars else task[:max_chars - 1] + "…"
            _text_box(slide, sx + 0.03, ty + ti * task_line_h,
                      _safe(seg_w - 0.06), _safe(task_line_h - 0.02),
                      f"- {display_task}", "Noto Sans JP", fs_task, False,
                      _c(design, "text"), PP_ALIGN.LEFT)
