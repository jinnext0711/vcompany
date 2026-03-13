"""Phase 1: リサーチモジュール — テーマに基づく深掘り調査

Claude Codeがリサーチを実施し、構造化されたリサーチデータを生成する。
このモジュールは:
  1. リサーチ実施のための構造化プロンプトを提供する
  2. 出力データのバリデーションを行う
  3. 結果をPhase 2へ渡せる形式に整形する
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# データポイント必須フィールド定義
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REQUIRED_DATA_POINT_FIELDS = (
    "metric", "value", "comparison_baseline", "source", "date", "so_what",
)

REQUIRED_CASE_STUDY_FIELDS = (
    "company", "context", "before_metrics", "after_metrics",
    "timeline", "key_success_factors", "lessons_learned",
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# リサーチプロンプトテンプレート
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESEARCH_PROMPT_TEMPLATE = """
# Phase 1: リサーチ指示書

## テーマ
{theme}

## 対象読者
{audience}

## 資料の目的
{objective}

## リサーチ要件

以下の8つの領域について、**徹底的に**調査してください。
各領域で「ファクト（定量データ）」と「インサイト（洞察）」の両方を収集すること。

**重要原則:**
- 全ての定量データには必ず**比較基準**を付与すること（例: 「CAGR 25%」だけでなく「CAGR 25%、SaaS市場平均15%を大幅に上回る」）
- 各データポイントには**"So What"（だから何が言えるのか）**を明記すること
- 各領域ごとに**最低3つ以上**のデータポイントを収集すること
- 各領域ごとに**反論・逆張りの視点（contrarian view）**を1つ以上含めること
- 各知見に対して**対象読者にとっての意味（audience_relevance）**を記述すること

### 1. SCQA特定（最重要）
資料の骨格となるSCQAを特定する:
- **Situation（状況）**: 読者が「そうだよね」と同意する現状認識
- **Complication（課題）**: 現状を脅かす変化・問題・テンション
- **Question（問い）**: ComplicationからAutomatic に生まれる「では、どうすべきか？」
- **Answer（答え）**: この資料が提示する結論・提言

### 2. 市場・環境分析
- 市場規模、成長率、トレンド（**必ず比較基準を含む**: 隣接市場、過去推移、地域比較等）
- 技術動向、規制環境
- 定量データ（数値 + 比較基準 + 出典 + 時点 + So What）を**最低3つ**
- **反論・逆張りの視点**: 市場成長に対する懐疑論や過大評価の可能性
- **対象読者への示唆**: なぜこの数値が {audience} にとって重要なのか

### 3. プレイヤー分析
- 主要企業・製品・サービスの特徴
- 競合比較軸（機能、価格、シェア等）— **定量的な比較データを最低3つ**
- ポジショニングマップの根拠データ
- **反論・逆張りの視点**: 現在の勝者が将来も勝者であるとは限らない理由
- **対象読者への示唆**: 自社のポジショニングへの影響

### 4. ユースケース・事例（深掘り）
- 導入事例を**最低2つ**、以下の構造で詳述:
  - **企業名・背景**: どのような企業が、なぜ導入したか
  - **導入前の状態（Before）**: 定量的な指標で記述
  - **導入後の成果（After）**: 定量的な指標で記述
  - **タイムライン**: 導入から成果までの期間
  - **成功要因**: 何が成否を分けたか
  - **教訓**: 他社が学ぶべきポイント
- 成功パターンと失敗パターンの**対比**
- **反論・逆張りの視点**: 成功事例のバイアス（生存者バイアス等）

### 5. 課題・リスク
- 導入・実現における障壁（**定量データ付き**: 失敗率、平均導入期間等）
- 技術的・組織的・法的リスク — **各最低1つのデータポイント**
- 対策・ミティゲーション
- **反論・逆張りの視点**: リスクが過小評価されている可能性

### 6. 将来展望
- 3-5年の予測（**複数ソースの予測値を比較**）
- 次のトレンド
- 機会と脅威
- **反論・逆張りの視点**: 楽観的予測への反論

### 7. データポイント収集
上記全体から、以下の情報を構造化して抽出:
- 数値データ: **metric, value, comparison_baseline, source, date, so_what** の組み合わせ（各領域最低3つ）
- 事例データ: **company, context, before_metrics, after_metrics, timeline, key_success_factors, lessons_learned** の組み合わせ
- 主要エンティティ: name, role, relevance の組み合わせ
- 出典一覧: title, url_or_ref, date, reliability の組み合わせ（**最低5つ**）

### 8. 領域横断シンセシス（Cross-Area Synthesis）
上記1〜7の領域を横断して、以下をまとめる:
- **領域間の因果関係**: 例）市場成長 → プレイヤー増加 → 価格競争 → 品質リスク
- **共通するパターン**: 複数の領域で繰り返し出現するテーマやトレンド
- **矛盾・テンション**: 領域間で矛盾する知見とその解釈
- **統合的な示唆**: 全領域を踏まえた {audience} への3つの重要メッセージ

## 出力形式

以下のJSON形式で出力してください:

```json
{{
  "theme": "{theme}",
  "target_audience": "{audience}",
  "objective": "{objective}",
  "scqa": {{
    "situation": "...",
    "complication": "...",
    "question": "...",
    "answer": "..."
  }},
  "research_areas": [
    {{
      "area_name": "領域名",
      "findings": ["ファクト1", "ファクト2", ...],
      "data_points": [
        {{
          "metric": "指標名",
          "value": "値",
          "comparison_baseline": "比較基準（例: 業界平均○○、前年比○○）",
          "source": "出典",
          "date": "時点",
          "so_what": "この数値が意味すること・示唆"
        }}
      ],
      "insights": ["洞察1", "洞察2", "洞察3", ...],
      "comparative_analysis": {{
        "comparison_axes": ["比較軸1", "比較軸2"],
        "summary": "比較分析のまとめ"
      }},
      "contrarian_view": "この領域における反論・逆張りの視点",
      "audience_relevance": "対象読者にとってこの領域がなぜ重要か"
    }}
  ],
  "case_studies": [
    {{
      "company": "企業名",
      "context": "導入背景・課題",
      "before_metrics": {{"指標名": "導入前の値"}},
      "after_metrics": {{"指標名": "導入後の値"}},
      "timeline": "導入から成果までの期間",
      "key_success_factors": ["成功要因1", "成功要因2"],
      "lessons_learned": ["教訓1", "教訓2"]
    }}
  ],
  "cross_area_synthesis": {{
    "causal_links": ["因果関係1: A → B → C", ...],
    "common_patterns": ["共通パターン1", ...],
    "contradictions": ["矛盾点1とその解釈", ...],
    "integrated_messages": ["統合メッセージ1", "統合メッセージ2", "統合メッセージ3"]
  }},
  "key_entities": [
    {{"name": "名前", "role": "役割", "relevance": "関連性"}}
  ],
  "sources": [
    {{"title": "タイトル", "url_or_ref": "参照", "date": "日付", "reliability": "high/medium/low"}}
  ],
  "raw_facts": ["事実1", "事実2", ...]
}}
```
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# プロンプト生成
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_research_prompt(theme, audience="経営層",
                        objective="テーマの全体像を理解し、意思決定に必要な情報を提供する"):
    """Phase 1 リサーチ用のプロンプトを生成する。"""
    return RESEARCH_PROMPT_TEMPLATE.format(
        theme=theme,
        audience=audience,
        objective=objective,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# データ生成・バリデーション
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def create_research_data(theme, target_audience, objective, scqa,
                         research_areas, key_entities=None,
                         sources=None, raw_facts=None,
                         case_studies=None, cross_area_synthesis=None):
    """リサーチ結果をデータ構造にまとめる。"""
    return {
        "theme": theme,
        "target_audience": target_audience,
        "objective": objective,
        "scqa": scqa,
        "research_areas": research_areas,
        "case_studies": case_studies or [],
        "cross_area_synthesis": cross_area_synthesis or {
            "causal_links": [],
            "common_patterns": [],
            "contradictions": [],
            "integrated_messages": [],
        },
        "key_entities": key_entities or [],
        "sources": sources or [],
        "raw_facts": raw_facts or [],
    }


def validate_research(data):
    """リサーチデータのバリデーション。

    Returns:
        tuple[bool, list[str]]: (合格フラグ, 不合格項目リスト)
    """
    issues = []

    # SCQA チェック
    scqa = data.get("scqa", {})
    for key in ("situation", "complication", "question", "answer"):
        if not scqa.get(key):
            issues.append(f"SCQA の {key} が空です")

    # リサーチ領域チェック — 最低5領域
    areas = data.get("research_areas", [])
    if len(areas) < 5:
        issues.append(f"リサーチ領域が {len(areas)} 個（最低5個必要）")

    for i, area in enumerate(areas):
        area_label = area.get("area_name", i)

        if not area.get("area_name"):
            issues.append(f"リサーチ領域[{i}] の area_name が空です")

        # findings チェック
        findings = area.get("findings", [])
        if len(findings) < 2:
            issues.append(
                f"リサーチ領域 '{area_label}' の findings が {len(findings)} 個（最低2個）"
            )

        # data_points チェック — 最低3個
        data_points = area.get("data_points", [])
        if len(data_points) < 3:
            issues.append(
                f"リサーチ領域 '{area_label}' の data_points が"
                f" {len(data_points)} 個（最低3個必要）"
            )

        # data_points 必須フィールドチェック
        for j, dp in enumerate(data_points):
            for field in REQUIRED_DATA_POINT_FIELDS:
                if not dp.get(field):
                    issues.append(
                        f"リサーチ領域 '{area_label}' の data_points[{j}] に"
                        f" {field} がありません"
                    )

        # insights チェック — 最低3個
        insights = area.get("insights", [])
        if len(insights) < 3:
            issues.append(
                f"リサーチ領域 '{area_label}' の insights が"
                f" {len(insights)} 個（最低3個必要）"
            )

    # ソースチェック — 最低5個
    sources = data.get("sources", [])
    if len(sources) < 5:
        issues.append(
            f"出典（sources）が {len(sources)} 個（最低5個必要）"
        )

    # テーマ・読者チェック
    if not data.get("theme"):
        issues.append("theme が空です")
    if not data.get("target_audience"):
        issues.append("target_audience が空です")

    return (len(issues) == 0, issues)
