"""Phase 4: デザインモジュール - デザイン設定の管理

デザインルール（docs/design-rules.md）に準拠した設定を提供する。
"""


class DesignConfig:
    """資料のデザイン設定を管理する。

    禁止事項:
    - デフォルトフォント（Inter, Arial, Calibri等）の使用禁止
    - 無駄なアニメーションの使用禁止
    - グラデーションの使用禁止（フラットカラーのみ）
    - アイコンの過剰使用禁止
    """

    # カラーパレット（フラットカラーのみ、グラデーション禁止）
    DEFAULT_COLORS = {
        "primary": "1A1A2E",       # 濃紺 — ヘッダー、見出し
        "secondary": "16213E",     # スレートブルー — サブヘッダー
        "accent": "0F3460",        # ティール — アクセント
        "highlight": "53868B",     # シアン — ハイライト、数値強調
        "text": "2D2D2D",          # ダークグレー — 本文
        "light_text": "6B6B6B",    # ミディアムグレー — キャプション
        "background": "FFFFFF",    # ホワイト — 背景
        "light_bg": "F5F5F5",      # ライトグレー — セクション背景
        "border": "E0E0E0",        # ボーダーグレー — 区切り線
    }

    # フォント設定（デフォルトフォント使用禁止）
    DEFAULT_FONTS = {
        "title": {"name": "Noto Sans JP", "size": 32, "bold": True},
        "heading": {"name": "Noto Sans JP", "size": 24, "bold": True},
        "subheading": {"name": "Noto Sans JP", "size": 18, "bold": False},
        "body": {"name": "Noto Sans JP", "size": 14, "bold": False},
        "caption": {"name": "Noto Sans JP", "size": 10, "bold": False},
        "data": {"name": "Noto Sans JP", "size": 20, "bold": True},
    }

    # レイアウト設定（インチ単位）
    LAYOUT = {
        "slide_width": 13.333,     # 16:9
        "slide_height": 7.5,
        "margin_top": 0.8,
        "margin_bottom": 0.8,
        "margin_left": 0.8,
        "margin_right": 0.8,
        "content_gap": 0.3,
        "max_bullet_items": 5,
        "header_height": 1.0,
    }

    # 禁止フォントリスト
    PROHIBITED_FONTS = [
        "Inter", "Arial", "Calibri", "MS Gothic", "MS PGothic",
        "MS Mincho", "MS PMincho", "Times New Roman", "Courier New",
        "Comic Sans MS", "Impact",
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
                    f"Noto Sans JP 等の指定フォントを使用してください。"
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
