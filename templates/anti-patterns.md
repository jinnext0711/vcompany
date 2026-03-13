# Claude Code アンチパターン集：実際に発生した失敗とその修正

> このファイルはClaude Codeが実際に生成した失敗パターンのカタログです。
> 各プロンプトの冒頭にある「禁止リスト」の根拠がここにあります。
> Claude Codeのシステムプロンプトや CLAUDE.md に組み込むことを推奨します。

---

## カテゴリ1: レイアウト崩壊

### AP-01: スライド下半分が空白
```
発生頻度: ★★★★★（ほぼ全スライドで発生）
原因: PptxGenJSで要素のy座標を小さく設定しすぎる / hを小さく設定しすぎる
```

```javascript
// ❌ 失敗: コンテンツがy=0.5〜2.5の範囲に集中、y=2.5〜5.6が空白
slide.addText("タイトル", { x:0.5, y:0.3, w:9, h:0.5 });
slide.addChart(pres.charts.BAR, data, { x:0.5, y:1.0, w:5.5, h:2.0 }); // h=2.0は小さすぎる
// → スライドの下半分（y=3.0〜5.6）が完全な空白

// ✅ 修正: チャートのhを3.5以上にし、ソース表記をy=5.15に配置
slide.addText("タイトル", { x:0.5, y:0.3, w:9, h:0.5 });
slide.addChart(pres.charts.BAR, data, { x:0.5, y:1.0, w:5.5, h:3.8 }); // h=3.8
slide.addText("Source: ...", { x:0.5, y:5.15, w:9, h:0.3, fontSize:8, color:"999999" });
```

検証方法: 全スライドで「最下要素の y+h > 4.5 inch」を確認

---

### AP-02: カード/ボックスの中が空白
```
発生頻度: ★★★★☆
原因: テキスト3行に対してh=3.0inchのカードを作る等
```

```javascript
// ❌ 失敗: 3行のテキストに対してh=2.5の巨大なカード
slide.addShape(pres.shapes.RECTANGLE, { x:1, y:1, w:3, h:2.5, fill:{color:"F8F9FA"} });
slide.addText("1行補完\n8K tokens\n+15-30%", { x:1.1, y:1.1, w:2.8, h:2.3 });
// → カードの下70%が空白

// ✅ 修正: カード高さをコンテンツに合わせる
slide.addShape(pres.shapes.RECTANGLE, { x:1, y:1, w:3, h:1.2, fill:{color:"F8F9FA"} });
slide.addText("1行補完\n8K tokens\n+15-30%", { x:1.1, y:1.05, w:2.8, h:1.1 });
```

---

## カテゴリ2: 禁止パターンの出現

### AP-03: タイトル下のアクセントライン
```
発生頻度: ★★★★★（明示的に禁止しても出現する）
原因: LLMの学習データにこのパターンが大量に含まれている
```

```javascript
// ❌ 失敗: AI生成スライドの典型パターン
slide.addText("タイトル", { x:0.8, y:1.2, w:8, h:1.5 });
slide.addShape(pres.shapes.LINE, {
  x:0.8, y:2.8, w:2.5, h:0,
  line: { color:"F96167", width:3 }  // ← オレンジのアクセントライン
});

// ✅ 修正: ラインを入れない。空白は余白として活かす
slide.addText("タイトル", { x:0.8, y:1.2, w:8, h:1.5 });
// アクセントラインは入れない
```

対策: プロンプトの最初の5行以内に「タイトル下にアクセントラインを入れるな」と明記

---

### AP-04: 装飾的な幾何学模様
```
発生頻度: ★★★★☆
原因: 「ビジュアル要素を入れろ」の指示を装飾で満たそうとする
```

```javascript
// ❌ 失敗: 意味のない装飾円
slide.addShape(pres.shapes.OVAL, {
  x:7.5, y:1.5, w:3.0, h:3.0,
  fill: { color:"2A3B6E", transparency:70 }
});
slide.addShape(pres.shapes.OVAL, {
  x:8.0, y:2.0, w:2.5, h:2.5,
  fill: { color:"3A4B7E", transparency:60 }
});

// ✅ 修正: 装飾ではなく「データを表現するビジュアル」を入れる
// Big Number カード、チャート、アイコン付き箇条書き等
```

---

### AP-05: ◎○△×の記号による評価
```
発生頻度: ★★★★★（テーブルのある全スライドで発生）
原因: 日本語圏のPowerPointで極めて一般的なパターン
```

```javascript
// ❌ 失敗
["ファイル操作", "◎ 完全自律", "△ 限定的", "○ マルチファイル", "◎ 完全自律"]

// ✅ 修正: テキスト評価 + 色分け
const C = { best:"0D7C3D", good:"333333", limited:"F59E0B", none:"C62828" };
const c = (t, lv) => ({ text:t, options:{ color:C[lv], fontSize:10, align:"center" }});
["ファイル操作",
  c("完全自律","best"), c("限定的","limited"),
  c("マルチファイル","good"), c("完全自律","best")]
```

---

### AP-06: Unicode bulletの直接使用
```
発生頻度: ★★★☆☆
```

```javascript
// ❌ 失敗: 二重bulletになる
slide.addText("• チャンピオン10名選定", { ... });

// ✅ 修正: bullet: true を使う
slide.addText([
  { text: "チャンピオン10名選定", options: { bullet: true, breakLine: true } },
  { text: "CLAUDE.md初版作成", options: { bullet: true } }
], { x:0.5, y:1.5, w:3, h:2 });
```

---

## カテゴリ3: チャート・図解の構造崩壊

### AP-07: 2x2マトリクスのY軸ラベル欠落
```
発生頻度: ★★★★☆
原因: 回転テキストの実装を忘れる / rotateの指定を間違える
```

```javascript
// ❌ 失敗: X軸ラベルだけ入れてY軸を忘れる
slide.addText("← 自律性 →", { x:1.2, y:5.0, w:6, h:0.3 });
// Y軸ラベルなし

// ✅ 修正: Y軸ラベルを回転テキストで入れる
slide.addText("← 自律性 →", { x:1.2, y:5.05, w:6, h:0.3,
  fontSize:10, color:"666666", align:"center" });
slide.addText("制御性 ↑", { x:0.2, y:1.2, w:0.8, h:3.8,
  fontSize:10, color:"666666", align:"center", valign:"middle",
  rotate:270 });
```

---

### AP-08: テキストが図形の裏に隠れる
```
発生頻度: ★★★☆☆
原因: addの順序（後に追加したものが上に来る）を意識していない
```

```javascript
// ❌ 失敗: 円を後に追加してテキストが隠れる
slide.addText("Amazon Q", { x:4, y:3, w:2, h:0.4 });
slide.addShape(pres.shapes.OVAL, { x:4.2, y:2.5, w:0.8, h:0.8, fill:{color:"1E2761"} });
// → 円がテキストの上に重なる

// ✅ 修正: 図形を先、テキストを後に追加
slide.addShape(pres.shapes.OVAL, { x:4.2, y:2.5, w:0.8, h:0.8, fill:{color:"1E2761"} });
slide.addText("Amazon Q", { x:4.2, y:3.4, w:1.5, h:0.35,
  fontSize:10, color:"333333", align:"center" });
// テキストは円の下に配置
```

---

### AP-09: 棒グラフの色分けに凡例がない
```
発生頻度: ★★★★☆
原因: 特定バーだけAccent色にするが、なぜかを説明しない
```

```javascript
// ❌ 失敗: 一部だけオレンジだが理由不明
chartColors: ["1E2761", "1E2761", "1E2761", "F96167", "F96167"]
// 凡例なし → なぜ2027と2030だけオレンジ？

// ✅ 修正A: 全バー同色（最もシンプル）
chartColors: ["1E2761"]

// ✅ 修正B: 色分けする場合は凡例テキストを追加
chartColors: ["1E2761", "1E2761", "1E2761", "F96167", "F96167"]
// + 凡例テキストを手動追加
slide.addText("■ 実績  ■ 予測", {
  x:6.5, y:0.8, w:3, h:0.3,
  fontSize:9, color:"666666"
});
```

---

## カテゴリ4: テーブル品質

### AP-10: 格子罫線テーブル
```
発生頻度: ★★★★★
原因: PptxGenJSのborder指定がデフォルトで全辺に適用される
```

対策: border: { type: "none" } をテーブル全体に指定し、
個別セルのborderでbottomのみ指定する

---

### AP-11: テーブルの空白地帯
```
発生頻度: ★★★★☆
原因: rowHを小さく設定し、テーブル全体がスライド上部に偏る
```

対策: rowH の合計が 3.5 inch 以上になるよう設定。
行数が少ない場合は rowH を大きくしてパディングを増やす。

---

## プロンプトに組み込む際のベストプラクティス

1. 禁止事項はプロンプトの冒頭5行以内に配置する
2. 禁止事項はコード内のコメントとしても埋め込む
3. 「やること」より「やるな」を先に書く
4. 具体的な座標値（y, h）を含む正解コードを提示する
5. 自己QAに頼らず、画像化→ユーザー確認のループを組み込む
