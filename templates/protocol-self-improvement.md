# CEO 自己改善オーケストレーション・プロトコル

> CEOエージェントがプロジェクト完了時に自動実行するプロトコルです。
> これにより、品質改善サイクルがOwnerの介入なしに回り続けます。

---

## プロトコル本文（CEOのCLAUDE.mdに追加）

```markdown
# 自己改善プロトコル（全プロジェクト完了後に自動実行）

## トリガー条件
以下のいずれかが発生した場合、このプロトコルを実行する:

1. プロジェクトの最終成果物が Owner に提出された後
2. Owner から品質に関するフィードバック（修正依頼、不満）があった時
3. QAレポートで Critical が 1件以上検出された時
4. Content QA で不合格（Phase 1 差し戻し）が発生した時

## 実行フロー

### Phase A: 成果物の確定
```
1. 開発部 → 最終 output.pptx を出力
2. 品質管理部 → qa-report.md + content-qa-report.md を出力
3. CEO → Owner に成果物 + QAレポートを提出
4. Owner → フィードバック（承認 or 修正要求）
```

### Phase B: 振り返りの起動（Owner承認後）
```
5. CEO → Auditor に以下を渡す:
   - 全中間生成物（research-report, outline, story-design, slide-master-plan）
   - 全QAレポート（content-qa-report, qa-report）
   - Ownerフィードバック（あれば）
   - 現在のCLAUDE.md

6. Auditor → プロジェクト種別を自動判定し、ドメインモジュールを読み込む
   - .pptx → audit-modules/slide.md
   - .py/.js → audit-modules/code.md
   - research-report.md → audit-modules/research.md
   - 該当モジュールがなければ新規生成

7. Auditor → MODE 1: Retrospective を実行
   - 失敗の収集 → ROOT分類（ROOT-1〜5）→ 対策立案
   - retrospective-report.md を出力

8. Auditor → MODE 2: QA監査 を実行（3回に1回、またはCritical多発時）
   - QAエージェント自体の検査漏れを検出
```

### Phase C: ルール更新の適用
```
9. Auditor → 以下のファイルを更新:
   - CLAUDE.md（全プロジェクト共通ルール）
   - anti-patterns.md（失敗パターン集）
   - audit-modules/*.md（ドメイン固有の検査知識）
   - 該当するロール設定（qa-agent-prompt, role-planning-research 等）

9. CEO → 更新内容を全部門に周知:
   "以下のルールが追加されました。次回プロジェクトから適用します。"
   （実際にはCLAUDE.mdに書かれているため自動適用される）

10. CEO → Owner に retrospective-report.md を提出:
    "今回のプロジェクトから N 件の改善点を発見し、ルールに反映しました。"
```

### Phase D: 改善効果の追跡
```
11. 次のプロジェクトで、前回の retrospective で追加したルールの効果を確認:
    - 同じ失敗が再発したか？ → ルールの表現が弱い → Auditor が再強化
    - 再発しなかったか？ → ルールが有効 → 維持
    - 新しい失敗が発生したか？ → 次の retrospective で対応
```

## 自動判定ロジック

### Critical即時対応（プロジェクト中に発動）
```
if (qa-report に Critical >= 1) {
  CEO → 該当部門に修正指示
  CEO → Auditor に「Critical発生」を通知
  Auditor → 即座に原因分類し、CLAUDE.md に暫定ルールを追加
  // プロジェクト完了を待たずにルールを更新
}
```

### Content QA 差し戻し時
```
if (content-qa-report が「不合格」) {
  CEO → 企画部に Phase 1 差し戻し指示
  CEO → Auditor に「Content QA不合格」を通知
  Auditor → リサーチ基準の見直しが必要か判断
  // 2回連続不合格の場合、role-planning-research.md を改訂
}
```

### QA問題ゼロ時（怪しい）
```
if (qa-report の問題数 == 0 && スライド枚数 >= 5) {
  CEO → Auditor に QA監査を要求（MODE 2）
  // 5枚以上のスライドで問題ゼロはありえない
  // QAの検査が甘い可能性を調査
}
```

## ルール更新の品質基準

Auditor がルールを更新する際の基準:

```
1. 具体性: 「品質を上げろ」ではなく「◎○△×を使うな」レベルの具体性
2. 検証可能性: ルールに違反しているかどうかを機械的に判定できること
3. Wrong/Right: 失敗コードと正解コードの両方を含むこと
4. 配置: 重要度が高いルールはプロンプトの冒頭5行以内に配置
5. 重複回避: 既存ルールと矛盾・重複しないこと（棚卸しで整理）
```

## 改善の累積効果の可視化

5プロジェクトごとに、以下のメトリクスを集計:

```markdown
# 改善メトリクス（5プロジェクト単位）

| 指標 | Period 1 | Period 2 | 傾向 |
|------|----------|----------|------|
| Critical検出数 / PJ | X | Y | ↓改善 |
| 差し戻し回数 / PJ | X | Y | ↓改善 |
| ルール総数 | X | Y | ↑増加 |
| 同一失敗の再発率 | X% | Y% | ↓改善（最重要） |
| QA検査漏れ率 | X% | Y% | ↓改善 |

★ 最重要指標: 同一失敗の再発率
  これが下がっていれば自己改善が機能している
  横ばいなら Auditor のルール更新が効果を出していない
```
```
