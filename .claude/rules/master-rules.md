---
paths:
  - "templates/prompt-master.md"
  - "templates/role-planning-research.md"
  - "templates/role-qa-content.md"
  - "**/story-design*"
  - "**/slide-master-plan*"
  - "**/quality-check*"
  - "**/research-report*"
  - "**/outline*"
  - "**/content-qa-report*"
  - "output/design/**"
---

# 資料作成パイプラインのルール（7フェーズ + 2 QAゲート）

## パイプライン順序（絶対遵守）

資料作成は必ず以下の7フェーズ + 2 QAゲートで行う。順序の逆転・省略は禁止。

```
Phase 1: リサーチ         → 企画部 + role-planning-research.md
Phase 2: アウトライン      → 企画部 + role-planning-research.md
  ── Content QA gate ──   → 品質管理部 + role-qa-content.md
Phase 3: 執筆             → 広報部 + prompt-master.md
Phase 4: デザインプラン     → デザイン部 + prompt-master.md (Phase 5)
Phase 5: デザイン実装      → 開発部 + prompt-slide-v2 / table-v2 等
  ── Visual QA gate ──    → 品質管理部 + qa-agent-prompt.md
Phase 7: ユーザーに提示
```

## Phase 1-2 の出力物（企画部）

`templates/role-planning-research.md` に基づいて以下を出力する:

| 出力ファイル | 役割 |
|-------------|------|
| research-report.md | リサーチレポート（ソース付き定量データ、信頼度ラベル [A]-[D]） |
| outline.md | アウトライン（スライド構成、データポイント配置、インサイトLevel判定） |

## Content QA gate（Phase 2 → Phase 3 の間）

品質管理部が `templates/role-qa-content.md` に基づいて検査し、content-qa-report.md を出力する。

合格条件:
- 捏造指数 ≤10%（[NOT FOUND] + [SUSPECT] + [UNVERIFIED] の割合）
- データ密度 ≥3.5/slide
- インサイト全 Level 3以上、Level 4以上が1つ以上
- ソース検証通過率 ≥80%

不合格 → Phase 1 に差し戻し。Content QA を通過するまで Phase 3 に進むことは禁止。

## Phase 3-4 の出力物（広報部 + デザイン部）

`templates/prompt-master.md` に基づいて以下を出力する:

| 出力ファイル | 役割 |
|-------------|------|
| story-design.md | ストーリー設計（資料全体の論理構成・メッセージフロー） |
| slide-master-plan.md | スライドマスタープラン（各スライドの詳細設計仕様） |
| quality-check.md | 品質チェックリスト（設計段階での検証項目と結果） |

出力先は `output/design/` とする。

## Phase 5: デザイン実装（開発部）

slide-master-plan.md の設計仕様に基づいて成果物を生成する:

- prompt-slide-v2.md → .pptx を生成
- prompt-eyecatch.md → .png（アイキャッチ）を生成
- prompt-diagram.md → .svg / .png（図解）を生成
- prompt-table-v2.md → .pptx / .html / .xlsx（テーブル）を生成

## Visual QA gate（Phase 5 → Phase 7 の間）

品質管理部が `templates/qa-agent-prompt.md` に基づいて検査し、qa-report.md を出力する。
Critical / Major がゼロになるまで Phase 5 に差し戻し・修正ループ。

## Phase 7: ユーザーに提示

画像 + qa-report.md + content-qa-report.md をユーザーに提示する。

## 自己改善ループ（プロジェクト完了後 — Auditor v2: Core + Domain Module）

プロトコル定義: `templates/protocol-self-improvement.md`
Auditorロール定義: `templates/role-auditor.md`
構造図: `templates/auditor_generalization_analysis.svg`

Owner承認後、CEOが自己改善プロトコルを発動する:
1. CEO → Auditor に全中間生成物 + QAレポート + Ownerフィードバックを渡す
2. Auditor → プロジェクト種別を自動判定 → ドメインモジュール読み込み（audit-modules/*.md）
3. Auditor → MODE 1 Retrospective（失敗収集 → ROOT分類 → 対策 → ファイル更新）
4. Auditor → retrospective-report.md を `retrospectives/` に出力
5. 更新先: CLAUDE.md → anti-patterns.md → audit-modules/*.md → QAプロンプト
6. 次プロジェクトでは更新されたルール + ドメインモジュールで自動適用

自動判定ロジック:
- Critical >= 1 → プロジェクト中に暫定ルール追加
- Content QA 2回連続不合格 → role-planning-research.md を改訂
- QA問題ゼロ（非trivial成果物）→ Auditor QA監査（MODE 2）を発動
- 5PJ完了 → MODE 3 ルール棚卸し

最重要KPI: 同一失敗の再発率（初期50%以下 → 中期20%以下 → 成熟期5%以下）
