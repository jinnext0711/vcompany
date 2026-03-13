---
paths:
  - "**/*.html"
  - "output/html/**"
---

# HTMLレポート・ダッシュボードの作成ルール

## 基本構造
- 単一HTMLファイルとして完結させる（CSS・JSはインライン）
- 画像はBase64エンコードで埋め込む（外部依存をなくす）
- CDNからの外部ライブラリ読み込みは https://cdnjs.cloudflare.com のみ許可
- 文字コードはUTF-8を指定する
- lang属性は"ja"を設定する

## レスポンシブ対応
- max-width: 1200px のコンテナで中央配置する
- タブレット（768px）以上で最適化する
- @media print を定義し、印刷時にもレイアウトが崩れないようにする
- 印刷時はナビゲーション、フィルタ、インタラクティブ要素を非表示にする

## デザイン（CSS変数）
```css
:root {
  --color-primary: #2E5090;
  --color-accent: #E67E22;
  --color-text: #333333;
  --color-bg: #FFFFFF;
  --color-bg-sub: #F5F7FA;
  --color-border: #E0E0E0;
  --color-success: #27AE60;
  --color-warning: #F39C12;
  --color-error: #E74C3C;
  --font-main: "Noto Sans JP", "Hiragino Sans", "Meiryo", sans-serif;
}
```

## レイアウト構成
- エグゼクティブサマリー: 1カラム、セクションごとにカードで区切る
- ダッシュボード: 2-3カラムのグリッドレイアウト
- レポート: 1カラム、目次 + セクション形式

## グラフ・可視化
- Chart.jsをCDNから読み込んで使用する
- グラフには必ずタイトル・凡例・単位を表示する
- カラーパレットはCSS変数と統一する
- ツールチップで詳細値を表示する
- 印刷時はグラフをそのまま画像として出力されるよう canvas を使う

## テーブル
- ヘッダー行に背景色（--color-primary、文字白）を設定する
- 偶数行にストライプ背景（--color-bg-sub）を設定する
- セル内のpaddingは 12px 16px を基本とする
- 数値は右揃え、テキストは左揃えにする
- 横スクロール対応: overflow-x: auto のラッパーで囲む

## 社外提出時の追加ルール
- ページ上部にロゴエリアと「Confidential」バッジを配置する
- フッターに作成日・作成者・バージョンを表示する
- 印刷時にヘッダー・フッターが各ページに出力されるようにする

## アクセシビリティ
- 画像にはalt属性を必ず設定する
- フォームにはlabel要素を対応させる
- カラーのみに依存しない情報伝達（アイコン・テキスト補助）を行う
- WAI-ARIA属性を適切に設定する（role, aria-label等）
