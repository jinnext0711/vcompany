"""Phase 4: デザインモジュール - デザイン設定の管理"""


class DesignConfig:
    """資料のデザイン設定を管理する。"""

    # デフォルトカラーパレット
    DEFAULT_COLORS = {
        "primary": "1F4E79",       # メインカラー（濃い青）
        "secondary": "2E75B6",     # サブカラー（青）
        "accent": "ED7D31",        # アクセントカラー（オレンジ）
        "text": "333333",          # テキストカラー
        "background": "FFFFFF",    # 背景色
        "light_bg": "F2F2F2",      # 薄い背景色
    }

    # デフォルトフォント設定
    DEFAULT_FONTS = {
        "title": {"name": "Yu Gothic", "size": 28, "bold": True},
        "subtitle": {"name": "Yu Gothic", "size": 18, "bold": False},
        "heading": {"name": "Yu Gothic", "size": 24, "bold": True},
        "body": {"name": "Yu Gothic", "size": 14, "bold": False},
        "caption": {"name": "Yu Gothic", "size": 10, "bold": False},
    }

    def __init__(self, colors: dict = None, fonts: dict = None):
        self.colors = {**self.DEFAULT_COLORS, **(colors or {})}
        self.fonts = {**self.DEFAULT_FONTS, **(fonts or {})}

    def get_color_rgb(self, color_key: str) -> tuple:
        """カラーキーからRGBタプルを返す。"""
        hex_color = self.colors.get(color_key, self.colors["text"])
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )
