"""Phase 2: アウトライン生成モジュール — 資料の構成設計

リサーチ結果を受け取り、以下を設計する:
  - ピラミッド構造（結論→柱→根拠）
  - SCQA導入シーケンス
  - MECE分解（セクション設計）
  - 全スライドのレイアウト×図解の組み合わせ
  - アクションタイトル（So What）
  - ストーリーライン
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 利用可能なレイアウトと図解
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AVAILABLE_LAYOUTS = [
    "full", "two_col", "two_col_wide_left", "two_col_wide_right",
    "three_col", "top_bottom", "card_grid", "grid_2x2", "main_side",
]

AVAILABLE_DIAGRAMS = [
    "structured_text", "bullet_list", "table", "flow", "pyramid",
    "matrix", "bar_chart", "waterfall", "funnel", "cycle",
    "stacked_bar", "timeline", "kpi_card", "comparison_panel",
]

SPECIAL_SLIDE_TYPES = [
    "title", "agenda", "section_divider", "executive_summary", "summary",
]

# 図解ごとの必須データフィールド
DIAGRAM_DATA_SCHEMA = {
    "structured_text": {
        "required": ["structured_items"],
        "item_fields": {"keyword": "str", "detail": "str"},
        "optional": ["bottom_note", "sub_detail"],
    },
    "bullet_list": {
        "required": ["items"],
        "optional": ["heading"],
    },
    "table": {
        "required": ["headers", "rows"],
    },
    "flow": {
        "required": ["flow_steps"],
        "optional": ["flow_descriptions", "flow_details"],
    },
    "pyramid": {
        "required": ["pyramid_levels"],
        "item_fields": {"title": "str", "description": "str"},
    },
    "matrix": {
        "required": ["x_label", "y_label", "items"],
        "optional": ["quadrant_labels"],
        "item_fields": {"name": "str", "x": "float", "y": "float"},
    },
    "bar_chart": {
        "required": ["items"],
        "item_fields": {"label": "str", "value": "number"},
        "optional": ["insight", "highlight"],
    },
    "waterfall": {
        "required": ["waterfall_items"],
        "item_fields": {"label": "str", "value": "number", "type": "str"},
    },
    "funnel": {
        "required": ["funnel_items"],
        "item_fields": {"title": "str", "description": "str"},
        "optional": ["value"],
    },
    "cycle": {
        "required": ["cycle_items"],
        "item_fields": {"title": "str", "description": "str"},
        "optional": ["cycle_center"],
    },
    "stacked_bar": {
        "required": ["categories", "series"],
        "series_fields": {"name": "str", "values": "list"},
    },
    "timeline": {
        "required": ["timeline_items"],
        "item_fields": {"phase": "str"},
        "optional": ["duration", "tasks", "highlight"],
    },
    "kpi_card": {
        "required": ["value", "label"],
        "optional": ["trend"],
    },
    "comparison_panel": {
        "required": ["heading", "items"],
        "optional": ["accent"],
    },
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# アウトラインプロンプトテンプレート
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OUTLINE_PROMPT_TEMPLATE = """
# Phase 2: アウトライン設計指示書

## リサーチ結果サマリー

テーマ: {theme}
対象読者: {audience}
目的: {objective}

### SCQA
- Situation: {situation}
- Complication: {complication}
- Question: {question}
- Answer: {answer}

### リサーチ領域
{research_summary}

## 設計タスク

以下の手順でアウトラインを設計してください:

### Step 1: ピラミッド構造の設計
1. **結論（トップメッセージ）**: Answer を1文で表現する
2. **支柱（3-5本）**: 結論を支える主張。各支柱は「なぜそう言えるのか？」に答える
3. **根拠**: 各支柱を裏付けるファクト・データ

### Step 2: SCQA導入シーケンスの設計
資料冒頭に以下を配置:
1. タイトルスライド
2. アジェンダ
3. エグゼクティブサマリー（Answer を提示）
4. セクション区切り → 本編へ

### Step 3: MECE分解
支柱をセクションとして展開:
- 各セクションは section_divider で開始
- セクション内のスライドは2-5枚
- セクション間に重複がないこと（MECE）
- 全セクションで全体を網羅すること

### Step 4: 各スライドの設計
各コンテンツスライドについて:
1. **slide_title**: 短いトピック名（8文字以内推奨）
2. **title**: アクションタイトル（So What主張文、30-60文字）
   - 必ず述語で終わる完全な文にすること
   - 具体的な数値や比較を含めること
3. **slide_type**: "content"（通常）/ 特殊タイプ
4. **body_layout**: レイアウトID
5. **zones**: 各ゾーンに配置する図解とデータの概要
6. **content_intent**: このスライドで何を伝えたいか
7. **data_needs**: リサーチデータのどの部分を使うか
8. **source_hint**: 出典候補

### Step 5: ストーリーライン検証
全スライドの title を順に読んで、ストーリーが一本の論理として通じるか確認。
通じない場合は順序やタイトルを修正。

### Step 6: まとめ
summary スライドで:
- 3点にまとめた結論
- Next Steps（具体的なアクション）

## 利用可能なレイアウト
{layouts}

## 利用可能な図解
{diagrams}

## 図解のデータスキーマ
{diagram_schemas}

## 出力形式

```json
{{
  "title": "資料タイトル",
  "subtitle": "サブタイトル",
  "date": "YYYY-MM-DD",
  "pyramid": {{
    "conclusion": "トップメッセージ",
    "pillars": [
      {{"claim": "支柱の主張", "evidence": ["根拠1", "根拠2"]}}
    ]
  }},
  "section_groups": [
    {{"name": "セクション名", "section_number": 1, "slide_count": 3}}
  ],
  "sections": [
    {{
      "slide_type": "agenda",
      "slide_title": "アジェンダ",
      "title": "...",
      "agenda_items": [...]
    }},
    {{
      "slide_type": "content",
      "slide_title": "短いトピック名",
      "title": "So What主張文（述語で終わる完全文）",
      "body_layout": "full",
      "zones": {{
        "main": {{
          "diagram": "bar_chart",
          "data": {{...}}
        }}
      }},
      "content_intent": "このスライドの伝達目的",
      "data_needs": ["使用するリサーチデータ"],
      "source_hint": "出典候補"
    }}
  ],
  "storyline_summary": "全タイトルを連結した要約"
}}
```
"""


def get_outline_prompt(research_data):
    """Phase 2 アウトライン設計用のプロンプトを生成する。"""
    scqa = research_data.get("scqa", {})

    # リサーチ領域サマリー
    areas_text = []
    for area in research_data.get("research_areas", []):
        findings = "\n".join(f"  - {f}" for f in area.get("findings", [])[:3])
        insights = "\n".join(f"  - {i}" for i in area.get("insights", [])[:2])
        areas_text.append(
            f"#### {area.get('area_name', '不明')}\n"
            f"主要ファクト:\n{findings}\n"
            f"インサイト:\n{insights}"
        )

    # 図解スキーマ
    schema_lines = []
    for name, schema in DIAGRAM_DATA_SCHEMA.items():
        req = ", ".join(schema.get("required", []))
        opt = ", ".join(schema.get("optional", []))
        schema_lines.append(f"- **{name}**: 必須=[{req}] 任意=[{opt}]")

    return OUTLINE_PROMPT_TEMPLATE.format(
        theme=research_data.get("theme", ""),
        audience=research_data.get("target_audience", ""),
        objective=research_data.get("objective", ""),
        situation=scqa.get("situation", ""),
        complication=scqa.get("complication", ""),
        question=scqa.get("question", ""),
        answer=scqa.get("answer", ""),
        research_summary="\n\n".join(areas_text),
        layouts=", ".join(AVAILABLE_LAYOUTS),
        diagrams=", ".join(AVAILABLE_DIAGRAMS),
        diagram_schemas="\n".join(schema_lines),
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# データ生成・バリデーション
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def create_outline(title, subtitle="", date="", pyramid=None,
                   section_groups=None, sections=None,
                   storyline_summary=""):
    """アウトラインデータを構造化する。"""
    return {
        "title": title,
        "subtitle": subtitle,
        "date": date,
        "pyramid": pyramid or {},
        "section_groups": section_groups or [],
        "sections": sections or [],
        "storyline_summary": storyline_summary,
    }


# 述語パターン（アクションタイトルが文として成立しているか判定）
import re
PREDICATE_PATTERN = re.compile(
    r'(る|た|い|だ|ある|いる|できる|している|される|された|'
    r'なる|なった|ない|ている|ていく|ていた|'
    r'すべきだ|すべきである|必要がある|重要だ|重要である|'
    r'見込みだ|見込みである|見通しだ|見通しである|'
    r'可能だ|可能である|'
    r'高い|低い|大きい|小さい|多い|少ない|強い|弱い|'
    r'不可欠だ|不可欠である|'
    r'求められる|期待される|注目される|'
    r'ポイントだ|ポイントである|カギだ|カギである|鍵だ|鍵である|'
    # 五段動詞の終止形（う段: く・ぐ・す・つ・ぬ・ぶ・む・う）
    r'[くぐすつぬぶむう]|'
    # よく使われる動詞終止形
    r'異なる|生む|防ぐ|持つ|立つ|勝つ|伸びる|伸ばす|超える|'
    r'進む|進める|始まる|変わる|高まる|広がる|増す|減る|'
    r'示す|占める|支える|担う|果たす|もたらす|生じる|'
    r'得る|至る|及ぶ|迫る|上回る|下回る|並ぶ)$'
)


def validate_outline(data):
    """アウトラインデータのバリデーション。

    Returns:
        tuple[bool, list[str]]: (合格フラグ, 不合格項目リスト)
    """
    issues = []
    sections = data.get("sections", [])

    if not data.get("title"):
        issues.append("タイトルが空です")

    # ピラミッド構造チェック
    pyramid = data.get("pyramid", {})
    if not pyramid.get("conclusion"):
        issues.append("ピラミッドの結論（conclusion）が空です")
    pillars = pyramid.get("pillars", [])
    if len(pillars) < 2:
        issues.append(f"ピラミッドの支柱が {len(pillars)} 本（最低2本）")

    # セクション数チェック
    if len(sections) < 5:
        issues.append(f"スライド数が {len(sections)} 枚（最低5枚）")
    if len(sections) > 50:
        issues.append(f"スライド数が {len(sections)} 枚（最大50枚）")

    # 特殊スライドの存在チェック
    slide_types = [s.get("slide_type", s.get("layout", "")) for s in sections]
    if "agenda" not in slide_types:
        issues.append("agenda スライドがありません")
    if "executive_summary" not in slide_types:
        issues.append("executive_summary スライドがありません")

    # section_divider の数チェック
    divider_count = sum(1 for t in slide_types if t == "section_divider")
    if divider_count < 2:
        issues.append(f"section_divider が {divider_count} 枚（最低2枚、MECE分解が不十分）")

    # アクションタイトルチェック
    skip_types = {"title", "agenda", "section_divider", "summary"}
    for i, section in enumerate(sections):
        st = section.get("slide_type", section.get("layout", ""))
        if st in skip_types:
            continue
        title = section.get("title", "")
        if not title:
            issues.append(f"セクション[{i}] のアクションタイトルが空です")
        elif not PREDICATE_PATTERN.search(title):
            issues.append(
                f"セクション[{i}] のタイトルが述語で終わっていません: "
                f"'{title[:40]}...'"
            )

    # レイアウト・図解の有効性チェック
    valid_layouts = set(AVAILABLE_LAYOUTS)
    valid_diagrams = set(AVAILABLE_DIAGRAMS)
    for i, section in enumerate(sections):
        st = section.get("slide_type", "")
        if st == "content":
            bl = section.get("body_layout", "full")
            if bl not in valid_layouts:
                issues.append(f"セクション[{i}] の body_layout '{bl}' は無効です")
            zones = section.get("zones", {})
            for zone_name, spec in zones.items():
                diag = spec.get("diagram", "")
                if diag and diag not in valid_diagrams:
                    issues.append(
                        f"セクション[{i}] ゾーン '{zone_name}' の "
                        f"diagram '{diag}' は無効です"
                    )

    # セクションバランスチェック
    groups = data.get("section_groups", [])
    if groups:
        counts = [g.get("slide_count", 0) for g in groups]
        if counts:
            max_c, min_c = max(counts), min(counts)
            if min_c > 0 and max_c / min_c > 4:
                issues.append(
                    f"セクション間のスライド数バランスが偏っています "
                    f"(最大{max_c}枚 / 最小{min_c}枚)"
                )

    return (len(issues) == 0, issues)
