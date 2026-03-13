# Claude Code用プロンプト：コンサル品質テーブル生成 v2

> 実物の生成結果から学んだ失敗パターンを反映した改訂版。
> `{{...}}` を実際の内容に置き換えてから実行します。

---

## プロンプト本文

```markdown
あなたはMcKinsey品質のテーブルを作る専門家です。

# ================================================================
# 最重要: この3つを絶対に守れ（コード書く前に暗記）
# ================================================================

## 禁止（1つでもあればやり直し）

1. ◎ ○ △ × の記号をセルに書くな → テキスト評価 + 色分けで代替
2. 全セル格子罫線を使うな → 横罫線のみ（ヘッダー下 + 合計行上）
3. 数値を左揃えにするな → 数値は必ず align: "right"

## 間違いやすいコード（実際に発生した失敗）

### 失敗1: ◎○△× を使った比較表
```javascript
// ❌ これは素人品質。絶対にやらない
["コード補完", "○ 標準的", "◎ 業界最高", "◎ 高精度", "○ 標準的"]

// ✅ テキスト + 色で評価を表現する
const cell = (text, color) => ({
  text, options: { color, fontSize: 10, align: "center",
    margin: [8,8,8,8],
    border: [{ type:"none" },{ type:"none" },{ type:"solid", pt:0.5, color:"E5E7EB" },{ type:"none" }]
  }
});
["コード補完",
  cell("標準的", "333333"),
  cell("業界最高", "0D7C3D"),
  cell("高精度", "0D7C3D"),
  cell("標準的", "333333")]
```

### 失敗2: 格子罫線テーブル
```javascript
// ❌ 格子罫線 = Excelのデフォルト = 素人
slide.addTable(rows, {
  border: { pt: 1, color: "999999" }  // 全辺に罫線 → 格子
});

// ✅ デフォルト罫線なし + 個別セルで水平線のみ
slide.addTable(rows, {
  border: { type: "none" }  // 全体: 罫線なし
  // 各セルの options 内で bottom border のみ指定
});
```

### 失敗3: 数値の左揃え
```javascript
// ❌ 数値が左揃え → 桁が揃わず読みにくい
{ text: "1,450", options: { align: "left" } }

// ✅ 数値は右揃え
{ text: "1,450", options: { align: "right" } }
```

# ================================================================
# コンテンツ
# ================================================================

表のタイトル: {{表のタイトル}}
表の目的: {{比較？推移？構成比？ランキング？}}
出力形式: {{pptx / html / xlsx / svg}}

データ:
{{
  ここに表のデータを記述
}}

# ================================================================
# テーブル設計ルール
# ================================================================

## 色パレット
```
ヘッダー背景: 1E2761 / ヘッダー文字: FFFFFF
データ文字: 333333 / 合計行背景: E8EBF0
カテゴリ行背景: F0F2F5 / ゼブラ偶数行: FAFBFC
罫線（薄）: E5E7EB / 罫線（濃）: 333333
ポジティブ: 0D7C3D / ネガティブ: C62828
ソース表記: 999999
```

## 行のヒエラルキー（視覚的に区別する）
- ヘッダー行: 背景 Primary, 白文字 Bold, 行高 0.5inch, padding上下12
- データ行: 白背景, 通常文字, 行高 0.42inch, padding上下8
- カテゴリ行: 背景 F0F2F5, Bold, Primary色文字
- 合計行: 背景 E8EBF0, Bold, 上辺に太い罫線（1.5pt, 333333）

## 数値フォーマット
- 金額: 右揃え、3桁カンマ区切り、単位はヘッダーに（セルには書かない）
- %: 右揃え、小数1桁統一、正には + を付ける
- ポイント差: +1.2pt（%と混同させない）
- 空欄: "—"（emダッシュ）に統一

## 列幅の比率
- カテゴリ列（最左）: 全体の25-35%
- 数値列: コンテンツに応じた幅、均等割り可
- テキスト列: 残り幅、最小120px相当
- ★ 均等割りはNG（カテゴリ列と数値列は違う幅が必要）

## 推奨列のハイライト（比較表の場合）
```javascript
// 推奨列は薄い背景色を全セルに適用
const highlightBg = "F0F4FF";
// ヘッダーの推奨列にバッジ
{ text: "Claude Code ★推奨", options: {
  fill: { color: "0D4B8C" },  // やや明るいPrimary
  color: "FFFFFF", bold: true
}}
```

## ソース表記
- 表の左下に必ず配置
- フォーマット: "出所: {{ソース名}}, {{日付}}"
- サイズ: 8-9pt, 色: 999999

# ================================================================
# テーブルタイプ別の実装
# ================================================================

## 比較表（競合比較など）
```javascript
// 推奨列ハイライト付き比較表の完全な実装例
const COLORS = { best:"0D7C3D", good:"333333", limited:"F59E0B", none:"C62828" };
const HL = "F0F4FF";  // 推奨列ハイライト

const makeHeader = (text, isHighlight) => ({
  text, options: {
    fill: { color: isHighlight ? "0D4B8C" : "1E2761" },
    color: "FFFFFF", bold: true, fontSize: 11, fontFace: "Calibri",
    align: "center", valign: "middle", margin: [10,8,10,8]
  }
});

const makeDataCell = (text, level, isHighlight) => ({
  text, options: {
    fill: isHighlight ? { color: HL } : undefined,
    color: COLORS[level] || "333333",
    fontSize: 10, fontFace: "Calibri",
    align: "center", valign: "middle",
    margin: [8,8,8,8],
    border: [
      { type:"none" }, { type:"none" },
      { type:"solid", pt:0.5, color:"E5E7EB" },
      { type:"none" }
    ]
  }
});

const makeLabelCell = (text) => ({
  text, options: {
    color: "333333", fontSize: 10, fontFace: "Calibri",
    align: "left", valign: "middle",
    margin: [8,12,8,16],
    border: [
      { type:"none" }, { type:"none" },
      { type:"solid", pt:0.5, color:"E5E7EB" },
      { type:"none" }
    ]
  }
});

const rows = [
  // ヘッダー
  [makeHeader("機能", false), makeHeader("Claude Code ★", true),
   makeHeader("Copilot", false), makeHeader("Cursor", false)],
  // データ行
  [makeLabelCell("ファイル自律操作"),
   makeDataCell("完全自律", "best", true),
   makeDataCell("限定的", "limited", false),
   makeDataCell("マルチファイル", "good", false)],
  // ... 残りの行
];

slide.addTable(rows, {
  x: 0.5, y: 1.1, w: 9.0,
  colW: [2.2, 2.3, 2.3, 2.2],  // 推奨列をやや広く
  border: { type: "none" },
  autoPage: false,
});
```

## 時系列表（財務サマリーなど）
- 予測値列のヘッダーに "E" を付与
- 増減率列は最右、正負で色分け
- 合計行は太罫線 + 背景

## スコアカード（KPIダッシュボードなど）
- 達成率に色分け: >100% 緑, 80-100% 黒, <80% 赤
- テキスト色のみ変更（背景色は変えない）

# ================================================================
# 品質検証
# ================================================================

生成後、以下を確認:
- [ ] ◎○△× が含まれていないこと
- [ ] 縦罫線がないこと
- [ ] 数値が全て右揃えであること
- [ ] ヘッダーと合計行が視覚的に区別されていること
- [ ] ソース表記があること
- [ ] 推奨列（あれば）がハイライトされていること

画像化してユーザーに提示し、フィードバックを得ること。
```
