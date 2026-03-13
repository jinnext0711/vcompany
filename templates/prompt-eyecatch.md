# Claude Code用プロンプト：高品質アイキャッチ画像生成

> このプロンプトをClaude Codeにそのまま貼り付けて使用してください。
> `{{...}}` の箇所を実際の内容に置き換えてから実行します。

---

## 使い方

```
# Claude Codeで以下をペーストし、{{...}} を埋めて実行

claude "$(cat prompt-eyecatch.md)"
```

---

## プロンプト本文

```markdown
あなたはグラフィックデザインとタイポグラフィの専門家です。
node-canvasを使い、note記事のアイキャッチ画像（OGP画像としても使える）を
高品質なPNG画像として生成するNode.jsスクリプトを書いてください。

# ===== コンテンツ =====

記事タイトル: {{記事のタイトルをここに記入}}
サブタイトル（任意）: {{サブタイトルやカテゴリ名。不要なら空欄}}
著者名（任意）: {{表示する場合は名前を記入。不要なら空欄}}

# ===== 画像仕様 =====

- サイズ: 1280 x 670 px（noteのアイキャッチ推奨サイズ）
- フォーマット: PNG
- DPI: 144（Retina対応）

# ===== デザインシステム（厳守） =====

## カラーパレット
- Background1: {{例: #1E2761}}（グラデーション開始色）
- Background2: {{例: #065A82}}（グラデーション終了色）
- TextPrimary: {{例: #FFFFFF}}（タイトルテキスト）
- TextSecondary: {{例: #CADCFC}}（サブタイトル・著者名）
- Accent: {{例: #F96167}}（装飾要素のアクセントカラー）

## タイポグラフィ
- タイトル: Noto Sans JP Bold、42px
  - 長いタイトル（20文字超）は自動で36pxに縮小
  - 最大2行まで（それ以上は末尾を "..." で省略）
- サブタイトル: Noto Sans JP Regular、20px
- 著者名: Noto Sans JP Regular、16px

## レイアウトルール
- 上下左右の安全マージン: 60px
- テキスト領域: 左寄せ or 中央揃え（テンプレートパターンによる）
- テキストの上下間隔: タイトル↔サブタイトル 20px、サブタイトル↔著者名 16px

# ===== テンプレートパターン =====

以下の中から記事の内容に最も合うものを1つ選んで実装すること。
選択理由をコメントで記載すること。

## パターンA: グラデーション背景 + 中央タイトル
- 背景: Background1 → Background2 の対角線グラデーション
- テキスト: 画面中央にタイトル（中央揃え）
- 装飾: 右下に半透明の幾何学パターン（円3つ + 三角形2つ、opacity 0.08〜0.15）
- 適合: 一般的な解説記事、概念紹介

## パターンB: 左右分割
- 左60%: Background1の単色面にテキスト（左揃え、左マージン80px）
- 右40%: Background2の色面に幾何学的な装飾パターン
- 境界: 斜めのカット（左下から右上への対角線、角度約15度）
- 適合: 技術記事、比較記事、How-to

## パターンC: 大きな数字 + サブタイトル
- 背景: Background1 → Background2 の上下グラデーション
- 中央上部: 巨大な数字やキーワード（120px Bold、opacity 0.15で背景装飾として）
- 中央: タイトルテキスト
- 適合: ランキング記事、「○つのTips」系

## パターンD: ノイズテクスチャ + オーバーレイ
- 背景: Background1の単色
- 全面: 微細なノイズテクスチャ（ピクセル単位のランダムドット、opacity 0.03〜0.05）
- オーバーレイ: 上部からの半透明グラデーション（黒 → 透明、opacity 0.2）
- テキスト: 下部1/3にタイトル（左揃え）
- 適合: エッセイ、思考系、ポエム的記事

## パターンE: カード風レイアウト
- 背景: Background2で全面塗り
- 中央: 白い角丸カード（角丸16px、shadow付き）、サイズ1120 x 510px
- カード内: Background1の細いアクセントバー（左端、幅6px）+ テキスト
- 適合: ビジネス記事、公式感のある記事

# ===== 装飾の品質ルール =====

## 幾何学パターンを描く場合
- 円: arc()で描画、線幅2px、色はAccentまたはTextSecondary、opacity 0.08〜0.20
- 三角形: moveTo/lineToで描画、塗りなし・線のみ
- 直線パターン: 等間隔の平行線、間隔20px、opacity 0.05〜0.10
- 要素数は5〜12個程度（多すぎるとうるさく、少なすぎると寂しい）
- テキスト領域と重ならない位置に配置する

## テキスト描画の品質ルール
- 日本語テキストのmeasureText()は不正確なことがあるため、行分割は文字数ベースで行う
  - 全角文字幅 ≒ fontSize、半角文字幅 ≒ fontSize × 0.5 で概算
  - 1行あたりの最大文字数 = (描画領域幅) / (fontSize) で計算
- テキストの影: 黒の半透明（rgba(0,0,0,0.3)）を offset (2, 2) blur 4 で入れると可読性が上がる
- 行間: fontSize × 1.5 を基本とする

# ===== フォント管理 =====

## フォントファイルの準備
```bash
# Noto Sans JPのダウンロード（Google Fontsから）
mkdir -p fonts
curl -L -o fonts/NotoSansJP-Bold.ttf \
  "https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP-Bold.ttf"
curl -L -o fonts/NotoSansJP-Regular.ttf \
  "https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP-Regular.ttf"
```

## フォント登録（スクリプト冒頭で必ず実行）
```javascript
const { registerFont, createCanvas } = require('canvas');
registerFont('./fonts/NotoSansJP-Bold.ttf', { family: 'Noto Sans JP', weight: 'bold' });
registerFont('./fonts/NotoSansJP-Regular.ttf', { family: 'Noto Sans JP', weight: 'normal' });
```

フォントのダウンロードに失敗する場合は、以下のフォールバック順で試すこと:
1. システムにインストール済みの日本語フォント（fc-list :lang=ja で確認）
2. canvas-fontsディレクトリ内の欧文フォント（日本語非対応だがレイアウト確認用に使用可能）

# ===== 実装手順（この順序で進めること） =====

## Step 1: 環境準備
```bash
npm install canvas
mkdir -p fonts
# フォントダウンロード（上記参照）
```

## Step 2: スクリプト構造
generate-eyecatch.js として以下の構造で実装:

```javascript
// 1. フォント登録
// 2. Canvas作成（1280 x 670）
// 3. 背景描画（パターンに応じた処理）
// 4. 装飾要素描画（幾何学パターン等）
// 5. テキスト描画（タイトル → サブタイトル → 著者名の順）
// 6. PNG出力
```

各ステップを個別の関数に分離し、パターン切り替えを容易にすること。

## Step 3: 生成実行
```bash
node generate-eyecatch.js
```

## Step 4: 品質検証（必須、省略禁止）
生成されたPNG画像を確認し、以下をチェック:

- [ ] テキストが安全マージン（60px）の内側に収まっているか
- [ ] テキストが途中で切れていないか
- [ ] 日本語フォントが正しく適用されているか（豆腐□になっていないか）
- [ ] 装飾要素がテキストと重なっていないか
- [ ] 背景とテキストのコントラスト比が十分か（WCAG AA基準: 4.5:1以上）
- [ ] 画像サイズが正確に1280 x 670pxか
- [ ] OGP画像として表示した場合に重要な情報がトリミングされないか
  （Twitter/Xは中央部分のみ表示されるため、タイトルは中央寄りが安全）

問題があれば修正して再生成すること。

## Step 5: バリエーション生成（任意）
同じコンテンツで複数パターンを比較したい場合:
```bash
# パターンを引数で切り替え可能にする
node generate-eyecatch.js --pattern A
node generate-eyecatch.js --pattern B
```

# ===== 出力 =====

最終ファイル: eyecatch.png
サイズ: 1280 x 670 px
```

---

## カラーパレットのプリセット集（コピペ用）

### Deep Ocean（テクノロジー・DX系）
```
- Background1: #0D1B2A
- Background2: #1B3A5C
- TextPrimary: #FFFFFF
- TextSecondary: #8ECAE6
- Accent: #219EBC
```

### Warm Gradient（ビジネス・キャリア系）
```
- Background1: #2D1B69
- Background2: #11998E
- TextPrimary: #FFFFFF
- TextSecondary: #E0E0E0
- Accent: #38EF7D
```

### Charcoal Editorial（エッセイ・思考系）
```
- Background1: #1A1A2E
- Background2: #16213E
- TextPrimary: #EAEAEA
- TextSecondary: #A0A0B0
- Accent: #E94560
```

### Soft Sage（ライフスタイル・ウェルビーイング系）
```
- Background1: #2C5F2D
- Background2: #1B4332
- TextPrimary: #F0FFF0
- TextSecondary: #97BC62
- Accent: #DAD7CD
```

### Sunset Corporate（経営・ファイナンス系）
```
- Background1: #1E2761
- Background2: #7A2048
- TextPrimary: #FFFFFF
- TextSecondary: #FFD6A5
- Accent: #F96167
```
