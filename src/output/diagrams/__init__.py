"""図解レンダラーレジストリ。

各図解レンダラーは以下のシグネチャに従う:
    render_xxx(slide, rect: Rect, data: dict, design: DesignConfig) -> None

rect はレイアウトが決めたゾーン領域。レンダラーはその中に収まるよう描画する。
"""

from src.output.diagrams.structured_text import render_structured_text
from src.output.diagrams.bullet_list import render_bullet_list
from src.output.diagrams.table import render_table
from src.output.diagrams.flow import render_flow
from src.output.diagrams.pyramid import render_pyramid
from src.output.diagrams.matrix import render_matrix
from src.output.diagrams.bar_chart import render_bar_chart
from src.output.diagrams.waterfall import render_waterfall
from src.output.diagrams.funnel import render_funnel
from src.output.diagrams.cycle import render_cycle
from src.output.diagrams.stacked_bar import render_stacked_bar
from src.output.diagrams.timeline import render_timeline
from src.output.diagrams.kpi_card import render_kpi_card
from src.output.diagrams.comparison_panel import render_comparison_panel

DIAGRAM_REGISTRY = {
    "structured_text": render_structured_text,
    "bullet_list": render_bullet_list,
    "table": render_table,
    "flow": render_flow,
    "pyramid": render_pyramid,
    "matrix": render_matrix,
    "bar_chart": render_bar_chart,
    "waterfall": render_waterfall,
    "funnel": render_funnel,
    "cycle": render_cycle,
    "stacked_bar": render_stacked_bar,
    "timeline": render_timeline,
    "kpi_card": render_kpi_card,
    "comparison_panel": render_comparison_panel,
}
