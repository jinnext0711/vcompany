# Claude Code用プロンプト：高品質スライド生成 v2

> 実物のスライド生成結果から学んだ失敗パターンを全て反映した改訂版。
> `{{...}}` の箇所を実際の内容に置き換えてから実行します。

---

## プロンプト本文

```markdown
あなたはプレゼンテーションデザインの専門家です。
PptxGenJSを使い、プロ品質の.pptxスライドを生成するNode.jsスクリプトを書いてください。

# ================================================================
# 最重要: 絶対に守るルール（コード生成前に3回読み返すこと）
# ================================================================

以下に違反した場合、そのスライドは不合格です。
コードを書く前に、この一覧を暗記してください。

## 絶対禁止（1つでもあれば全スライドやり直し）

1. タイトル下のアクセントライン（装飾的な水平線）を絶対に入れない
2. 装飾的な円・楕円・幾何学模様を意味なく配置しない
3. ◎ ○ △ × の記号を表のセルに使わない
4. Unicode bullet "•" を直接テキストに書かない（bullet: true を使う）
5. スライドの下半分（y > 3.5 inch）を空白にしない
6. 全セル格子罫線のテーブルを作らない

## コード生成時の必須チェック

全スライドの全要素について以下を確認:
- 最も下にある要素の (y + h) が 4.5 inch 以上であること（空白防止）
- テキストの (x + w) が 9.5 inch を超えないこと（はみ出し防止）
- 図形内のテキストが図形の幅に収まること（文字数 × 0.11 inch < 図形の幅 - 0.3）
- 全ての色コードに # を含めないこと（PptxGenJSはファイル破損する）
- shadow等のオプションオブジェクトは毎回新規作成すること（ファクトリ関数を使う）

# ================================================================
# コンテンツ
# ================================================================

タイトル: {{プレゼンのタイトル}}
対象者: {{誰に向けた発表か}}
スライド枚数の目安: {{5〜15枚など}}

スライド構成:
{{
  ここにスライドの内容を箇条書きで記述
}}

# ================================================================
# デザインシステム
# ================================================================

## カラーパレット（# なしの6桁hexで記述）
- Primary: {{例: 1E2761}}（タイトルスライド背景、見出し文字）
- Accent: {{例: F96167}}（強調ポイント）
- TextDark: {{例: 1A1A2E}}（本文テキスト）
- TextLight: {{例: FFFFFF}}（暗い背景上のテキスト）
- Surface: {{例: F8F9FA}}（コンテンツスライドの背景）
- Border: {{例: E0E0E0}}（罫線、区切り線）

## フォント
- 見出し: Georgia Bold
- 本文: Calibri Regular
- サイズ: タイトル 28-32pt / 本文 14-16pt / キャプション 10-11pt

# ================================================================
# レイアウト座標テンプレート（コピペして使うこと）
# ================================================================

LAYOUT_16x9 = 10 inch × 5.625 inch を前提とします。
以下は「空白なし」で全面を活用する座標テンプレートです。
各スライドは必ず以下のいずれかのテンプレートをベースにしてください。

## テンプレートA: タイトルスライド（暗い背景）
```javascript
// 背景
slide.background = { color: "1E2761" };
// メインタイトル（スライド中央やや上）
slide.addText("タイトル", {
  x: 0.8, y: 1.2, w: 8.4, h: 1.5,
  fontSize: 36, fontFace: "Georgia", bold: true,
  color: "FFFFFF", align: "left", valign: "middle"
});
// サブタイトル
slide.addText("サブタイトル", {
  x: 0.8, y: 2.8, w: 6.0, h: 0.8,
  fontSize: 18, fontFace: "Calibri", color: "CADCFC",
  align: "left", valign: "top"
});
// 日付や発表者名（左下）
slide.addText("2026-03-13", {
  x: 0.8, y: 4.8, w: 3.0, h: 0.4,
  fontSize: 11, fontFace: "Calibri", color: "8899BB"
});
// ★ タイトル下にアクセントラインを入れない
// ★ 右側に装飾的な円を入れない
```

## テンプレートB: チャート + 右カード（2カラム）
```javascript
// スライドタイトル（主張型: 必ず文として完結させる）
slide.addText("市場規模は年率25%で成長し2030年に160億ドルに到達", {
  x: 0.5, y: 0.3, w: 9.0, h: 0.6,
  fontSize: 20, fontFace: "Georgia", bold: true,
  color: "1E2761", align: "left", valign: "bottom", margin: 0
});
// チャート（左60%、スライド高さの70%を使い切る）
slide.addChart(pres.charts.BAR, chartData, {
  x: 0.5, y: 1.1, w: 5.5, h: 3.8,  // ★ h=3.8で下部まで使い切る
  // ... チャート設定
});
// 右カード（Big Number等）
slide.addShape(pres.shapes.RECTANGLE, {
  x: 6.3, y: 1.1, w: 3.2, h: 2.0,
  fill: { color: "F8F9FA" }
});
// ソース表記（左下）
slide.addText("Source: ...", {
  x: 0.5, y: 5.15, w: 9.0, h: 0.3,
  fontSize: 8, fontFace: "Calibri", color: "999999"
});
```

## テンプレートC: フル幅チャート
```javascript
// タイトル
slide.addText("主張型タイトル", {
  x: 0.5, y: 0.3, w: 9.0, h: 0.6,
  fontSize: 20, fontFace: "Georgia", bold: true,
  color: "1E2761", margin: 0
});
// チャート（フル幅、高さ最大活用）
slide.addChart(pres.charts.BAR, chartData, {
  x: 0.5, y: 1.1, w: 9.0, h: 3.8,  // ★ w=9.0, h=3.8 で全面活用
  // ... チャート設定
});
// ソース
slide.addText("Source: ...", {
  x: 0.5, y: 5.15, w: 9.0, h: 0.3,
  fontSize: 8, fontFace: "Calibri", color: "999999"
});
```

## テンプレートD: テーブル（コンサル品質）
```javascript
// タイトル
slide.addText("主張型タイトル", {
  x: 0.5, y: 0.3, w: 9.0, h: 0.6,
  fontSize: 20, fontFace: "Georgia", bold: true,
  color: "1E2761", margin: 0
});
// テーブル（高さを十分に取る）
const rows = [headerRow, ...dataRows, totalRow];
slide.addTable(rows, {
  x: 0.5, y: 1.1, w: 9.0,
  colW: [2.2, 1.7, 1.7, 1.7, 1.7],  // 合計 = 9.0
  border: { type: "none" },  // ★ デフォルト罫線なし
  margin: [8, 12, 8, 12],
  rowH: [0.5, 0.42, 0.42, 0.42, 0.42, 0.42, 0.42, 0.5],
  // ★ 行数 × rowH の合計が 3.5 以上になるよう調整
  autoPage: false,
});
// ソース
slide.addText("Source: ...", {
  x: 0.5, y: 5.15, w: 9.0, h: 0.3,
  fontSize: 8, fontFace: "Calibri", color: "999999"
});
```

## テンプレートE: 3カラムカード
```javascript
// タイトル
slide.addText("主張型タイトル", {
  x: 0.5, y: 0.3, w: 9.0, h: 0.6,
  fontSize: 20, fontFace: "Georgia", bold: true,
  color: "1E2761", margin: 0
});
// 3カラムのカード（等幅配置）
const cardW = 2.8, cardH = 3.6, cardY = 1.1;  // ★ h=3.6 で下部まで活用
const gap = 0.3;
const startX = 0.5;
for (let i = 0; i < 3; i++) {
  const cx = startX + i * (cardW + gap);
  // カード背景
  slide.addShape(pres.shapes.RECTANGLE, {
    x: cx, y: cardY, w: cardW, h: cardH,
    fill: { color: "F8F9FA" }
  });
  // カードタイトル（上部にアクセントバー）
  slide.addShape(pres.shapes.RECTANGLE, {
    x: cx, y: cardY, w: 0.06, h: cardH,
    fill: { color: colors[i] }  // Primary / Accent 等
  });
  // カード見出し
  slide.addText(titles[i], {
    x: cx + 0.2, y: cardY + 0.15, w: cardW - 0.4, h: 0.4,
    fontSize: 14, bold: true, color: colors[i], fontFace: "Georgia"
  });
  // カード本文（★ 十分な高さを確保）
  slide.addText(bodies[i], {
    x: cx + 0.2, y: cardY + 0.6, w: cardW - 0.4, h: 2.8,
    fontSize: 11, color: "333333", fontFace: "Calibri",
    valign: "top", lineSpacingMultiple: 1.3
  });
}
```

## テンプレートF: タイムライン / プロセスフロー
```javascript
// タイトル
slide.addText("主張型タイトル", {
  x: 0.5, y: 0.3, w: 9.0, h: 0.6,
  fontSize: 20, fontFace: "Georgia", bold: true, color: "1E2761", margin: 0
});
// タイムラインの水平線
slide.addShape(pres.shapes.LINE, {
  x: 0.8, y: 1.8, w: 8.4, h: 0,
  line: { color: "CCCCCC", width: 2 }
});
// フェーズノード（3つ）
const phases = [
  { x: 1.5, label: "Phase 1", period: "2週間", items: ["項目A", "項目B"] },
  { x: 4.5, label: "Phase 2", period: "1ヶ月", items: ["項目C", "項目D"] },
  { x: 7.5, label: "Phase 3", period: "2ヶ月", items: ["項目E", "項目F"] },
];
phases.forEach(p => {
  // ノードの円
  slide.addShape(pres.shapes.OVAL, {
    x: p.x - 0.15, y: 1.65, w: 0.3, h: 0.3,
    fill: { color: "1E2761" }
  });
  // フェーズラベル（円の上）
  slide.addText(p.label, {
    x: p.x - 1.0, y: 1.1, w: 2.0, h: 0.4,
    fontSize: 13, bold: true, color: "1E2761", align: "center"
  });
  // 期間（円の下）
  slide.addText(p.period, {
    x: p.x - 0.8, y: 2.1, w: 1.6, h: 0.35,
    fontSize: 12, bold: true, color: "333333", align: "center"
  });
  // 詳細項目（★ y=2.5 から開始し、下部まで使い切る）
  slide.addText(
    p.items.map(item => ({ text: item, options: { bullet: true, breakLine: true } })),
    {
      x: p.x - 1.2, y: 2.5, w: 2.4, h: 2.5,
      fontSize: 11, color: "555555", fontFace: "Calibri", valign: "top"
    }
  );
});
```

## テンプレートG: Big Number（1つの数字で語る）
```javascript
slide.background = { color: "F8F9FA" };
// タイトル
slide.addText("主張型タイトル", {
  x: 0.5, y: 0.3, w: 9.0, h: 0.6,
  fontSize: 20, fontFace: "Georgia", bold: true, color: "1E2761", margin: 0
});
// Big Number（中央）
slide.addText("200%", {
  x: 1.0, y: 1.5, w: 8.0, h: 1.8,
  fontSize: 72, fontFace: "Georgia", bold: true,
  color: "1E2761", align: "center", valign: "middle"
});
// コンテキスト文（Big Numberの直下）
slide.addText("導入企業の平均ROI — 投資回収期間3-6ヶ月", {
  x: 1.5, y: 3.3, w: 7.0, h: 0.6,
  fontSize: 16, fontFace: "Calibri", color: "666666", align: "center"
});
// 補足情報カード（下部に配置して空白を埋める）
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1.5, y: 4.0, w: 7.0, h: 1.0,
  fill: { color: "FFFFFF" },
  shadow: makeShadow()
});
slide.addText("Intercom: 10倍高速化 / Shopify: 92%浸透率 / 回収期間: SaaS平均の1/3", {
  x: 1.7, y: 4.1, w: 6.6, h: 0.8,
  fontSize: 12, fontFace: "Calibri", color: "555555",
  align: "center", valign: "middle"
});
```

## テンプレートH: 2x2マトリクス（ポジショニングマップ）
```javascript
// タイトル
slide.addText("主張型タイトル", {
  x: 0.5, y: 0.3, w: 9.0, h: 0.6,
  fontSize: 20, fontFace: "Georgia", bold: true, color: "1E2761", margin: 0
});
// マトリクス領域
const mX = 1.2, mY = 1.2, mW = 6.0, mH = 3.8;
// 4象限の背景
slide.addShape(pres.shapes.RECTANGLE, { x: mX, y: mY, w: mW/2, h: mH/2, fill: { color: "EBF5FB" } });
slide.addShape(pres.shapes.RECTANGLE, { x: mX+mW/2, y: mY, w: mW/2, h: mH/2, fill: { color: "E8F8F5" } });
slide.addShape(pres.shapes.RECTANGLE, { x: mX, y: mY+mH/2, w: mW/2, h: mH/2, fill: { color: "F5F5F5" } });
slide.addShape(pres.shapes.RECTANGLE, { x: mX+mW/2, y: mY+mH/2, w: mW/2, h: mH/2, fill: { color: "FEF9E7" } });
// 軸線
slide.addShape(pres.shapes.LINE, { x: mX, y: mY+mH/2, w: mW, h: 0, line: { color: "999999", width: 1 } });
slide.addShape(pres.shapes.LINE, { x: mX+mW/2, y: mY, w: 0, h: mH, line: { color: "999999", width: 1 } });
// ★ 軸ラベル（必ず4つ全て入れる）
slide.addText("← 低い　　自律性　　高い →", {
  x: mX, y: mY + mH + 0.05, w: mW, h: 0.3,
  fontSize: 10, color: "666666", align: "center"
});
slide.addText("制御性 高い ↑", {  // ★ Y軸ラベルを忘れない
  x: mX - 1.0, y: mY, w: 0.9, h: mH,
  fontSize: 10, color: "666666", align: "center", valign: "top",
  rotate: 270
});
// ★ 象限ラベル（14pt以上で読めるサイズ）
slide.addText("安全だがタスク限定", { x: mX+0.1, y: mY+0.1, w: 2.8, h: 0.3, fontSize: 10, color: "888888" });
slide.addText("高自律・高制御（最適）", { x: mX+mW/2+0.1, y: mY+0.1, w: 2.8, h: 0.3, fontSize: 10, color: "0D7C3D" });
// プロットポイント（各製品）★ テキストが円の上に被らない位置に配置
// ...（各製品のx,y座標を計算し、ラベルは円の右か下に配置）

// 右側に凡例（マトリクスの右）
slide.addText([
  { text: "● Claude Code $200/月\n", options: { color: "F96167", fontSize: 11, breakLine: true } },
  { text: "● Copilot $39/月\n", options: { color: "1E2761", fontSize: 11, breakLine: true } },
  // ...
], { x: 7.5, y: 1.5, w: 2.2, h: 2.5, valign: "top" });
```

# ================================================================
# テーブルのルール（コンサル品質）
# ================================================================

テーブルを含むスライドでは以下を厳守:

## 罫線
- border: { type: "none" } をデフォルトにする
- 横罫線のみ使用。ヘッダー下（1.5pt）と合計行上（1pt）
- 縦罫線は原則禁止
- 各データ行の下に薄い区切り線（0.5pt, E0E0E0）を入れる場合は
  borderのbottomだけ指定

## セルの書式
- 数値: 右揃え（align: "right"）
- テキスト: 左揃え（align: "left"）
- ヘッダー: 背景色 Primary, テキスト白, Bold
- 合計行: 背景色 E8EBF0, テキスト Bold
- パディング: margin: [8, 12, 8, 12] を全セルに

## 比較表で「評価」を表現する方法
- ◎○△× は絶対に使わない
- 代わりに以下を使う:
  - テキスト評価: "完全自律" / "基本的" / "限定的" / "未対応"
  - 色分け: テキスト色で差をつける
    - 最高評価: "0D7C3D"（緑）
    - 標準: "333333"（黒）
    - 限定的: "F59E0B"（オレンジ）
    - 未対応/劣位: "C62828"（赤）
  - 推奨列: 列全体の背景を "F0F4FF"（薄い青）にする

## 比較表の実装例（正しいコード）
```javascript
// ★ ◎○△×を使わない比較表
const headerRow = [
  { text: "機能", options: { fill: { color: "1E2761" }, color: "FFFFFF", bold: true, fontSize: 11, align: "left", margin: [10,12,10,16] }},
  { text: "Claude Code", options: { fill: { color: "1E2761" }, color: "FFFFFF", bold: true, fontSize: 11, align: "center" }},
  { text: "Copilot", options: { fill: { color: "1E2761" }, color: "FFFFFF", bold: true, fontSize: 11, align: "center" }},
];

// データ行 — テキスト + 色で評価を表現
const makeCell = (text, level) => {
  const colors = { best: "0D7C3D", good: "333333", limited: "F59E0B", none: "C62828" };
  return { text, options: { color: colors[level], fontSize: 10, align: "center", margin: [8,8,8,8],
    border: [{ type:"none" },{ type:"none" },{ type:"solid", pt:0.5, color:"E5E7EB" },{ type:"none" }]
  }};
};

const row1 = [
  { text: "ファイル自律操作", options: { fontSize: 10, align: "left", margin: [8,12,8,16],
    border: [{ type:"none" },{ type:"none" },{ type:"solid", pt:0.5, color:"E5E7EB" },{ type:"none" }] }},
  makeCell("完全自律", "best"),
  makeCell("限定的", "limited"),
];
```

# ================================================================
# チャートのルール
# ================================================================

## 棒グラフの色分け
- 単一系列: 全バーを Primary 色で統一。特定バーを強調する場合のみ Accent 色
- 強調バーがある場合: 凡例またはラベルで理由を明記
- 複数系列: Primary / Accent / Secondary で色分けし、凡例を必ず表示

## 必須設定
```javascript
slide.addChart(pres.charts.BAR, data, {
  x: 0.5, y: 1.1, w: 5.5, h: 3.8,  // ★ h は 3.5 以上
  barDir: "col",
  chartColors: ["1E2761", "F96167"],  // ★ # なし
  catGridLine: { style: "none" },
  valGridLine: { color: "E2E8F0", size: 0.5 },
  showValue: true,
  dataLabelPosition: "outEnd",
  dataLabelColor: "333333",
  dataLabelFontSize: 10,
  catAxisLabelColor: "666666",
  valAxisLabelColor: "666666",
  showLegend: data.length > 1,
  legendPos: "b",
});
```

# ================================================================
# 空白防止チェックリスト
# ================================================================

全スライドのコードを書き終えた後、以下を1枚ずつ検証すること:

1. 最も下にある要素の (y + h) を計算する
   - 5.15 inch 以上 → OK（ソース表記が下端にある）
   - 4.5 inch 未満 → NG: 要素を下に伸ばすか、補足情報を追加する
   
2. テキストボックスのhが内容に対して過大でないか
   - bullet 3項目で h = 3.0 inch は過大 → h = 1.5 に縮め、その分y を下げるか別要素を追加

3. カード/ボックスの内部が空白になっていないか
   - テキスト3行で h = 2.5 inch のカード → h を内容に合わせ 1.2 程度に

# ================================================================
# 実装手順
# ================================================================

## Step 1: 環境準備
```bash
npm install -g pptxgenjs
npm install react-icons react react-dom sharp  # アイコンが必要な場合
```

## Step 2: コード構造
1つのファイル generate-slides.js にまとめる。構造:
```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

// ファクトリ関数（★ オブジェクト再利用禁止）
const makeShadow = () => ({ type:"outer", color:"000000", blur:4, offset:2, angle:135, opacity:0.08 });

// === Slide 1: タイトル ===
function slide1() { /* テンプレートA使用 */ }

// === Slide 2: 市場規模 ===
function slide2() { /* テンプレートB使用 */ }

// ... 各スライドを個別関数で

// 実行
[slide1, slide2, /* ... */].forEach(fn => fn());
pres.writeFile({ fileName: "output.pptx" });
```

## Step 3: 生成
```bash
node generate-slides.js
```

## Step 4: QAエージェントによる品質検査

自分自身でQAしない。生成者は確認バイアスにより問題を見逃す。
必ずサブエージェントまたは別セッションで検査すること。

```bash
# 4-1. 画像化
python /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
rm -f slide-*.jpg
pdftoppm -jpeg -r 150 output.pdf slide

# 4-2. テキスト抽出
python -m markitdown output.pptx > slide-content.txt

# 4-3. QAエージェント起動（qa-agent-prompt.md の内容でサブエージェントを呼び出す）
# → qa-report.md が出力される
```

QAエージェントは qa-agent-prompt.md に定義された専用ロールで動作する。
検査項目: 空白チェック / 禁止パターン / テーブル品質 / チャート品質 / タイポグラフィ / コンテンツ

## Step 5: 修正と再検査

qa-report.md の結果に基づき修正:
- Critical: 全て修正必須（1件でもあれば再生成レベル）
- Major: 全て修正必須
- Minor: 可能な限り修正

修正後、Step 3 → Step 4 を再実行。
全 Critical と Major がゼロになるまでループ。
最低1回はfix-and-verifyサイクルを完了すること。

## Step 6: ユーザーへの最終提示

最終版の画像とqa-report.mdをユーザーに提示し、フィードバックを求める。

# ================================================================
# 出力
# ================================================================

最終ファイル: output.pptx
検証画像: slide-*.jpg
品質レポート: qa-report.md
```

---

## カラーパレットのプリセット集（コピペ用）

### Midnight Executive（ビジネス・経営層向け）
```
Primary: 1E2761 / Accent: F96167 / TextDark: 1A1A2E
TextLight: FFFFFF / Surface: F0F4F8 / Border: E0E0E0
```

### Teal Trust（テクノロジー・DX系）
```
Primary: 028090 / Accent: 02C39A / TextDark: 0D1B2A
TextLight: FFFFFF / Surface: F0FAFA / Border: D1E8E8
```

### Charcoal Minimal（汎用・ミニマル）
```
Primary: 36454F / Accent: 212121 / TextDark: 212121
TextLight: FFFFFF / Surface: FAFAFA / Border: E0E0E0
```
