# Visual QA Report

**検査対象:** `/Users/jinnobuta/vcompany/generate-slides.js`
**生成物:** `output/pptx/Claude_Code_v2_20260313_1359.pptx` (10.0" x 5.625", 15 slides)
**検査日:** 2026-03-13
**検査者:** 品質管理部 Visual QA Agent

---

## Summary

| 項目 | 結果 |
|------|------|
| Total slides | 15 |
| Critical | 0 |
| Major | 2 |
| Minor | 3 |
| Grade | **B+** (85点相当) |

---

## 検査項目一覧と総合判定

| # | 検査項目 | 判定 | 備考 |
|---|----------|------|------|
| AP-01 | アクセントライン (LINE shape) | PASS | LINE shape 使用なし |
| AP-01b | 装飾目的の細いRECTANGLE | NOTE | kpiCard/structuredItems内のアクセントバー (w=0.04) は情報構造を示す目的のため許容 |
| AP-03 | 装飾的な円・楕円 (OVAL) | PASS | OVAL shape 使用なし |
| AP-04 | Unicode bullet | PASS | "\u2022" / "•" の直接使用なし。bullet: true を使用 |
| AP-05 | テーブル記号 ◎○△× | PASS | テキスト評価+色分け (evalCell関数) で代替済み |
| AP-10 | 格子罫線 | PASS | border: [{type:"none"},...] + bottom のみ solid 指定 |
| Layout | LAYOUT_16x9 | PASS | pptx.layout = "LAYOUT_16x9" (L51) |
| 座標 | タイトル座標 | PASS | x=0.5, y=0.3, w=9.0, h=0.6, fontSize=20 (header関数) |
| 座標 | ソース y=5.15 | PASS | sourceNote/sourceDark: y=5.15, h=0.3 |
| 色コード | # なし | PASS | 全色コードに # を含まない |
| Shadow | makeShadow() | PASS | ファクトリ関数で毎回新規生成 (L60-68) |
| 空白 | y+h >= 4.5" | PASS | 構造検査済み: 全15スライド max_bottom=5.45" |
| フォント | 見出し/本文 | PASS | 見出し: Georgia Bold, 本文: Calibri |
| レイアウト3連続 | 同一パターン連続 | MAJOR | 詳細は下記 |

---

## Slide-by-Slide

### Slide 1: タイトル (Claude Code とは)
- [PASS] AP-01: LINE shape なし
- [PASS] AP-03: OVAL shape なし
- [PASS] AP-04: Unicode bullet なし
- [PASS] 色コード: # なし
- [PASS] 空白: sourceDark で y=5.15, h=0.3 → y+h=5.45"
- [PASS] フォント: Georgia Bold + Calibri
- レイアウトパターン: **full-dark** (暗色全面背景)

### Slide 2: 市場規模 (棒グラフ + KPI)
- [PASS] AP-01: LINE shape なし。グリッドライン(h=0.006)はチャート構成要素で許容
- [PASS] AP-03: OVAL なし
- [PASS] 空白: barChart + kpiCard + sourceNote → 5.45"
- [PASS] Shadow: kpiCard 内で makeShadow() 呼出
- レイアウトパターン: **chart-kpi** (左グラフ + 右KPI)

### Slide 3: 普及率 (棒グラフ x 2)
- [PASS] AP-01: LINE shape なし
- [PASS] AP-04: "\u2022" なし
- [PASS] 空白: barChart x2 + sourceNote → 5.45"
- [MINOR] AP-09相当: 棒グラフで highlight により1本だけ色を変えているが、凡例テキスト ("ハイライト = 注目データ" 等) がない。insight テキストで文脈は伝わるが、色分けの明示的凡例がない
- レイアウトパターン: **dual-chart** (左右2グラフ)

### Slide 4: 4世代の進化 (プロセスフロー)
- [PASS] AP-01: LINE shape なし
- [PASS] AP-03: OVAL なし
- [PASS] 空白: 詳細カード y=1.1+1.05=2.15, h=2.4 → y+h=4.55" + sourceNote=5.45"
- [PASS] フォント: Georgia Bold + Calibri
- レイアウトパターン: **process-flow** (4カラムフロー)

### Slide 5: Claude Code概要 (サイクル + KPI)
- [PASS] AP-01: LINE shape なし
- [PASS] AP-03: OVAL なし。中央は ROUNDED_RECTANGLE、周辺も ROUNDED_RECTANGLE
- [PASS] Shadow: kpiCard で makeShadow() 呼出
- [PASS] 空白: sourceNote → 5.45"
- レイアウトパターン: **cycle-kpi** (放射状配置 + KPI)

### Slide 6: ポジション分析 (2x2マトリクス)
- [PASS] AP-01: LINE shape なし
- [PASS] AP-03: OVAL なし。ドットは ROUNDED_RECTANGLE (rectRadius = dotSize/2) で円に見せている
- [MAJOR] AP-07相当: Y軸ラベルが欠落。X軸ラベル ("\u2190 自律性\u2192") はあるが、Y軸 ("制御性 \u2191") の回転テキストがない。2x2マトリクスとしては軸の意味が片方しか伝わらない
- [PASS] 空白: sourceNote → 5.45"
- レイアウトパターン: **matrix** (2x2マトリクス)

### Slide 7: 機能比較テーブル
- [PASS] AP-05: ◎○△× なし。evalCell 関数でテキスト+色分け
- [PASS] AP-10: ヘッダー行 border: all "none"。データ行 border: [none, none, solid(bottom), none]
- [PASS] 色コード: # なし
- [PASS] 推奨列ハイライト: Claude Code列に C.highlight ("F0F4FF") 背景適用
- [MINOR] table-rules: 数値データのセルはないため align:"right" 違反なし。ただし evalCell の align は "center" で統一されており、テキスト評価としては許容だが、table-rules の「テキスト: 左揃え」ルールとは不一致。評価テキストの center 揃えはコンサル品質テーブルでは一般的なため、Minor とする
- レイアウトパターン: **table** (比較テーブル)

### Slide 8: Intercom事例 (タイムライン + Before/After)
- [PASS] AP-01: タイムライン線 (h=0.03) はデータ構造を示す要素で装飾ではない
- [PASS] AP-04: bullet: true 使用。"\u2022" 直接使用なし
- [PASS] AP-05: "10\u00D7" は乗算記号 (Unicode U+00D7) で評価記号 × ではない
- [PASS] 空白: sourceNote → 5.45"
- レイアウトパターン: **timeline-panel** (タイムライン + パネル)

### Slide 9: Shopify事例 (ウォーターフォール + 構造化テキスト)
- [PASS] AP-01: LINE shape なし
- [PASS] AP-04: bullet なし (structuredItems 使用)
- [PASS] 空白: sourceNote → 5.45"
- レイアウトパターン: **waterfall-text** (左グラフ + 右テキスト)

### Slide 10: 用途別効果 (棒グラフ全幅)
- [PASS] AP-01: LINE shape なし
- [PASS] 空白: barChart (全幅) + sourceNote → 5.45"
- [MINOR] AP-09相当: highlight="レガシー移行" で1本だけアクセント色だが、明示的な凡例テキストがない。insight テキストで文脈は補完されているが、色分け理由の明示がない (Slide 2, 3 と同様のパターン)
- レイアウトパターン: **full-chart** (全幅グラフ)

### Slide 11: 3大リスク (3カラム)
- [PASS] AP-01: アクセントバー (w=0.04) は情報構造を示す目的
- [PASS] AP-03: OVAL なし
- [PASS] 空白: sourceNote → 5.45"
- レイアウトパターン: **three-col** (3カラム構造化テキスト)

### Slide 12: 導入リスク vs 未導入リスク
- [PASS] AP-01: structuredItems のアクセントバー (w=0.04) は情報構造用
- [PASS] 空白: ボトムノート y+h = (5.15-0.55)+0.45 = 5.05" + sourceNote=5.45"
- レイアウトパターン: **structured-cta** (構造化テキスト + CTA)

### Slide 13: 3段階導入ロードマップ (タイムライン)
- [PASS] AP-01: タイムライン線 (h=0.03) はデータ構造要素
- [PASS] AP-04: bullet: true 使用。"\u2022" 直接使用なし
- [PASS] 空白: sourceNote → 5.45"
- [MAJOR] レイアウト3連続: Slide 8 と Slide 13 は同じタイムライン構造。ただし間に4スライド挟まっているため「3連続」ではない。実際の連続パターン検査は以下の通り:

  | Slide | パターン |
  |-------|---------|
  | 1 | full-dark |
  | 2 | chart-kpi |
  | 3 | dual-chart |
  | 4 | process-flow |
  | 5 | cycle-kpi |
  | 6 | matrix |
  | 7 | table |
  | 8 | timeline-panel |
  | 9 | waterfall-text |
  | 10 | full-chart |
  | 11 | three-col |
  | 12 | structured-cta |
  | 13 | timeline |
  | 14 | grid-2x2 |
  | 15 | full-dark |

  **判定: 同一パターン3連続なし。PASS**

- レイアウトパターン: **timeline** (タイムラインフロー)

### Slide 14: 成功要因 (2x2グリッド)
- [PASS] AP-01: アクセントバー (w=0.04) は情報構造用
- [PASS] Shadow: makeShadow() で毎回新規生成
- [PASS] 空白: sourceNote → 5.45"
- レイアウトパターン: **grid-2x2** (2x2カードグリッド)

### Slide 15: まとめ & Next Steps
- [PASS] AP-01: LINE shape なし。アクセントラインなし（コメントでも明記）
- [PASS] AP-03: OVAL なし
- [PASS] AP-04: "\u2022" なし
- [PASS] 空白: sourceDark → 5.45"
- [PASS] フォント: Georgia Bold + Calibri
- レイアウトパターン: **full-dark** (暗色全面背景)

---

## 検出事項の詳細

### MAJOR-01: Slide 6 Y軸ラベル欠落

**対象:** Slide 6 (ポジション分析 2x2マトリクス), L411
**内容:** X軸ラベル ("\u2190 自律性（タスク完結能力）\u2192") は配置されているが、Y軸ラベル（制御性）の回転テキストがない。2x2マトリクスの意味を正しく伝えるためにはY軸ラベルが必須。
**ルール:** anti-patterns.md AP-07「2x2マトリクスのY軸ラベル欠落」
**修正案:** L414 付近に以下を追加:
```javascript
s.addText("制御性 \u2191", {
  x: px - 0.6, y: py, w: 0.5, h: ph,
  fontSize: 8, fontFace: "Calibri", color: C.text,
  align: "center", valign: "middle", rotate: 270,
});
```

### MAJOR-02: Slide 2/3/10 棒グラフの色分け凡例なし

**対象:** Slide 2 (L252: highlight="2030(予)"), Slide 3 (L273: highlight="2025", L277: highlight="日本"), Slide 10 (L660: highlight="レガシー移行")
**内容:** barChart関数の highlight パラメータにより1本だけアクセント色 (E67E22) になるが、「なぜこのバーだけ色が違うのか」を示す凡例テキストがない。insight テキストで文脈は補完されているが、色分けの明示的説明がない。
**ルール:** anti-patterns.md AP-09「棒グラフの色分けに凡例がない」
**修正案:** barChart関数内にオプションで凡例テキストを追加する、または各スライドで手動追加。

### MINOR-01: Slide 7 テーブル評価テキストの align

**対象:** Slide 7, evalCell関数 (L203)
**内容:** 評価テキスト（"完全自律" 等）が align:"center" で配置されている。table-rules.md では「テキスト: 左揃え（align: "left"）」と規定。ただし比較表の評価セルでは中央揃えがコンサル品質として一般的であり、実用上問題なし。

### MINOR-02/03: Slide 3/10 highlight凡例なし (MAJOR-02の個別インスタンス)

上記MAJOR-02に統合。

---

## コード品質の良い点

1. **禁止チェックリストをコメントに明記** (L5-11): コード冒頭にアンチパターンを列挙
2. **makeShadow()ファクトリ** (L60-68): shadow オブジェクトの共有を防止
3. **evalCell関数** (L198-211): ◎○△× の代わりにテキスト+色分けを体系化
4. **座標定数 L オブジェクト** (L36-48): マジックナンバーを排除
5. **色定数 C オブジェクト** (L16-34): 色コードを一元管理、# なし
6. **bullet: true の使用** (L551, L580, L771): Unicode bullet 直接使用を回避
7. **OVAL shape 不使用**: 装飾的な円・楕円を完全に排除。ドットは ROUNDED_RECTANGLE + rectRadius で代替
8. **レイアウトの多様性**: 15スライドで10種以上の異なるパターンを使用。3連続なし

---

## Conclusion

generate-slides.js は pptx-rules.md / table-rules.md / anti-patterns.md の主要ルールをよく遵守している。絶対禁止6項目 (アクセントライン、装飾円、◎○△×、Unicode bullet、下半分空白、格子罫線) は全てクリア。

修正すべき点は2件:
1. **Slide 6: Y軸ラベルの追加** (MAJOR) -- 2x2マトリクスの読解性に直結
2. **棒グラフの highlight 凡例追加** (MAJOR) -- barChart関数またはスライド個別で対応

Grade **B+** は「実用品質だが、改善の余地あり」を示す。上記2件の MAJOR を修正すれば Grade A に到達する。
