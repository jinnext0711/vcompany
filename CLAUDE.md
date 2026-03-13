# vCompany - Virtual Company Organization

# 絶対禁止（全エージェント必読、違反は全成果物やり直し）

以下に1つでも違反した場合、成果物は全てやり直しになる。
コード生成・文書作成の前に必ず読み返すこと。

## スライド
- タイトル下にアクセントライン（装飾的な水平線）を入れるな → 発見次第やり直し
- 装飾的な円・楕円・幾何学模様を意味なく配置するな → 発見次第やり直し
- スライドの下半分（y > 3.5inch）を空白にするな → 最下要素の y+h >= 4.5inch を確認
- PptxGenJSの色コードに # を含めるな → ファイル破損する
- PptxGenJSのオプションオブジェクトを再利用するな → 破壊的変更される
- Unicode bullet を直接書くな → bullet: true を使え

## テーブル
- 記号（◎ ○ △ ×）をセルに使うな → テキスト評価+色分けで代替せよ
- 全セル格子罫線を使うな → border: { type: "none" } をデフォルトにせよ
- 数値を左揃えにするな → 数値は必ず align: "right"

## 情報品質
- 出所不明の数値を書くな → 全数値に「ソース名+発行年」を付けよ
- LLMの学習データから数値を生成するな → 捏造と同じ。ウェブ検索で裏付けを取れ

## 頻出違反の Wrong/Right（実際に発生した失敗）

### AP-03: タイトル下アクセントライン
❌ NG
```js
slide.addShape(pres.shapes.LINE, { x:0.8, y:2.8, w:2.5, h:0, line:{color:"F96167", width:3} });
```
✅ OK
```
アクセントラインは入れない。タイトル下は余白として活かす。
```

### AP-05: 記号による評価
❌ NG
```js
["機能", "◎ 完全自律", "△ 限定的", "× 未対応"]
```
✅ OK
```js
const cell = (text, color) => ({ text, options: { color, fontSize:10, align:"center" }});
["機能", cell("完全自律","0D7C3D"), cell("限定的","F59E0B"), cell("未対応","C62828")]
```

### AP-10: 格子罫線テーブル
❌ NG
```js
slide.addTable(rows, { border: { pt:1, color:"999999" } });
```
✅ OK
```js
slide.addTable(rows, { border: { type:"none" } });
// 各セルの options 内で border の bottom のみ指定
```

---

AIエージェントによる仮想会社組織プロジェクト。

## Quick Start

```bash
pip install -r requirements.txt   # python-pptx, markdown, weasyprint
npm install pptxgenjs             # PptxGenJS（STEP 2スライド生成）
python main.py --input output/phase3_content.json --formats pptx
python main.py --input content.json --all-formats --output-dir output
node generate-slides.js           # PptxGenJS でスライド生成（STEP 2）
```

## コードベース構造

```
src/
  pipeline.py          # 6フェーズパイプラインの統括
  research/collector.py  # Phase 1: リサーチ
  outline/generator.py   # Phase 2: アウトライン
  writer/composer.py     # Phase 3: 執筆・評価・改善
  design/builder.py      # Phase 4: デザイン設定
  qa/auto_checker.py     # Phase 5: QA（JSON検証）
  qa/visual_validator.py # Phase 6.5: 視覚品質検証（PPTX再読込）
  output/
    pptx_exporter.py     # Phase 6: PPTX生成
    html_exporter.py     # HTML生成
    layouts.py           # ゾーン分割レイアウト
    special_slides.py    # 特殊スライド（title/agenda/summary等）
    helpers.py           # 描画プリミティブ・座標定数
    diagrams/            # 12種の図解レンダラー
templates/
  prompt-master.md       # STEP 1: 思考設計プロンプト
  prompt-slide-v2.md     # STEP 2: スライド実装プロンプト（座標テンプレート付き）
  prompt-eyecatch.md     # STEP 2: アイキャッチ実装プロンプト
  prompt-diagram.md      # STEP 2: 図解実装プロンプト
  prompt-table-v2.md     # STEP 2: テーブル実装プロンプト（失敗コード例付き）
  anti-patterns.md       # アンチパターン集（実際の失敗カタログ）
  qa-agent-prompt.md     # Visual QAサブエージェント専用ロール設定
  role-planning-research.md  # 企画部リサーチエージェント（Phase 1-2）
  role-qa-content.md     # コンテンツQAエージェント（Content QA gate）
  role-auditor.md        # 監査役エージェント v2（汎用自己改善エンジン）
  protocol-self-improvement.md  # CEO自己改善オーケストレーション・プロトコル
  updated_workflow_with_agents.svg  # 7フェーズワークフロー図
  why_agents_dont_self_correct.svg  # 自己改善の必要性を示す構造図
  auditor_generalization_analysis.svg  # Auditor Core + Domain Module 分離設計図
  claude-code-visual-quality-guide.md  # ビジュアル品質ガイド
  claude-md-snippet.md   # CLAUDE.md用品質ルールスニペット
generate-slides.js       # STEP 2: PptxGenJS スライド生成スクリプト
audit-modules/
  slide.md               # スライド監査ドメインモジュール
  code.md                # コード開発監査ドメインモジュール
  research.md            # リサーチ監査ドメインモジュール
retrospectives/          # Auditor Retrospective レポート履歴
output/
  design/                # STEP 1 成果物（story-design.md 等）
  pptx/                  # STEP 2 成果物（.pptx）
```

## パイプライン（7フェーズ + 2 QAゲート）

```
Phase 1: リサーチ        → 企画部 + role-planning-research.md → research-report.md
Phase 2: アウトライン     → 企画部 + role-planning-research.md → outline.md
  ── Content QA gate ──  → 品質管理部 + role-qa-content.md → content-qa-report.md
  │  NG → Phase 1 に差し戻し
  │  OK ↓
Phase 3: 執筆            → 広報部 + prompt-master.md → story-design.md
Phase 4: デザインプラン    → デザイン部 + prompt-master.md → slide-master-plan.md
Phase 5: デザイン実装     → 開発部 + prompt-slide-v2 / table-v2 等 → output.pptx
  ── Visual QA gate ──   → 品質管理部 + qa-agent-prompt.md → qa-report.md
  │  NG → Phase 5 に差し戻し
  │  OK ↓
Phase 7: ユーザーに提示   → 画像 + qa-report + content-qa-report
```

ワークフロー図: `templates/updated_workflow_with_agents.svg`
中間成果物は `output/` 配下に保存。中断・再開可能。

## スライド・資料生成ルール

（禁止事項はファイル冒頭の「絶対禁止」セクションに集約済み）

### レイアウト基準
- 全スライドの最下要素の (y + h) が 4.5 inch 以上であること
- チャートの h は 3.5 inch 以上
- テーブルの rowH の合計は 3.5 inch 以上
- テキストボックスの h はコンテンツ量に比例させる（3行で h=2.5 は過大）

### テーブル品質
- 罫線: border: { type: "none" } をデフォルトにし、個別セルで bottom のみ指定
- 数値: 右揃え、3桁カンマ区切り、正の増減率に + を付ける
- ヘッダー: 背景色あり（1E2761）、白文字、Bold
- 合計行: 背景色あり（E8EBF0）、上辺に太い罫線
- 比較表の評価: 色分けテキスト（緑: 0D7C3D / 黒: 333333 / 橙: F59E0B / 赤: C62828）

### QAフロー（v2）
1. コード生成 → 実行
2. LibreOfficeでPDF変換 → pdftoppmで画像化 → markitdownでテキスト抽出
3. QAサブエージェント（`templates/qa-agent-prompt.md`）で検査 → qa-report.md を出力
   - 自分自身（コード生成者）がQAすることは禁止。確認バイアスにより問題を見逃す
4. qa-report.md の Critical / Major を全て修正 → 再実行 → 再検査
5. 全 Critical / Major がゼロになったらユーザーに画像 + qa-report.md を提示
6. 失敗パターンの参照: `templates/anti-patterns.md`

## 重要な制約（Gotchas）

- python-pptx の Chart API（add_chart）は使用禁止（Mac PowerPointで修復エラー発生）
- チャートは全てシェイプベース（_rect + _text_box）で描画する（python-pptx使用時）
- PptxGenJSの addChart は使用可能
- ゾーン名はレイアウトの返す名前と完全一致させる（two_col→left/right、three_col→col1/col2/col3）
- 同じレイアウトパターンを3スライド以上連続させない
- 詳細は `.claude/rules/` 配下の各ルールファイルを参照

## 資料作成システム（7フェーズ・パイプライン）

資料作成は7フェーズ + 2 QAゲートで行う。各フェーズの担当部門と使用プロンプトは上記パイプライン図を参照。

### Phase 1-2: リサーチ + アウトライン（企画部）

```
企画部が role-planning-research.md に基づいて実行
  → research-report.md   （ソース付きリサーチレポート、信頼度ラベル [A]-[D]）
  → outline.md           （スライド構成、データポイント配置、インサイトLevel判定）
```

情報の信頼性3原則: 出所不明の数値禁止、LLM生成と外部ソースの混同禁止、一次ソースへの遡及。

### Content QA gate（品質管理部）

```
品質管理部が role-qa-content.md に基づいて検査
  → content-qa-report.md （ソース検証、数値クロスチェック、捏造指数、インサイト深度）
```

合格条件: 捏造指数 ≤10%、データ密度 ≥3.5/slide、インサイト全 Level 3以上、Level 4以上が1つ以上。
不合格 → Phase 1 に差し戻し。

### Phase 3: 執筆（広報部）

```
広報部が prompt-master.md に基づいて実行
  → story-design.md        （ストーリー設計）
  → quality-check.md       （品質チェックリスト）
```

### Phase 4: デザインプラン（デザイン部）

```
デザイン部が prompt-master.md (Phase 5) に基づいて実行
  → slide-master-plan.md   （全スライドの設計仕様）
```

### Phase 5: デザイン実装（開発部）

slide-master-plan.md の各スライド設計を、用途に応じた実装プロンプトに入力して成果物を生成する。

| プロンプト | 技術スタック | 出力 | 出力先 |
|-----------|------------|------|--------|
| `prompt-slide-v2.md` | Node.js + PptxGenJS | .pptx | `output/pptx/` |
| `prompt-eyecatch.md` | Node.js + node-canvas | .png | `output/eyecatch/` |
| `prompt-diagram.md` | SVG / Mermaid / node-canvas | .svg / .png | `output/diagram/` |
| `prompt-table-v2.md` | PptxGenJS / HTML / openpyxl / SVG | .pptx / .html / .xlsx | `output/table/` |

### Visual QA gate（品質管理部）

```
品質管理部が qa-agent-prompt.md に基づいて検査
  → qa-report.md （空白、禁止パターン、テーブル品質、チャート品質等）
```

Critical / Major がゼロになるまで Phase 5 に差し戻し・修正ループ。

### Phase 7: ユーザーに提示

画像 + qa-report.md + content-qa-report.md をユーザーに提示。

### 自己改善ループ（Auditor v2: Core + Domain Module）

```
┌─────────────────────────────────────────────────┐
│ Auditor Core（汎用エンジン）                        │
│ 失敗収集 → ROOT分類(1-5) → ルール更新 → 永続化 → 効果追跡│
└──────┬──────────┬──────────┬─────────────────────┘
       │          │          │
  ┌────▼────┐ ┌───▼────┐ ┌──▼───────┐
  │ slide   │ │ code   │ │ research │  ← audit-modules/*.md
  └─────────┘ └────────┘ └──────────┘
```

プロジェクト完了後の自動実行フロー:
1. CEO → Auditor に全成果物 + QAレポート + フィードバックを渡す
2. Auditor → プロジェクト種別を自動判定 → ドメインモジュール読み込み
3. Auditor → MODE 1 Retrospective（失敗収集 → ROOT分類 → 対策 → ルール更新）
4. 更新先: CLAUDE.md → anti-patterns.md → audit-modules/*.md → QAプロンプト
5. 次プロジェクトでは更新されたルールで自動適用 → 同じ失敗は再発しない

最重要KPI: **同一失敗の再発率**（初期50%以下 → 中期20%以下 → 成熟期5%以下）

構造図: `templates/auditor_generalization_analysis.svg`
問題分析: `templates/why_agents_dont_self_correct.svg`
プロトコル: `templates/protocol-self-improvement.md`
Auditorロール: `templates/role-auditor.md`

品質管理部は「ルールに従って検査」、Auditor は「ルールそのものを進化させる」。

### Retrospective 実行義務

Phase 7（出力）完了後、CEOは以下を必ず実行する。スキップは禁止。

```bash
claude --print "$(cat .claude/agents/auditor.md)

成果物一覧: $(ls *.md *.pptx *.pdf 2>/dev/null | tr '\n' ' ')
QAレポート: $(cat *qa-report*.md 2>/dev/null)
現在のルール: $(cat .claude/rules/*.md 2>/dev/null)" > retrospectives/$(date +%Y%m%d)-retrospective.md
```

Retrospective未実行のプロジェクトは「未完了」として扱う。

### 旧Pythonパイプライン（併存）

```bash
python main.py --input output/phase3_content.json --formats pptx
```

Phase 1→2→3→5→6→6.5 の自動生成パイプライン。7フェーズ・パイプラインとは独立して使用可能。

## 組織構成

```
                      ┌──────────────┐
                      │   Owner      │
                      │ (ユーザー)    │
                      └──────┬───────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
   ┌──────┴───────┐   ┌─────┴──────┐   ┌───────┴──────┐
   │   Auditor    │   │    CEO     │   │  Secretary   │
   │  (監査役)     │   │  (統括)    │   │   (秘書)     │
   └──────────────┘   └─────┬──────┘   └──────────────┘
                            │
 ┌─────┬─────┬─────┬─────┬────┬───┼───┬─────┬─────┬─────┐
 │     │     │     │     │        │   │     │     │     │
企画  開発  品質  広報 デザ  法務  総務  経理  Data  人事
Plan  Dev   QA   PR  Design Legal GA  Fin   Ana   HR
      └┬─┘
  Front Back Infra
```

## ルール

### 自律動作の原則

- **判断して進む（確認を最小化する）**
  - 小さな技術的判断は自分で決めて実行する。いちいち確認しない
  - 「どうしますか？」と聞くのは、方向性そのものが不明な時と、取り消せない破壊的操作の直前だけ

- **長く動く（途中で止まらない）**
  - エラーが出た場合、同じアプローチを繰り返さず代替手段を自分で考えて試す
  - タスクが完了してから判断・問題をまとめて伝える

### 組織ルール
- Owner（ユーザー）が最終意思決定者
- CEO が各部門への指示を統括する
- Auditor は CEO から独立し、Owner に直接報告する
- Secretary は CEO をサポートし、MCP連携のハブとなる
- 各部門は CEO の指示に基づき業務を遂行する

### コミュニケーションルール
- 応答時は必ず冒頭に発言者を明示する
- 形式: **【役職/部門名】** に続けて発言内容を記載する
- 例:
  - **【CEO】** 承知しました。各部門に指示を出します。
  - **【Secretary】** スケジュールを確認しました。
  - **【開発部】** 実装方針をご報告します。
  - **【Auditor】** 監査結果をOwnerにご報告します。
- 複数部門が関わる場合は、それぞれの発言を分けて記載する

### プロジェクト管理ルール
- プロジェクトの管理は全て GitHub リポジトリ上で行う
- 進捗管理には GitHub Issues を使用する
  - タスクは Issue として起票し、担当部門の Label を付与する
  - 進捗状況は Issue のステータス（Open / Closed）で管理する
- マイルストーンの管理には GitHub Milestones を使用する
- 作業の成果物は全て GitHub 上で管理し、Pull Request を通じてレビュー・マージする
- プロジェクト全体の進捗は GitHub Projects で可視化する
- ドキュメント・議事録・決定事項も全てリポジトリ内に記録する

### 課題・リスク管理ルール
- ラベル: `type:task` / `type:issue` / `type:risk` + `severity:critical〜low`
- リスクは影響度×発生確率でCritical〜Lowを判定
- 暫定対応（応急）→ 本格対応（根本解決）の2段階で対処
- 詳細は `.github/ISSUE_TEMPLATE/` のテンプレートを参照

#### 監査スケジュール（Auditor）
- **定例監査（週1回）** — リスク一覧のレビュー、進捗の健全性チェック、Ownerへの定例報告
- **臨時監査（随時）** — `severity:critical` または `severity:high` 起票時に即座にレビュー
- **月次監査（月1回）** — コスト監査（経理部連携）、組織全体のガバナンス総括レポート

## 定期メンテナンス

### CLAUDE.md品質監査（Auditor定例監査に含む・週1回）
- 実行: `/claude-md-management:claude-md-improver`
- 基準: 全ファイルGrade B（70点）以上を維持
- コードベース変更時にCLAUDE.mdが追随しているか確認

## エージェント定義

各エージェントの定義は `.claude/agents/` 配下に配置。
