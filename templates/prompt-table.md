# Claude Code用プロンプト：コンサルティングファーム品質の表・テーブル生成

> このプロンプトをClaude Codeにそのまま貼り付けて使用してください。
> `{{...}}` の箇所を実際の内容に置き換えてから実行します。
>
> 対応出力形式: スライド(.pptx) / HTML / Excel(.xlsx) / SVG

---

## 使い方

```
# Claude Codeで以下をペーストし、{{...}} を埋めて実行

claude "$(cat prompt-table.md)"
```

---

## プロンプト本文

```markdown
あなたはMcKinsey・BCG・Bainレベルの戦略コンサルティングファームで
10年以上の経験を持つスライド/資料デザインのエキスパートです。
コンサルファーム品質のテーブル（表）を生成してください。

コンサルファームの表は「データを一瞬で理解させる」ために存在します。
装飾ではなく情報伝達の精度と速度が品質基準です。

# ===== コンテンツ =====

表のタイトル: {{表のタイトル}}
表の目的: {{この表で何を伝えたいか。比較？推移？構成比？ランキング？}}

データ:
{{
  ここに表のデータを記述。例：

  | 項目 | FY2023 | FY2024 | FY2025E | YoY成長率 |
  |------|--------|--------|---------|----------|
  | 売上高 | 1,200 | 1,450 | 1,680 | +15.9% |
  | 営業利益 | 180 | 220 | 275 | +25.0% |
  | 営業利益率 | 15.0% | 15.2% | 16.4% | +1.2pt |

  または自然言語で:
  - 3つのサービスの比較表を作りたい
  - 列: サービス名、月額費用、ユーザー数上限、主な機能、おすすめ度
}}

出力形式: {{pptx / html / xlsx / svg から1つ選択}}

# ===== コンサル品質テーブルの絶対ルール =====

以下のルールはMcKinsey・BCGの実際のスライドから抽出した
デザイン原則です。例外なく厳守すること。

## 原則1: ボーダー（罫線）のミニマリズム

コンサル品質の表は「罫線が少ないほど上質」です。

```
【最悪】全セル格子罫線（Excelデフォルト）
┌────┬────┬────┐
│    │    │    │
├────┼────┼────┤   ← 絶対にやらない
│    │    │    │
└────┴────┴────┘

【標準】水平罫線のみ（コンサル標準）
─────────────────
  Header  Header  Header
─────────────────
  Data    Data    Data
  Data    Data    Data
─────────────────
  Total   Total   Total
═════════════════

【上級】ヘッダー下 + 合計上のみ
  Header  Header  Header
─────────────────
  Data    Data    Data
  Data    Data    Data
─────────────────
  Total   Total   Total
```

実装ルール:
- 縦罫線は原則として使用禁止
- 横罫線はヘッダー下（太め: 1.5〜2pt）と合計行上（細め: 0.75〜1pt）のみ
- セル間の区切りは罫線ではなく「余白」で表現する
- 表の外枠（上下左右）の太い罫線も禁止
- 罫線色は黒ではなくグレー系（#333333〜#666666）

## 原則2: ヘッダーの設計

ヘッダー行は表全体の印象を決める最重要要素です。

パターンA「ダークヘッダー」（推奨）:
- 背景: 濃い色（Primary色）
- テキスト: 白、Bold、12〜14pt
- 下辺に罫線なし（背景色が境界として機能）
- パディング: 上下12px以上

パターンB「アンダーライン」:
- 背景: なし（透明）
- テキスト: 濃い色、Bold、12〜14pt
- 下辺に太めの罫線（2pt、Primary色）
- テキストは全大文字 or 小さめのキャプション体

パターンC「カテゴリ列強調」:
- 最左列（カテゴリ列）のみ背景色を薄く
- ヘッダー行は太字のみ、背景なし
- 左列とデータ列の間に視覚的な分離（余白 or 薄い縦罫線1本だけ許容）

コンテンツに合うパターンを1つ選択し、選択理由をコメントすること。

## 原則3: 数値のフォーマッティング

数値の書式は「0.1秒で読み取れる」ことが基準です。

```
【必須ルール】
- 金額: 右揃え、3桁カンマ区切り、通貨単位はヘッダーに記載（セルには書かない）
  ✓ ヘッダー: "売上高（百万円）"  セル: "1,450"
  ✗ セル: "¥1,450百万円"

- パーセンテージ: 右揃え、小数点1桁で統一
  ✓ "15.2%"  "+3.4%"  "-1.2%"
  ✗ "15%"  "15.17%"  "15.2"（%なし）

- 増減率: 符号を必ず付ける（+も明記）
  ✓ "+15.9%"  "-3.2%"  "±0.0%"
  ✗ "15.9%"（正の符号なし）

- ポイント差: "pt" で表記
  ✓ "+1.2pt"  "-0.5pt"
  ✗ "+1.2%"（率と混同する）

- 倍率: "x" で表記、小数点1桁
  ✓ "2.3x"  "0.8x"
  ✗ "2.3倍"  "230%"

- 整数: 右揃え、3桁カンマ区切り
  ✓ "1,234"  "56,789"
  ✗ "1234"

- テキスト: 左揃え
- ヘッダー: テキスト列は左揃え、数値列は右揃え（データに合わせる）
- N/Aや空欄: "—"（emダッシュ）で統一、"N/A" "-" "n/a" は禁止
```

## 原則4: 行の視覚的ヒエラルキー

表の行には「カテゴリ行」「データ行」「小計行」「合計行」の4種類があり、
それぞれ視覚的に区別されなければなりません。

```
【カテゴリ行（セクション見出し）】
- 背景: 薄いグレー（#F0F2F5）
- テキスト: Bold、Primary色、やや大きめ（+1pt）
- 値セルは空 or emダッシュ
- 上に余白（上パディング追加 or 空行）

【データ行（通常行）】
- 背景: 白
- テキスト: Regular、#333333
- ゼブラストライピングを入れる場合は #FAFBFC（ほぼ白に近いグレー）

【小計行】
- 背景: #F7F8FA
- テキスト: SemiBold
- 上に細い罫線（0.5pt、#CCCCCC）
- インデントなし（データ行と左揃え一致）

【合計行（最下部）】
- 背景: #E8EBF0 or Primary色の10%不透明度
- テキスト: Bold、やや大きめ（+1pt）
- 上に太めの罫線（1.5pt、#333333）
- 下に二重線（2本の細い罫線、間隔2px）or 太い単線（2pt）
```

## 原則5: 列幅の黄金比

列幅は「均等割り」にしないこと。コンテンツに応じた比率を設定します。

```
【カテゴリ列（最左）】: 全体の25〜35%
- 一番長いテキストが折り返さない幅を確保
- 左パディング: 12〜16px

【数値列】: 均等 or コンテンツ比率
- 数値は桁数に応じた幅（"1,450" と "15.2%" は違う幅が必要）
- 右パディング: 12〜16px（数値の右端が列の右端から離れすぎない）

【テキスト列（説明等）】: 残りの幅
- 最小幅: 120px（折り返しが3行を超えない幅）
```

列幅の具体例:
```
5列の表（カテゴリ + 4つの数値）:
  全体幅: 100%
  カテゴリ列: 28%
  数値列 x 4: 各18%

4列の表（カテゴリ + テキスト + 2つの数値）:
  全体幅: 100%
  カテゴリ列: 22%
  テキスト列: 38%
  数値列 x 2: 各20%
```

## 原則6: 条件付きフォーマット（コンディショナル・フォーマッティング）

数値の意味を色で補強します。ただし「控えめに」が鉄則です。

```
【増減の色分け】
- ポジティブ: #0D7C3D（深いグリーン）— テキスト色のみ変更
- ネガティブ: #C62828（深いレッド）— テキスト色のみ変更
- ニュートラル: #333333（通常色）
- 背景色は変えない（テキスト色だけで十分）

【ヒートマップ（比較表の場合）】
- 最高値: Primary色の背景（15%不透明度）+ Primary色テキスト
- 中間値: 背景なし + 通常テキスト
- 最低値: 薄い赤の背景（#FEE2E2）+ #C62828テキスト
- グラデーションは3段階まで（5段階以上は読みにくい）

【評価・ランク表示】
- ★★★ / ◎ / ● の記号は使用禁止（素人感が出る）
- 代わりに: 色付きバー（インラインデータバー）or 数値スコア
- 「おすすめ」を示す場合: 列背景を薄い色で強調 + ヘッダーにバッジ
```

## 原則7: パディングとスペーシング

「窮屈な表」はコンサル品質ではありません。

```
【セル内パディング】
- 上下: 8〜12px
- 左右: 12〜16px
- ヘッダーセル: 上下12〜16px（データ行より広め）

【行の高さ】
- ヘッダー行: 44〜52px
- データ行: 36〜44px
- カテゴリ行: 40〜48px（データ行より少し高い）
- 合計行: 44〜52px（ヘッダーと同等）

【表の外側の余白】
- 表タイトルと表本体の間: 16〜24px
- 表の下の注釈との間: 12〜16px
```

## 原則8: 表タイトルと注釈

```
【表タイトル】
- 位置: 表の左上、表本体の上
- フォーマット: Bold、16〜18pt、#1A1A2E
- 内容: 「何が」「何を」示しているか1文で（例: "事業セグメント別 売上高推移（FY2023-2025E）"）

【ソース表記】
- 位置: 表の左下
- フォーマット: Regular、9〜10pt、#999999
- 内容: "出所: {{ソース名}}, {{日付}}" or "Source: {{source}}"

【注釈】
- 位置: ソース表記の上、表本体の下
- フォーマット: Regular、9〜10pt、#666666
- 番号付き: "1) ... 2) ..." or 上付き数字 "¹⁾ ... ²⁾ ..."
- "E" = Estimate の注釈は必ず入れる: "E: 会社予想"
```

# ===== 出力形式別の実装指示 =====

## A. スライド（.pptx）の場合

PptxGenJSで実装。以下の設定を適用:

```javascript
// コンサル品質テーブルの基本設定
const tableOpts = {
  x: 0.5,
  y: 1.2,  // タイトル用スペースを確保
  w: 9.0,
  colW: [2.5, 1.6, 1.6, 1.6, 1.7],  // コンテンツに合わせた列幅（合計 = w）
  border: { type: "none" },  // デフォルトは罫線なし
  margin: [8, 12, 8, 12],  // [top, right, bottom, left] in points
  autoPage: false,
  rowH: [0.45, 0.38, 0.38, 0.38, 0.45],  // ヘッダーと合計行を少し高く
};

// ヘッダー行
const headerRow = [
  { text: "項目", options: {
    fill: { color: "1E2761" }, color: "FFFFFF", bold: true,
    fontSize: 11, fontFace: "Calibri", align: "left", valign: "middle",
    margin: [10, 12, 10, 16]
  }},
  { text: "FY2023", options: {
    fill: { color: "1E2761" }, color: "FFFFFF", bold: true,
    fontSize: 11, fontFace: "Calibri", align: "right", valign: "middle"
  }},
  // ... 数値列は全てalign: "right"
];

// データ行
const dataRow = [
  { text: "売上高", options: {
    color: "333333", fontSize: 10, fontFace: "Calibri",
    align: "left", valign: "middle", margin: [8, 12, 8, 16],
    border: [
      { type: "none" },  // top
      { type: "none" },  // right
      { type: "solid", pt: 0.5, color: "E0E0E0" },  // bottom（薄い区切り線）
      { type: "none" }   // left
    ]
  }},
  { text: "1,450", options: {
    color: "333333", fontSize: 10, fontFace: "Calibri",
    align: "right", valign: "middle",
    border: [
      { type: "none" },
      { type: "none" },
      { type: "solid", pt: 0.5, color: "E0E0E0" },
      { type: "none" }
    ]
  }},
];

// 合計行
const totalRow = [
  { text: "合計", options: {
    fill: { color: "E8EBF0" }, color: "1A1A2E", bold: true,
    fontSize: 11, fontFace: "Calibri", align: "left", valign: "middle",
    margin: [10, 12, 10, 16],
    border: [
      { type: "solid", pt: 1.5, color: "333333" },  // top: 太い区切り線
      { type: "none" },
      { type: "solid", pt: 2, color: "333333" },  // bottom: 最下部の太線
      { type: "none" }
    ]
  }},
  // ...
];
```

表タイトルはaddTextで表の上に配置:
```javascript
slide.addText("事業セグメント別 売上高推移（FY2023-2025E）", {
  x: 0.5, y: 0.7, w: 9.0, h: 0.4,
  fontSize: 14, fontFace: "Calibri", bold: true, color: "1A1A2E",
  align: "left", valign: "bottom", margin: 0
});
```

ソース表記はaddTextで表の下に配置:
```javascript
slide.addText("出所: 各社IR資料よりチーム作成", {
  x: 0.5, y: 4.8, w: 9.0, h: 0.25,
  fontSize: 8, fontFace: "Calibri", color: "999999",
  align: "left", valign: "top", margin: 0
});
```

## B. HTML（Note記事・Webページ）の場合

```html
<style>
  .consul-table {
    width: 100%;
    border-collapse: collapse;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Noto Sans JP", sans-serif;
    font-size: 14px;
    color: #333333;
    line-height: 1.5;
  }

  /* 縦罫線なし、横罫線のみ */
  .consul-table th,
  .consul-table td {
    padding: 10px 16px;
    border: none;
    border-bottom: 1px solid #E5E7EB;
  }

  /* ヘッダー */
  .consul-table thead th {
    background: #1E2761;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 13px;
    padding: 14px 16px;
    border-bottom: none;
    letter-spacing: 0.02em;
  }

  /* テキスト列は左揃え、数値列は右揃え */
  .consul-table thead th.text-col { text-align: left; }
  .consul-table thead th.num-col  { text-align: right; }
  .consul-table td.text-col { text-align: left; }
  .consul-table td.num-col  { text-align: right; font-variant-numeric: tabular-nums; }

  /* ゼブラストライプ（ほぼ白） */
  .consul-table tbody tr:nth-child(even) { background: #FAFBFC; }

  /* カテゴリ行 */
  .consul-table tr.category-row {
    background: #F0F2F5;
  }
  .consul-table tr.category-row td {
    font-weight: 700;
    color: #1E2761;
    padding-top: 14px;
    border-bottom: 1px solid #D1D5DB;
  }

  /* 合計行 */
  .consul-table tr.total-row {
    background: #E8EBF0;
  }
  .consul-table tr.total-row td {
    font-weight: 700;
    color: #1A1A2E;
    border-top: 2px solid #333333;
    border-bottom: 3px double #333333;
    padding: 12px 16px;
  }

  /* 増減の色分け */
  .positive { color: #0D7C3D; }
  .negative { color: #C62828; }

  /* 表タイトル */
  .consul-table-title {
    font-size: 16px;
    font-weight: 700;
    color: #1A1A2E;
    margin-bottom: 12px;
  }

  /* ソース表記 */
  .consul-table-source {
    font-size: 11px;
    color: #999999;
    margin-top: 8px;
  }

  /* 注釈 */
  .consul-table-notes {
    font-size: 11px;
    color: #666666;
    margin-top: 4px;
  }
</style>
```

HTMLの場合、font-variant-numeric: tabular-nums を数値セルに必ず適用する。
これにより数字が等幅レンダリングされ、縦の桁揃えが完璧になる。

## C. Excel（.xlsx）の場合

openpyxlで実装。以下の書式設定を適用:

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers

# 罫線定義（縦罫線なし）
thin_bottom = Border(bottom=Side(style='thin', color='E5E7EB'))
thick_bottom = Border(bottom=Side(style='medium', color='333333'))
double_bottom = Border(bottom=Side(style='double', color='333333'))
header_border = Border(bottom=Side(style='medium', color='1E2761'))

# ヘッダースタイル
header_font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
header_fill = PatternFill('solid', fgColor='1E2761')
header_align_text = Alignment(horizontal='left', vertical='center', wrap_text=True)
header_align_num = Alignment(horizontal='right', vertical='center')

# データ行スタイル
data_font = Font(name='Calibri', size=10, color='333333')
data_align_text = Alignment(horizontal='left', vertical='center')
data_align_num = Alignment(horizontal='right', vertical='center')

# 合計行スタイル
total_font = Font(name='Calibri', size=10, bold=True, color='1A1A2E')
total_fill = PatternFill('solid', fgColor='E8EBF0')

# 数値フォーマット
fmt_comma = '#,##0'           # 整数
fmt_decimal = '#,##0.0'       # 小数1桁
fmt_pct = '0.0%'              # パーセント
fmt_pct_sign = '+0.0%;-0.0%'  # 符号付きパーセント

# 行の高さ
ws.row_dimensions[1].height = 36  # ヘッダー
# データ行: 各28
# 合計行: 32
```

列幅はmin_width = max(セル内最長文字数 × 1.2, 12) で自動計算し、
さらにカテゴリ列は +4、数値列は +2 の余白を加える。

## D. SVG（図解埋め込み用）の場合

```xml
<!-- テーブルの基本構造 -->
<g class="consul-table" transform="translate(40, 60)">
  <!-- 表タイトル -->
  <text x="0" y="-16" font-size="16" font-weight="bold" fill="#1A1A2E"
        font-family="sans-serif">表タイトル</text>

  <!-- ヘッダー背景 -->
  <rect x="0" y="0" width="{{tableWidth}}" height="44"
        fill="#1E2761" rx="0"/>

  <!-- ヘッダーテキスト -->
  <text x="16" y="28" fill="#FFFFFF" font-size="12" font-weight="bold"
        font-family="sans-serif">項目</text>
  <text x="{{col2Right}}" y="28" fill="#FFFFFF" font-size="12"
        font-weight="bold" font-family="sans-serif" text-anchor="end">FY2023</text>

  <!-- データ行（y = 44 + rowIndex * rowHeight） -->
  <!-- 行区切り線（水平のみ） -->
  <line x1="0" y1="{{y}}" x2="{{tableWidth}}" y2="{{y}}"
        stroke="#E5E7EB" stroke-width="1"/>

  <!-- データテキスト -->
  <text x="16" y="{{textY}}" fill="#333333" font-size="11"
        font-family="sans-serif">売上高</text>
  <text x="{{col2Right}}" y="{{textY}}" fill="#333333" font-size="11"
        font-family="sans-serif" text-anchor="end">1,450</text>

  <!-- 合計行 -->
  <line x1="0" y1="{{totalLineY}}" x2="{{tableWidth}}" y2="{{totalLineY}}"
        stroke="#333333" stroke-width="2"/>
  <rect x="0" y="{{totalBgY}}" width="{{tableWidth}}" height="44"
        fill="#E8EBF0"/>
</g>
```

SVGテーブルの数値は必ずtext-anchor="end"で右揃えにする。
各列の右端x座標を事前計算し、全数値列でその座標にanchorを合わせること。

# ===== やってはいけないこと（違反リスト） =====

以下は1つでもあるとコンサル品質から脱落します:

1. 全セル格子罫線（Excelデフォルトの見た目）
2. 縦罫線の使用（カテゴリ列の右に1本だけは例外的に許容）
3. 数値の左揃え
4. テキストの右揃え
5. 列幅の均等割り
6. セル内パディングなし（テキストが罫線にくっつく）
7. ★や◎や△での評価表示
8. 全行同じフォントウェイト（ヘッダー・データ・合計の区別なし）
9. "N/A" "n/a" "-" の混在（emダッシュ "—" に統一）
10. パーセンテージの小数桁数が行によってバラバラ
11. 正の増減率に "+" をつけない
12. 金額とパーセンテージを同じ列に混在させる
13. ソース表記（出所）の欠落
14. 表タイトルの欠落
15. ヘッダーと同じ背景色をデータ行にも使う
16. 虹色のセル背景色
17. 丸ゴシック系フォントの使用（ポップすぎる）

# ===== 表のタイプ別テンプレート =====

データの種類に応じて最適なテーブル構造を選択すること。

## 比較表（Comparison Matrix）
- 列: 比較軸（最左）+ 比較対象（2〜5列）
- 最左列は固定幅、比較対象列は均等幅
- 推奨列にハイライト: 列ヘッダーにバッジ（"推奨" or "Recommended"）+ 列全体の背景をPrimary色の5%不透明度
- 行グルーピング: カテゴリ行で機能群を分類

## 時系列表（Time Series / Financial Summary）
- 列: 項目（最左）+ 期間（FY2022, FY2023, FY2024E, ...）
- 予測値の列ヘッダーに "E" を付与し、列背景を微妙に変える（#FAFBFC → #F5F6F8）
- 増減率列は最右に配置、正負で色分け
- 小計行・合計行をヒエラルキーに応じて配置

## スコアカード（Scorecard / KPI Dashboard）
- 列: KPI名 / 目標値 / 実績値 / 達成率 / ステータス
- 達成率に条件付き色分け（>100%: グリーン、80-100%: 通常、<80%: レッド）
- ステータスは色付きドット（●）で表現（テキストではなくSVG丸 or Unicode ● + 色）
  - グリーン ●: #0D7C3D（達成）
  - イエロー ●: #F59E0B（進行中）
  - レッド ●: #C62828（要対応）

## プロコン表（Pros & Cons / Option Evaluation）
- 列: 評価項目（最左）+ 選択肢A, B, C
- 定性評価は「High / Med / Low」で統一（◎○△は使わない）
- "High" = #0D7C3D / "Med" = #333333 / "Low" = #C62828 でテキスト色のみ変更
- 最下部にスコア合計行を配置

## RACI / 責任分担表
- 列: タスク（最左）+ ロール名（複数列）
- セル値: R（Responsible） / A（Accountable） / C（Consulted） / I（Informed）
- 各文字に背景色: R=#1E2761白文字 / A=#065A82白文字 / C=#E8EBF0 / I=#F5F5F5
- 中央揃え

# ===== 実装手順 =====

## Step 1: テーブルタイプの判定
コンテンツから最適なテーブルタイプを選択。

## Step 2: データ整形
- 数値フォーマットの統一（カンマ、小数桁、符号）
- emダッシュへの置換
- 列幅比率の計算

## Step 3: 実装
選択した出力形式に応じたコードを記述。
原則1〜8の全ルールを適用。

## Step 4: 品質検証（必須、省略禁止）
生成物を画像化して以下を確認:

- [ ] 縦罫線がないこと（許容された例外を除く）
- [ ] 数値が全て右揃えであること
- [ ] テキストが全て左揃えであること
- [ ] 数値の小数桁数が列内で統一されていること
- [ ] 正の増減率に "+" が付いていること
- [ ] ヘッダー・データ行・合計行が視覚的に区別されていること
- [ ] 列幅がコンテンツに適切であること（折り返しなし or 最大2行）
- [ ] セル内パディングが十分であること（窮屈でない）
- [ ] ソース表記があること
- [ ] 表タイトルがあること
- [ ] 条件付きフォーマットが正しく適用されていること
- [ ] フォントがConsistentであること

問題があれば修正して再検証。

# ===== 出力 =====

最終ファイルは指定された出力形式で出力すること。
検証用の画像（PNG or JPG）も併せて出力すること。
```

---

## クイックリファレンス：数値フォーマット早見表

| 種類 | 形式 | 例 | 揃え |
|------|------|-----|------|
| 金額（整数） | #,##0 | 1,450 | 右 |
| 金額（小数） | #,##0.0 | 1,450.5 | 右 |
| パーセンテージ | 0.0% | 15.2% | 右 |
| 増減率 | +0.0% / -0.0% | +15.9% | 右 |
| ポイント差 | +0.0pt / -0.0pt | +1.2pt | 右 |
| 倍率 | 0.0x | 2.3x | 右 |
| 整数（人数等） | #,##0 | 1,234 | 右 |
| テキスト | — | テキスト | 左 |
| 空欄・N/A | — | — | 中央 |

## カラーパレット早見表

| 用途 | 色コード | 用例 |
|------|---------|------|
| ヘッダー背景 | #1E2761 | thead |
| ヘッダー文字 | #FFFFFF | th |
| データ文字 | #333333 | td |
| 合計行背景 | #E8EBF0 | tr.total |
| カテゴリ行背景 | #F0F2F5 | tr.category |
| ゼブラ偶数行 | #FAFBFC | tr:nth-child(even) |
| 罫線（薄） | #E5E7EB | border-bottom |
| 罫線（濃） | #333333 | 合計行上 |
| ポジティブ | #0D7C3D | +増 |
| ネガティブ | #C62828 | -減 |
| ソース表記 | #999999 | 出所 |
| 注釈 | #666666 | 注記 |
