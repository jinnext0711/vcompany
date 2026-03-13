"""レイアウトシステム — ボディ領域をゾーンに分割する。

レイアウトは「スライドのボディ領域をどう区切るか」のみを担当する。
各ゾーンは Rect（矩形領域）として定義され、図解レンダラーに渡される。
"""

from dataclasses import dataclass

from src.output.helpers import (
    BODY_TOP, BODY_BOTTOM, MARGIN_L, CONTENT_W, BODY_H, G,
    GAP as _SPEC_GAP,
)


@dataclass(frozen=True)
class Rect:
    """描画ゾーンの矩形領域（inches）。"""
    left: float
    top: float
    width: float
    height: float


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# レイアウト関数（各関数は dict[zone_name, Rect] を返す）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GAP = _SPEC_GAP  # spec §5-4: 0.333" カラム間ギャップ


def layout_full() -> dict:
    """全幅1ゾーン。"""
    return {"main": Rect(MARGIN_L, BODY_TOP, CONTENT_W, BODY_H)}


def layout_two_col(ratio=(0.5, 0.5)) -> dict:
    """2カラム。ratio で左右の比率を指定。"""
    usable = CONTENT_W - GAP
    left_w = usable * ratio[0]
    right_w = usable * ratio[1]
    return {
        "left": Rect(MARGIN_L, BODY_TOP, left_w, BODY_H),
        "right": Rect(MARGIN_L + left_w + GAP, BODY_TOP, right_w, BODY_H),
    }


def layout_three_col() -> dict:
    """3カラム均等。"""
    usable = CONTENT_W - GAP * 2
    col_w = usable / 3
    return {
        "col1": Rect(MARGIN_L, BODY_TOP, col_w, BODY_H),
        "col2": Rect(MARGIN_L + col_w + GAP, BODY_TOP, col_w, BODY_H),
        "col3": Rect(MARGIN_L + (col_w + GAP) * 2, BODY_TOP, col_w, BODY_H),
    }


def layout_top_bottom(ratio=(0.5, 0.5)) -> dict:
    """上下分割。"""
    usable = BODY_H - GAP
    top_h = usable * ratio[0]
    bottom_h = usable * ratio[1]
    return {
        "top": Rect(MARGIN_L, BODY_TOP, CONTENT_W, top_h),
        "bottom": Rect(MARGIN_L, BODY_TOP + top_h + GAP, CONTENT_W, bottom_h),
    }


def layout_card_grid(n: int) -> dict:
    """N個のカードを横並びに配置。"""
    n = max(n, 1)
    total_gap = GAP * (n - 1)
    card_w = (CONTENT_W - total_gap) / n
    return {
        f"card_{i}": Rect(
            MARGIN_L + i * (card_w + GAP), BODY_TOP, card_w, BODY_H
        )
        for i in range(n)
    }


def layout_grid_2x2() -> dict:
    """2x2グリッド。"""
    usable_w = CONTENT_W - GAP
    usable_h = BODY_H - GAP
    w = usable_w / 2
    h = usable_h / 2
    return {
        "top_left": Rect(MARGIN_L, BODY_TOP, w, h),
        "top_right": Rect(MARGIN_L + w + GAP, BODY_TOP, w, h),
        "bottom_left": Rect(MARGIN_L, BODY_TOP + h + GAP, w, h),
        "bottom_right": Rect(MARGIN_L + w + GAP, BODY_TOP + h + GAP, w, h),
    }


def layout_main_side(ratio=(0.65, 0.35)) -> dict:
    """メイン + サイドバー。"""
    return layout_two_col(ratio)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# レイアウトレジストリ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT_REGISTRY = {
    "full": layout_full,
    "two_col": lambda: layout_two_col((0.5, 0.5)),
    "two_col_wide_left": lambda: layout_two_col((0.667, 0.333)),
    "two_col_wide_right": lambda: layout_two_col((0.333, 0.667)),
    "three_col": layout_three_col,
    "top_bottom": lambda: layout_top_bottom((0.5, 0.5)),
    "card_grid": layout_card_grid,   # 引数 n が必要
    "grid_2x2": layout_grid_2x2,
    "main_side": lambda: layout_main_side((0.65, 0.35)),
}


def resolve_zones(body_layout: str, **kwargs) -> dict:
    """レイアウト名からゾーン辞書を返す。

    Args:
        body_layout: レイアウトID
        **kwargs: card_grid の n など、レイアウト固有パラメータ

    Returns:
        dict[str, Rect]: ゾーン名 → 矩形領域
    """
    fn = LAYOUT_REGISTRY.get(body_layout)
    if fn is None:
        return layout_full()

    if body_layout == "card_grid":
        return fn(kwargs.get("n", 3))
    return fn()
