"""PowerPoint出力エクスポーター — コンサルティング品質（KPMG型）v3

レイアウト × 図解 分離アーキテクチャ:
  - レイアウト: ボディ領域のゾーン分割（layouts.py）
  - 図解: ゾーン内に描画されるコンテンツ（diagrams/）
  - 特殊スライド: title, agenda, section_divider, executive_summary, summary

新スキーマ（slide_type + body_layout + zones）とレガシースキーマ（layout）の
両方をサポートし、後方互換性を維持する。

■ ヘッダー3層:
  スライドタイトル（トピック名, 14pt Bold）
  + リード文/メッセージ（So What主張文, 16pt）
  + 区切り線

■ ボディ: レイアウト(ゾーン(図解)) — スライドの70%以上
■ フッター: 出典 + ページ番号

デザイン方針:
  - KPMG型: タイトルとメッセージ（リード文）を分離
  - 白ベース背景 + 70-25-5配色ルール
  - Noto Sans JP 1フォント、ウェイトで階層表現
  - 8pxグリッド準拠のスペーシング
  - WCAG AA コントラスト比
"""

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches

from src.design.builder import DesignConfig
from src.output.helpers import (
    _text_box, _add_header, _add_footer, _add_notes,
    _blank_slide, _c,
    SLIDE_W, SLIDE_H, MARGIN_L, CONTENT_W, BODY_TOP, BODY_H,
    FOOTER_TOP, FOOTER_H, FS_FOOTER,
    PP_ALIGN,
)
from src.output.layouts import Rect, resolve_zones, layout_full
from src.output.diagrams import DIAGRAM_REGISTRY
from src.output.special_slides import (
    add_title_slide,
    SPECIAL_SLIDE_HANDLERS,
)

from pptx.dml.color import RGBColor


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# レガシー互換マッピング
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 旧 layout 値 → (slide_type, body_layout, diagram_id, data_remap関数)
def _identity(section):
    """セクションデータをそのまま返す。"""
    return section


def _remap_two_column(section):
    """two_column レガシーデータを zones 形式に変換する。"""
    left = section.get("left_column", {})
    right = section.get("right_column", {})
    return {
        "zones": {
            "left": {"diagram": "comparison_panel", "data": {**left, "accent": "light_text"}},
            "right": {"diagram": "comparison_panel", "data": {**right, "accent": "highlight"}},
        }
    }


def _remap_comparison(section):
    """comparison レガシーデータを zones 形式に変換する。"""
    left = section.get("comparison_left", {})
    right = section.get("comparison_right", {})
    return {
        "zones": {
            "left": {"diagram": "comparison_panel", "data": {**left, "accent": "light_text"}},
            "right": {"diagram": "comparison_panel", "data": {**right, "accent": "highlight"}},
        }
    }


_LEGACY_MAP = {
    # (slide_type, body_layout, default_diagram, data_remap)
    "structured_text": ("content", "full", "structured_text", _identity),
    "table":           ("content", "full", "table", lambda s: s.get("table", s)),
    "flow":            ("content", "full", "flow", _identity),
    "kpi":             ("content", "full", "kpi_card", _identity),
    "two_column":      ("content", "two_col", None, _remap_two_column),
    "comparison":      ("content", "two_col", None, _remap_comparison),
    "matrix":          ("content", "full", "matrix", lambda s: s.get("matrix", s)),
    "bar_chart":       ("content", "full", "bar_chart", lambda s: s.get("chart_data", s)),
    "pyramid":         ("content", "full", "pyramid", _identity),
    "timeline":        ("content", "full", "timeline", _identity),
    "waterfall":       ("content", "full", "waterfall", _identity),
    "funnel":          ("content", "full", "funnel", _identity),
    "cycle":           ("content", "full", "cycle", _identity),
    "stacked_bar":     ("content", "full", "stacked_bar", _identity),
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# コンポーザブルコンテンツスライド
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _add_content_slide(prs, section, design, page_num):
    """コンポーザブルコンテンツスライド: ヘッダー + レイアウト(ゾーン(図解)) + フッター。"""
    slide = _blank_slide(prs)
    _add_header(slide, section, design)

    # ゾーン解決
    body_layout = section.get("body_layout", "full")
    zones = resolve_zones(body_layout, n=section.get("card_count", 3))

    # 各ゾーンに図解を描画
    zone_specs = section.get("zones", {})

    # ゾーン名エイリアス: コンテンツ側の名前 → レイアウト側の名前にマッピング
    _ZONE_ALIASES = {
        "main": ["main", "left", "col1"],
        "side": ["right", "col2"],
        "left": ["left", "col1"],
        "center": ["col2"],
        "right": ["right", "col3", "col2"],
    }
    # zone_specs のキーを zones のキーにマッチさせる
    resolved_specs = {}
    for zone_name in zones:
        if zone_name in zone_specs:
            resolved_specs[zone_name] = zone_specs[zone_name]
        else:
            # エイリアスから探す
            for spec_key, aliases in _ZONE_ALIASES.items():
                if zone_name in aliases and spec_key in zone_specs:
                    resolved_specs[zone_name] = zone_specs[spec_key]
                    break

    for zone_name, rect in zones.items():
        spec = resolved_specs.get(zone_name)
        if spec is None:
            continue
        diagram_id = spec.get("diagram", "structured_text")
        renderer = DIAGRAM_REGISTRY.get(diagram_id)
        if renderer:
            renderer(slide, rect, spec.get("data", {}), design)

    _add_footer(slide, section.get("source", ""), design, page_num)
    _add_notes(slide, section)


def _add_content_slide_legacy(prs, section, design, page_num):
    """レガシー形式のコンテンツスライド。旧 layout 値を新形式に変換して描画。"""
    layout = section.get("layout", "structured_text")
    mapping = _LEGACY_MAP.get(layout)
    if mapping is None:
        # 不明な layout → structured_text として処理
        mapping = _LEGACY_MAP["structured_text"]

    slide_type, body_layout, default_diagram, data_remap = mapping

    slide = _blank_slide(prs)
    _add_header(slide, section, design)

    # ゾーン解決
    if body_layout == "full" and default_diagram:
        zones = resolve_zones("full")
        remapped = data_remap(section)
        renderer = DIAGRAM_REGISTRY.get(default_diagram)
        if renderer:
            renderer(slide, zones["main"], remapped, design)
    else:
        # two_column/comparison → 既にゾーン形式に変換済み
        remapped = data_remap(section)
        zone_specs = remapped.get("zones", {})
        zones = resolve_zones(body_layout)
        for zone_name, rect in zones.items():
            spec = zone_specs.get(zone_name)
            if spec is None:
                continue
            diagram_id = spec.get("diagram", "structured_text")
            renderer = DIAGRAM_REGISTRY.get(diagram_id)
            if renderer:
                renderer(slide, rect, spec.get("data", {}), design)

    _add_footer(slide, section.get("source", ""), design, page_num)
    _add_notes(slide, section)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# メインエクスポート関数
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def export_pptx(content, output_path, design=None):
    """コンテンツJSONからPPTXを生成する。

    新スキーマ（slide_type + body_layout + zones）と
    レガシースキーマ（layout）の両方をサポート。
    """
    if design is None:
        design = DesignConfig()

    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)

    # タイトルスライド
    add_title_slide(prs, content, design)

    page_num = 1
    for section in content.get("sections", []):
        # 新スキーマ: slide_type を優先
        slide_type = section.get("slide_type")

        if slide_type:
            # 新スキーマ
            handler = SPECIAL_SLIDE_HANDLERS.get(slide_type)
            if handler:
                # special handler がコンテンツを持たない場合（zonesのみ）→ contentとして処理
                has_special_content = any(
                    section.get(k) for k in
                    ("conclusion", "key_points", "bullet_points",
                     "agenda_items", "key_takeaways", "next_steps",
                     "section_number")
                )
                if has_special_content or slide_type in ("title", "section_divider"):
                    handler(prs, section, design)
                else:
                    # zonesデータはあるがspecial用データがない → contentとして描画
                    _add_content_slide(prs, section, design, page_num)
            elif slide_type == "content":
                _add_content_slide(prs, section, design, page_num)
            else:
                # 不明な slide_type → コンテンツとして処理
                _add_content_slide(prs, section, design, page_num)
        else:
            # レガシースキーマ: layout を使用
            layout = section.get("layout", "structured_text")
            special_handler = SPECIAL_SLIDE_HANDLERS.get(layout)
            if special_handler:
                special_handler(prs, section, design)
            elif layout in _LEGACY_MAP:
                _add_content_slide_legacy(prs, section, design, page_num)
            else:
                _add_content_slide_legacy(prs, section, design, page_num)

        page_num += 1

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    prs.save(output_path)
    return output_path
