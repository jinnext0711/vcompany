"""Phase 4: デザインモジュール - デザイン設定の管理

デザインルール（docs/design-rules.md）に準拠した設定を提供する。
WCAG AA準拠、Tufte原則、8pxグリッド基準。
"""


class DesignConfig:
    """資料のデザイン設定を管理する。

    禁止事項:
    - デフォルトフォント（Inter, Arial, Calibri等）の使用禁止
    - 無駄なアニメーションの使用禁止
    - グラデーションの使用禁止（フラットカラーのみ）
    - アイコンの過剰使用禁止
    - チャートジャンク禁止
    - 色のみによる情報伝達禁止
    """

    # カラーパレット — 基本4色 + 補助4色
    DEFAULT_COLORS = {
        # 基本カラー（常用4色）
        "primary": "1A1A2E",       # 濃紺 — ヘッダー、見出し（白背景でコントラスト比 15.4:1 AAA）
        "highlight": "53868B",     # シアン — アクセント（白背景で 3.9:1 AA大テキスト）
        "text": "2D2D2D",          # ダークグレー — 本文（白背景で 12.6:1 AAA）
        "background": "FFFFFF",    # ホワイト — 背景
        # 補助カラー（必要時のみ）
        "secondary": "16213E",     # スレートブルー — サブヘッダー
        "light_text": "6B6B6B",    # ミディアムグレー — キャプション（白背景で 5.0:1 AA）
        "light_bg": "F5F5F5",      # ライトグレー — セクション背景
        "border": "E0E0E0",        # ボーダーグレー — 区切り線
    }

    # グラフ・図表用カラー（最大4色、データインク比を意識）
    CHART_COLORS = [
        "1A1A2E",  # 主要データ
        "53868B",  # 比較データ
        "6B6B6B",  # 補助データ
        "E0E0E0",  # 背景・参考データ
    ]

    # フォント設定 — Noto Sans JP の1種類のみ、ウェイトで階層表現
    # プレゼンスライド用サイズ
    DEFAULT_FONTS = {
        "title": {"name": "Noto Sans JP", "size": 36, "bold": True, "line_spacing": 1.2},
        "heading": {"name": "Noto Sans JP", "size": 28, "bold": True, "line_spacing": 1.2},
        "subheading": {"name": "Noto Sans JP", "size": 20, "bold": False, "line_spacing": 1.3},
        "body": {"name": "Noto Sans JP", "size": 18, "bold": False, "line_spacing": 1.5},
        "caption": {"name": "Noto Sans JP", "size": 12, "bold": False, "line_spacing": 1.5},
        "data": {"name": "Noto Sans JP", "size": 40, "bold": True, "line_spacing": 1.0},
    }

    # ドキュメント（HTML/PDF）用サイズ
    DOCUMENT_FONTS = {
        "h1": {"size_px": 32, "weight": 700, "line_height": 1.2},
        "h2": {"size_px": 24, "weight": 700, "line_height": 1.3},
        "h3": {"size_px": 18, "weight": 500, "line_height": 1.3},
        "body": {"size_px": 16, "weight": 400, "line_height": 1.8},
        "caption": {"size_px": 12, "weight": 400, "line_height": 1.5},
    }

    # スペーシング（8pxグリッド基準、IBM Carbon準拠）
    SPACING = {
        "spacing-01": 2,    # 微細な調整
        "spacing-02": 4,    # アイコンとテキストの間
        "spacing-03": 8,    # 基本単位
        "spacing-04": 12,   # ラベルとフィールドの間
        "spacing-05": 16,   # 標準パディング
        "spacing-06": 24,   # セクション内の余白
        "spacing-07": 32,   # セクション間の余白
        "spacing-08": 40,   # 大きなセクション間の余白
        "spacing-09": 48,   # ページ上下のマージン
    }

    # レイアウト設定（インチ単位）
    LAYOUT = {
        "slide_width": 13.333,     # 16:9
        "slide_height": 7.5,
        "margin_top": 0.8,         # ≒48px (spacing-09)
        "margin_bottom": 0.8,
        "margin_left": 0.8,
        "margin_right": 0.8,
        "content_gap": 0.4,        # ≒24px (spacing-06)
        "max_bullet_items": 5,
        "max_body_lines": 3,
        "header_height": 1.0,
    }

    # テキストルール
    TEXT_RULES = {
        "max_chars_per_line_ja": 40,   # 日本語1行最大文字数
        "max_chars_per_line_en": 75,   # 英語1行最大文字数
        "text_align": "left",          # 左揃え（均等揃え禁止）
        "bullet_marker": "—",          # 箇条書き行頭記号
        "paragraph_spacing_ratio": 2.0, # 段落間スペース = フォントサイズ × 2
    }

    # WCAG AA コントラスト比の最低基準
    CONTRAST_REQUIREMENTS = {
        "normal_text": 4.5,    # 通常テキスト
        "large_text": 3.0,     # 大テキスト（18pt以上 / 太字14pt以上）
        "ui_component": 3.0,   # UIコンポーネント
    }

    # 禁止フォントリスト
    PROHIBITED_FONTS = [
        "Inter", "Arial", "Calibri", "MS Gothic", "MS PGothic",
        "MS Mincho", "MS PMincho", "Times New Roman", "Courier New",
        "Comic Sans MS", "Impact", "Yu Gothic",
    ]

    def __init__(self, colors: dict = None, fonts: dict = None):
        self.colors = {**self.DEFAULT_COLORS, **(colors or {})}
        self.fonts = {**self.DEFAULT_FONTS, **(fonts or {})}
        self._validate_fonts()

    def _validate_fonts(self):
        """禁止フォントが使用されていないか検証する。"""
        for key, font_config in self.fonts.items():
            font_name = font_config.get("name", "")
            if font_name in self.PROHIBITED_FONTS:
                raise ValueError(
                    f"禁止フォント '{font_name}' が {key} に指定されています。"
                    f"Noto Sans JP を使用してください。"
                )

    def get_color_rgb(self, color_key: str) -> tuple:
        """カラーキーからRGBタプルを返す。"""
        hex_color = self.colors.get(color_key, self.colors["text"])
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )

    def get_font(self, font_key: str) -> dict:
        """フォントキーからフォント設定を返す。"""
        return self.fonts.get(font_key, self.fonts["body"])

    def get_chart_color_rgb(self, index: int) -> tuple:
        """グラフ用カラーをインデックスで取得する。"""
        hex_color = self.CHART_COLORS[index % len(self.CHART_COLORS)]
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )

    @staticmethod
    def calc_contrast_ratio(hex_fg: str, hex_bg: str) -> float:
        """2色のコントラスト比を計算する（WCAG基準）。"""
        def relative_luminance(hex_color: str) -> float:
            r, g, b = (
                int(hex_color[0:2], 16) / 255,
                int(hex_color[2:4], 16) / 255,
                int(hex_color[4:6], 16) / 255,
            )
            r = r / 12.92 if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
            g = g / 12.92 if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
            b = b / 12.92 if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4
            return 0.2126 * r + 0.7152 * g + 0.0722 * b

        l1 = relative_luminance(hex_fg)
        l2 = relative_luminance(hex_bg)
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)
