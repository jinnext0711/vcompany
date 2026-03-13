# ルール体系 診断レポート

検査日: 2026-03-13
検査対象: 8ファイル
検査者: Auditor（MODE 2: ルール体系監査）

---

## サマリー

| 診断観点 | 判定 | 深刻度 |
|---------|------|--------|
| a) 禁止事項の強さ | NG — 4ファイルで罰則なしの曖昧表現 | Major |
| b) ルールの配置 | NG — CLAUDE.md の禁止事項が83行目（遅すぎる） | Critical |
| c) Wrong/Right コード例 | NG — 自動読込ファイル全てにコード例なし | Critical |
| d) QA実行方法 | NG — qa.md にサブエージェント起動コマンドなし | Critical |
| e) Retrospective 実行痕跡 | NG — retrospectives/ は空（.gitkeep のみ） | Major |

総合判定: 不合格 — 5項目中5項目が NG。仕組みは「書いてある」が「動いていない」。

---

## a) 禁止事項の「強さ」

### 問題

禁止の表現に3段階の強度差がある。弱い表現はLLMに無視される。

| ファイル | 行 | 現状の表現 | 強度 |
|---------|-----|----------|------|
| CLAUDE.md | 84 | "入れない" | 弱 |
| CLAUDE.md | 85 | "配置しない" | 弱 |
| CLAUDE.md | 86 | "使わない" | 弱 |
| CLAUDE.md | 88 | "空白にしない" | 弱 |
| CLAUDE.md | 89 | "作らない" | 弱 |
| pptx-rules.md | 21 | "絶対に入れない" | 強 |
| pptx-rules.md | 22 | "配置しない" | 弱 |
| table-rules.md | 15 | "書くな" | 強 |
| table-rules.md | 16 | "使うな" | 強 |
| ~/.claude/CLAUDE.md | 14 | "使用しない" | 弱（罰則なし） |
| audit-modules/slide.md | 5 | "禁止" | 中（罰則なし） |

### 修正提案

**CLAUDE.md L83-91 — 禁止事項を「命令形 + 罰則」に統一:**

```diff
 ### 絶対禁止（違反は全体やり直し）
-- タイトル下にアクセントライン（装飾的な水平線）を入れない
-- 装飾的な円・楕円・幾何学模様を意味なく配置しない
-- ◎ ○ △ × の記号をテーブルのセルに使わない（テキスト評価+色分けで代替）
-- Unicode bullet "•" を直接テキストに書かない（PptxGenJSの bullet: true を使う）
-- スライドの下半分（y > 3.5 inch）を空白にしない
-- 全セル格子罫線のテーブルを作らない（横罫線のみ）
-- PptxGenJSの色コードに # を含めない（ファイル破損する）
-- PptxGenJSのオプションオブジェクトを複数の要素間で再利用しない（破壊的変更される）
+1. タイトル下にアクセントライン（装飾的な水平線）を入れるな → 発見次第やり直し
+2. 装飾的な円・楕円・幾何学模様を意味なく配置するな → 発見次第やり直し
+3. ◎ ○ △ × の記号をテーブルのセルに書くな → テキスト評価+色分けで代替せよ
+4. Unicode bullet "•" を直接テキストに書くな → PptxGenJSの bullet: true を使え
+5. スライドの下半分（y > 3.5 inch）を空白にするな → 最下要素の y+h ≥ 4.5 を確認せよ
+6. 全セル格子罫線のテーブルを作るな → 横罫線のみ（border: {type:"none"} + bottom個別指定）
+7. PptxGenJSの色コードに # を含めるな → ファイルが破損する。"FF0000" であって "#FF0000" ではない
+8. PptxGenJSのオプションオブジェクトを複数要素で共有するな → makeShadow() 等で毎回新規生成せよ
```

**pptx-rules.md L22 — "配置しない" を強化:**

```diff
-2. 装飾的な円・楕円・幾何学模様を意味なく配置しない
+2. 装飾的な円・楕円・幾何学模様を意味なく配置するな → 発見次第やり直し
```

**audit-modules/slide.md L3-8 — 罰則を追記:**

```diff
 ## 品質基準
-- 空白率: スライド下部30%以上が空白ならNG
-- テーブル: ◎○△×禁止、格子罫線禁止、数値は右揃え
+- 空白率: スライド下部30%以上が空白 → Critical判定、やり直し
+- テーブル: ◎○△×を1つでも使ったら → Critical判定、やり直し。格子罫線 → Critical。数値は右揃え必須
```

---

## b) ルールの配置

### 問題

CLAUDE.md（307行）で禁止事項が83行目から始まる。
その前に Quick Start（5-13行）、コードベース構造（16-59行）、パイプライン（61-79行）がある。
LLMのコンテキストでは「冒頭に書かれたルール」ほど遵守率が高い。
83行目は全体の27%地点であり、コンテキスト圧縮時に残りやすいとは言えない。

| ファイル | 禁止事項の開始行 | 全体行数 | 位置(%) | 判定 |
|---------|---------------|---------|---------|------|
| CLAUDE.md | 83行目 | 307 | 27% | NG（コード構造の後ろ） |
| pptx-rules.md | 17行目 | 92 | 18% | OK（frontmatter直後） |
| table-rules.md | 13行目 | 72 | 18% | OK（frontmatter直後） |
| ~/.claude/CLAUDE.md | 13行目 | 42 | 31% | OK（短いファイル） |
| audit-modules/slide.md | 3行目 | 24 | 13% | OK |

### 修正提案

**CLAUDE.md — 禁止事項をファイル冒頭（3行目）に移動:**

```diff
 # vCompany - Virtual Company Organization

 AIエージェントによる仮想会社組織プロジェクト。
+
+## 絶対禁止（違反は全スライドやり直し — コード生成前に必ず確認）
+1. タイトル下にアクセントライン（装飾的な水平線）を入れるな
+2. 装飾的な円・楕円・幾何学模様を意味なく配置するな
+3. ◎ ○ △ × の記号をテーブルのセルに書くな → テキスト評価+色分けで代替
+4. Unicode bullet "•" を直接テキストに書くな → bullet: true を使え
+5. スライドの下半分（y > 3.5 inch）を空白にするな → y+h ≥ 4.5 必須
+6. 全セル格子罫線のテーブルを作るな → 横罫線のみ
+7. PptxGenJSの色コードに # を含めるな → ファイル破損
+8. オプションオブジェクトを複数要素で共有するな → 毎回新規生成

 ## Quick Start
```

元の83行目付近の「### 絶対禁止」セクションは削除（二重管理を避ける）。

---

## c) Wrong/Right コード例の有無

### 問題

自動読込されるファイル（CLAUDE.md, pptx-rules.md, table-rules.md）に
Wrong/Right コード例が1つもない。

コード例が存在するのは templates/ 配下のプロンプトファイルだけであり、
それらは手動で読み込まない限りコンテキストに入らない。

| ファイル | Wrong/Right例 | 判定 |
|---------|-------------|------|
| CLAUDE.md | なし | NG |
| pptx-rules.md | なし（参照先のみ） | NG |
| table-rules.md | なし | NG |
| audit-modules/slide.md | なし | NG |
| templates/anti-patterns.md | あり | OK（だが自動読込されない） |
| templates/prompt-table-v2.md | あり | OK（だが自動読込されない） |

LLMは「やるな」という文章より「このコードがダメ」という具体例のほうが理解する。

### 修正提案

**CLAUDE.md — 禁止事項の直後に最頻出3パターンのWrong/Rightを追記:**

```markdown
### Wrong/Right 例（最頻出の違反パターン）

❌ AP-05: ◎○△×をテーブルに使う
```js
rows.push(["Claude Code", "◎", "○", "△"]);  // ← 絶対禁止
```

✅ 正解: テキスト評価 + 色分け
```js
rows.push(["Claude Code",
  {text:"完全自律", options:{color:"0D7C3D", bold:true}},
  {text:"標準", options:{color:"333333"}},
  {text:"限定的", options:{color:"F59E0B"}}
]);
```

❌ AP-03: タイトル下にアクセントライン
```js
slide.addShape(pres.shapes.LINE, {x:0.5, y:1.0, w:3, h:0,
  line:{color:"1E2761", width:2}});  // ← 絶対禁止
```

✅ 正解: アクセントラインを入れない（タイトル→即コンテンツ）

❌ AP-10: 全セル格子罫線
```js
slide.addTable(rows, {border: {type:"solid", pt:1, color:"999999"}}); // ← 絶対禁止
```

✅ 正解: border: none + 横罫線のみ
```js
const rows = data.map((r, i) => r.map(cell => ({
  text: cell,
  options: {border: [
    {type:"none"}, {type:"none"},
    i === 0 ? {type:"solid", pt:1.5, color:"1E2761"} : {type:"solid", pt:0.5, color:"E5E7EB"},
    {type:"none"}
  ]}
})));
```
```

**pptx-rules.md L27 — 参照だけでなく代表例を1つ追記:**

```diff
 失敗パターンの詳細は `templates/anti-patterns.md` を参照。
+
+### 最頻出の禁止コード例
+❌ slide.addShape(pres.shapes.LINE, {x:0.5, y:1.0, w:3, h:0, line:{color:"1E2761", width:2}});
+   → アクセントラインは入れるな。このコードを書いた時点でやり直し。
+❌ rows.push(["項目", "◎", "○", "△"]);
+   → ◎○△×はテーブルに書くな。テキスト評価+色分けで代替。
```

**audit-modules/slide.md — 頻出問題にWrong例を追記:**

```diff
 ## 頻出問題パターン
 | # | パターン | ROOT | 再発回数 |
 |---|---------|------|---------|
-| AP-01 | スライド下半分が空白 | ROOT-2 | 高頻度 |
-| AP-03 | タイトル下アクセントライン | ROOT-2 | 高頻度 |
-| AP-05 | ◎○△×の記号使用 | ROOT-2 | 高頻度 |
+| AP-01 | スライド下半分が空白 | ROOT-2 | 高頻度 |
+| AP-03 | タイトル下アクセントライン | ROOT-2 | 高頻度 |
+| AP-05 | ◎○△×の記号使用 | ROOT-2 | 高頻度 |
 | AP-07 | 2x2マトリクスのY軸ラベル欠落 | ROOT-1 | 中頻度 |
 | AP-09 | 棒グラフの凡例なし色分け | ROOT-4 | 中頻度 |
+
+### AP-05 の Wrong/Right
+❌ `rows.push(["Claude Code", "◎", "○", "△"]);`
+✅ `rows.push(["Claude Code", {text:"完全自律", options:{color:"0D7C3D"}}]);`
+
+### AP-03 の Wrong/Right
+❌ `slide.addShape(pres.shapes.LINE, {x:0.5, y:1.0, w:3, h:0, line:{color:"1E2761", width:2}});`
+✅ アクセントラインのコード自体を書かない。タイトル→即コンテンツ。
+
+### AP-10 の Wrong/Right
+❌ `slide.addTable(rows, {border: {type:"solid", pt:1, color:"999999"}});`
+✅ `border: [{type:"none"},{type:"none"},{type:"solid",pt:0.5,color:"E5E7EB"},{type:"none"}]`
```

---

## d) QAの実行方法

### 問題

qa.md（品質管理部のエージェント定義）は2つのQAゲートの検査項目を列挙しているが、
「どうやってサブエージェントを起動するか」の具体的なコマンドが一切ない。

| 記述 | qa.md の状態 | 問題 |
|------|------------|------|
| PDF変換コマンド | なし | QA担当者がコマンドを知らない |
| 画像化コマンド | なし | 同上 |
| markitdown抽出コマンド | なし | 同上 |
| サブエージェント起動コマンド | なし | 「ファイルを参照」としか書いていない |
| $(cat ...) によるインライン渡し | なし | ファイル名参照だけでは中身が読まれない |

qa-agent-prompt.md のセクションA/Dには具体的な起動コマンドがあるが、
qa.md からはファイル名で「参照」しているだけ。
LLMはファイル名を見ても自動的にそのファイルを読むわけではない。

### 修正提案

**qa.md — Visual QA gate セクションに実行手順を追記:**

```diff
 ### Visual QA gate（Phase 5 → Phase 7 の間）
 - ロール定義: `templates/qa-agent-prompt.md`
 - 入力: PPTX をPDF変換 → 画像化 + markitdownでテキスト抽出
 - 出力: qa-report.md
+
+#### 実行手順（必ずこの順序で実行）
+```bash
+# 1. PDF変換 → 画像化 → テキスト抽出
+libreoffice --headless --convert-to pdf output.pptx
+rm -f slide-*.jpg
+pdftoppm -jpeg -r 150 output.pdf slide
+python -m markitdown output.pptx > slide-content.txt
+
+# 2. QAサブエージェント起動（自分でQAするな — 必ずサブエージェントに委託）
+claude --print "$(cat templates/qa-agent-prompt.md)"
+```
+サブエージェントに渡すのはファイル名ではなく $(cat ...) でインライン展開した内容。
+ファイル名だけ渡しても、サブエージェントはそのファイルを読まない。
```

**qa.md — Content QA gate セクションにも同様に追記:**

```diff
 ### Content QA gate（Phase 2 → Phase 3 の間）
 - ロール定義: `templates/role-qa-content.md`
 - 入力: research-report.md + outline.md + slide-content.txt
 - 出力: content-qa-report.md
+
+#### 実行手順
+```bash
+# Content QAサブエージェント起動
+claude --print "$(cat templates/role-qa-content.md)"
+```
+入力ファイル（research-report.md, outline.md）は
+サブエージェントのプロンプト内で cat で読み込む指示が含まれている。
```

---

## e) Auditor Retrospective の実行痕跡

### 問題

```
retrospectives/
  .gitkeep    ← これしかない。レポートはゼロ。
```

Auditor の MODE 1 Retrospective は「プロジェクト完了後に自動実行」と定義されているが、
一度も実行された形跡がない。

直近のプロジェクト（Claude Code スライド生成）は Owner に提出済みだが、
Retrospective は起動されていない。

原因の推定:
- [ROOT-1] ルールの不在: CEOの自己改善プロトコルに「自動実行」と書いてあるが、
  実際にはCEOが自分で判断して起動する必要がある。自動トリガーの仕組みは存在しない。
- [ROOT-3] 配置ミス: プロトコルが templates/protocol-self-improvement.md にあるが、
  これは自動読込されないファイル。CEOが意識して読まない限り発動しない。

### 修正提案

**CLAUDE.md — 自己改善ループの直後に、実行を促す強制トリガーを追記:**

```diff
 品質管理部は「ルールに従って検査」、Auditor は「ルールそのものを進化させる」。
+
+### Retrospective 実行義務
+スライド資料をユーザーに提示した後、Auditor は必ず MODE 1 Retrospective を実行する。
+「忘れた」「時間がない」は理由にならない。以下を出力するまで完了とみなさない:
+- retrospectives/YYYYMMDD_[テーマ]_retrospective.md
+実行痕跡がない場合（retrospectives/ が空）は、直近のプロジェクトに対して即時実行する。
```

**auditor.md — MODE 1 に「直近未実行時の即時実行」ルールを追記:**

```diff
 ### MODE 1: Retrospective（振り返り）

 - トリガー: プロジェクト完了後、Critical >= 1、Ownerフィードバック、差し戻し発生
+- 起動チェック: retrospectives/ に直近プロジェクトのレポートがなければ即時実行
+  `ls retrospectives/*.md 2>/dev/null | tail -1` で最新レポートの日付を確認
+  最新レポートが存在しない or 最終プロジェクト完了日より古い → 即時実行
```

---

## 修正の優先順位

| 順位 | 修正内容 | 対象ファイル | 理由 |
|------|---------|------------|------|
| 1 | CLAUDE.md 冒頭に禁止事項を移動 | CLAUDE.md | 最も影響が大きい。全セッションで自動読込される |
| 2 | CLAUDE.md に Wrong/Right コード例を追記 | CLAUDE.md | 禁止事項の実効性を大幅に上げる |
| 3 | qa.md にサブエージェント起動コマンドを追記 | qa.md | QAが「動く」ために必須 |
| 4 | 禁止表現を命令形+罰則に統一 | CLAUDE.md, pptx-rules.md | 曖昧表現の排除 |
| 5 | audit-modules/slide.md に Wrong/Right 追記 | audit-modules/slide.md | ドメイン知識の具体化 |
| 6 | Retrospective 実行義務を追記 | CLAUDE.md, auditor.md | 自己改善ループの起動 |
| 7 | 直近PJに対してRetrospective即時実行 | retrospectives/ | 仕組みの初回起動 |

---

## 根本的な問題の指摘

この診断で判明した最大の問題は:

**「設計は素晴らしいが、実行されていない」**

- 7フェーズパイプラインは定義されているが、禁止事項がコンテキストの奥に埋もれている
- QAサブエージェントは設計されているが、起動コマンドが qa.md に書かれていない
- 自己改善ループは設計されているが、一度も実行されていない
- Wrong/Right コード例は anti-patterns.md にあるが、自動読込ファイルにはない

対策の本質は「テンプレートファイルにある情報を、自動読込ファイルに転写する」こと。
LLMは自動読込されないファイルの存在を知っていても、中身を読むとは限らない。
