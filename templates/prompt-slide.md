# Claude Code用プロンプト：高品質スライド生成

> このプロンプトをClaude Codeにそのまま貼り付けて使用してください。
> `{{...}}` の箇所を実際の内容に置き換えてから実行します。

---

## 使い方

```
# Claude Codeで以下をペーストし、{{...}} を埋めて実行

claude "$(cat prompt-slide.md)"
```

---

## プロンプト本文

```markdown
あなたはプレゼンテーションデザインの専門家です。
PptxGenJSを使い、プロ品質の.pptxスライドを生成するNode.jsスクリプトを書いてください。

# ===== コンテンツ =====

タイトル: {{プレゼンのタイトル}}
対象者: {{誰に向けた発表か}}
スライド枚数の目安: {{5〜15枚など}}

スライド構成:
{{
  ここにスライドの内容を箇条書きで記述。例：
  1. タイトルスライド: メインタイトル + サブタイトル + 発表者名
  2. 課題提起: 現状の課題を3点
  3. 解決策: 提案するソリューション概要
  4. 詳細1: ...
  5. 詳細2: ...
  6. まとめ: 要点の振り返り + CTA
}}

# ===== デザインシステム（厳守） =====

## カラーパレット
- Primary: {{例: #1E2761}}（タイトルスライド背景、見出し文字）
- Secondary: {{例: #CADCFC}}（コンテンツスライド背景のアクセント）
- Accent: {{例: #F96167}}（強調ポイント、CTA）
- TextDark: {{例: #1A1A2E}}（本文テキスト）
- TextLight: {{例: #FFFFFF}}（暗い背景上のテキスト）
- Surface: {{例: #F8F9FA}}（コンテンツスライドの背景）

## タイポグラフィ
- 見出しフォント: Georgia Bold
- 本文フォント: Calibri
- タイトルスライドの見出し: 40pt Bold
- コンテンツスライドの見出し: 28pt Bold
- 本文: 16pt Regular
- キャプション・注釈: 11pt、色は #888888

## レイアウトルール
- スライドサイズ: LAYOUT_16x9（10" x 5.625"）
- 余白: 上下左右 0.5inch以上
- 要素間のスペーシング: 0.3inch以上
- タイトルは左揃え（中央揃えはタイトルスライドのみ許可）
- テキストボックスのmarginは用途に応じて0に設定し、他要素との位置揃えを正確にする

# ===== スライド設計の必須ルール =====

## 構造ルール
- タイトルスライドと最終スライドは暗い背景（Primary色）、中間スライドは明るい背景（Surface色）
- 全スライドにビジュアル要素（図形・アイコン・チャート・数字のハイライト）を必ず含める
- テキストのみのスライドは絶対に作らない
- 同じレイアウトパターンを3スライド以上連続させない
- bullet pointは1スライドあたり最大5項目

## レイアウトバリエーション（以下から組み合わせる）
- 2カラム（左テキスト + 右ビジュアル）
- アイコン + テキスト行（色付き丸の中にアイコン、横にテキスト）
- 大きな数字のコールアウト（60-72pt数字 + 小さなラベル）
- 2x2グリッド（4つの要素を均等配置）
- タイムライン / プロセスフロー（番号付きステップ + 矢印）
- 比較カラム（Before/After、左右対比）

## 図形・装飾ルール
- ROUNDED_RECTANGLEとRECTANGLEのアクセントバーを組み合わせない（角が合わない）
- shadow設定はファクトリ関数で毎回新しいオブジェクトを生成する（PptxGenJSがオブジェクトを破壊的に変更するため）
- hexカラーに # を含めない（ファイル破損の原因）
- 8桁hexでopacityを表現しない（opacityプロパティを使う）

## やってはいけないこと
- タイトル下のアクセントライン（AI生成スライドの典型パターン）
- Unicode bullet（"•"）の直接使用（bullet: true を使う）
- lineSpacingとbulletの併用（paraSpaceAfterを使う）
- デフォルトフォント（Arial単体）のみの使用
- 紫グラデーション背景（AI生成の典型パターン）
- 全スライド同じレイアウトの繰り返し
- 低コントラストなテキスト（明るい背景に薄いグレー等）

# ===== チャートがある場合 =====

チャートを含むスライドでは以下を適用:
- chartColorsにデザインシステムのカラーパレットを使う
- catGridLineは非表示（style: "none"）
- valGridLineは薄い色（#E2E8F0, size: 0.5）
- データラベルを表示（showValue: true, dataLabelPosition: "outEnd"）
- 単一系列ならlegendは非表示

# ===== アイコン =====

アイコンが必要な場合:
- react-iconsからSVGを取得し、sharpでPNGにラスタライズしてbase64で埋め込む
- サイズ256px以上でレンダリングし、スライド上では0.4〜0.6inchで表示
- npm install: react-icons react react-dom sharp

# ===== 実装手順（この順序で進めること） =====

## Step 1: 環境準備
```bash
npm install -g pptxgenjs
npm install react-icons react react-dom sharp
```

## Step 2: スクリプト作成
- 1つのNode.jsファイル（generate-slides.js）にまとめる
- shadow等の共通スタイルはファクトリ関数で定義
- スライドごとに関数を分離し、レイアウトバリエーションを明示的に切り替える

## Step 3: 生成実行
```bash
node generate-slides.js
```

## Step 4: 品質検証（必須、省略禁止）
```bash
# PDF変換
python scripts/office/soffice.py --headless --convert-to pdf output.pptx

# 画像化
rm -f slide-*.jpg
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

生成された画像を1枚ずつ確認し、以下の問題を検出すること:
- テキストの重なり・はみ出し・切れ
- 要素間の距離が0.3inch未満
- スライド端との余白が0.5inch未満
- 低コントラスト（背景色とテキスト色が近い）
- レイアウトの不均衡（一方に偏った配置）
- テンプレートのプレースホルダテキストの残存

## Step 5: 修正と再検証
- 発見した問題を修正
- Step 4を再実行して修正を確認
- 全スライドで問題がなくなるまで繰り返す

# ===== 出力 =====

最終ファイル: output.pptx
検証済みのスライド画像も併せて出力すること。
```

---

## カラーパレットのプリセット集（コピペ用）

必要に応じてデザインシステムのカラーパレット部分を以下に置き換えてください。

### Midnight Executive（ビジネス・経営層向け）
```
- Primary: #1E2761
- Secondary: #CADCFC
- Accent: #FFFFFF
- TextDark: #1A1A2E
- TextLight: #FFFFFF
- Surface: #F0F4F8
```

### Forest & Moss（環境・サステナビリティ系）
```
- Primary: #2C5F2D
- Secondary: #97BC62
- Accent: #F5F5F5
- TextDark: #1B3A1C
- TextLight: #FFFFFF
- Surface: #F5F7F3
```

### Warm Terracotta（カルチャー・クリエイティブ系）
```
- Primary: #B85042
- Secondary: #E7E8D1
- Accent: #A7BEAE
- TextDark: #3D1F18
- TextLight: #FFFFFF
- Surface: #FAF8F2
```

### Teal Trust（テクノロジー・DX系）
```
- Primary: #028090
- Secondary: #00A896
- Accent: #02C39A
- TextDark: #0D1B2A
- TextLight: #FFFFFF
- Surface: #F0FAFA
```

### Charcoal Minimal（汎用・ミニマル）
```
- Primary: #36454F
- Secondary: #F2F2F2
- Accent: #212121
- TextDark: #212121
- TextLight: #FFFFFF
- Surface: #FAFAFA
```
