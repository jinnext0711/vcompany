"""Phase 3: 執筆モジュール — 各スライドのコンテンツ執筆

アウトラインとリサーチデータを受け取り、
各スライドの完全なコンテンツデータ（JSON）を生成する。

出力はそのまま pptx_exporter.export_pptx() に渡せる形式。
"""

import re

from src.outline.generator import DIAGRAM_DATA_SCHEMA, AVAILABLE_DIAGRAMS


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ライタープロンプトテンプレート
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WRITER_PROMPT_TEMPLATE = """
# Phase 3: コンテンツ執筆指示書

## 資料情報
タイトル: {title}
サブタイトル: {subtitle}
対象読者: {audience}

## ピラミッド構造
結論: {conclusion}

支柱:
{pillars_text}

## SCQA
- Situation: {situation}
- Complication: {complication}
- Question: {question}
- Answer: {answer}

## リサーチデータ（利用可能な素材）
{research_data_text}

## アウトライン（各スライドの設計）
{outline_sections_text}

## 執筆ルール

### テキスト品質
1. **3点ルール**: 箇条書きは最大3項目。4つ以上ある場合はグルーピング
2. **冗長表現の排除**:
   - 「〜することが可能である」→「〜できる」
   - 「〜という点に関しましては」→「〜については」
   - 一文60文字以内
3. **用語の統一**: 同一概念に対して資料内で用語を統一する
4. **述語の明示**: アクションタイトルは必ず述語で終わる完全文

### コンテンツ品質
5. **出典の明記**: 全コンテンツスライドに source フィールドを設定
6. **定量データの活用**: 可能な限り数値データを含める
7. **スタンドアローン性**: 口頭説明なしでスライド単体で理解できること
8. **スピーカーノート**: 全スライドに notes を設定

### 図解データの正確性
9. 各図解のデータスキーマに厳密に従うこと
10. bar_chart の items には value（数値）を必ず含める
11. matrix の items には x, y（0-1の範囲）を含める
12. stacked_bar の series.values は categories と同数の要素

## 図解データスキーマ一覧
{diagram_schemas}

## 出力形式

export_pptx() に直接渡せるJSON形式で出力してください:

```json
{{
  "title": "{title}",
  "subtitle": "{subtitle}",
  "date": "{date}",
  "sections": [
    // 各スライドの完全なデータ
    // slide_type が "content" の場合:
    {{
      "slide_type": "content",
      "slide_title": "短いトピック名",
      "title": "So What主張文（述語で終わる）",
      "body_layout": "レイアウトID",
      "zones": {{
        "main": {{
          "diagram": "図解ID",
          "data": {{
            // 図解固有のデータフィールド
          }}
        }}
      }},
      "source": "出典",
      "notes": "スピーカーノート"
    }},
    // 特殊スライドの場合: slide_type に応じた固有フィールド
  ]
}}
```
"""


def get_writer_prompt(outline_data, research_data):
    """Phase 3 コンテンツ執筆用のプロンプトを生成する。"""
    pyramid = outline_data.get("pyramid", {})
    scqa = research_data.get("scqa", {})

    # 支柱テキスト
    pillars = pyramid.get("pillars", [])
    pillars_text = "\n".join(
        f"  {i+1}. {p.get('claim', '')} — 根拠: {', '.join(p.get('evidence', []))}"
        for i, p in enumerate(pillars)
    )

    # リサーチデータサマリー
    research_lines = []
    for area in research_data.get("research_areas", []):
        research_lines.append(f"\n### {area.get('area_name', '')}")
        for f in area.get("findings", []):
            research_lines.append(f"  - {f}")
        for dp in area.get("data_points", []):
            research_lines.append(
                f"  📊 {dp.get('metric', '')}: {dp.get('value', '')} "
                f"({dp.get('source', '')}, {dp.get('date', '')})"
            )
        for ins in area.get("insights", []):
            research_lines.append(f"  💡 {ins}")
    research_data_text = "\n".join(research_lines)

    # アウトラインセクション
    outline_lines = []
    for i, sec in enumerate(outline_data.get("sections", [])):
        st = sec.get("slide_type", sec.get("layout", "unknown"))
        outline_lines.append(
            f"\n### スライド {i+1}: {st}\n"
            f"  slide_title: {sec.get('slide_title', '')}\n"
            f"  title: {sec.get('title', '')}\n"
            f"  body_layout: {sec.get('body_layout', 'N/A')}\n"
            f"  content_intent: {sec.get('content_intent', '')}\n"
            f"  data_needs: {sec.get('data_needs', [])}"
        )
    outline_sections_text = "\n".join(outline_lines)

    # 図解スキーマ
    schema_lines = []
    for name, schema in DIAGRAM_DATA_SCHEMA.items():
        req = ", ".join(schema.get("required", []))
        item_f = schema.get("item_fields", {})
        item_desc = ""
        if item_f:
            fields = [f"{k}: {v}" for k, v in item_f.items()]
            item_desc = f" | 各要素: {{{', '.join(fields)}}}"
        schema_lines.append(f"- **{name}**: [{req}]{item_desc}")

    return WRITER_PROMPT_TEMPLATE.format(
        title=outline_data.get("title", ""),
        subtitle=outline_data.get("subtitle", ""),
        date=outline_data.get("date", ""),
        audience=research_data.get("target_audience", ""),
        conclusion=pyramid.get("conclusion", ""),
        pillars_text=pillars_text,
        situation=scqa.get("situation", ""),
        complication=scqa.get("complication", ""),
        question=scqa.get("question", ""),
        answer=scqa.get("answer", ""),
        research_data_text=research_data_text,
        outline_sections_text=outline_sections_text,
        diagram_schemas="\n".join(schema_lines),
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# データ生成・バリデーション
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def create_content(title, subtitle="", date="", sections=None):
    """執筆済みコンテンツをデータ構造にまとめる。"""
    return {
        "title": title,
        "subtitle": subtitle,
        "date": date,
        "sections": sections or [],
    }


def validate_content(content):
    """コンテンツデータのバリデーション。

    Returns:
        tuple[bool, list[str]]: (合格フラグ, 不合格項目リスト)
    """
    issues = []
    sections = content.get("sections", [])

    if not content.get("title"):
        issues.append("タイトルが空です")

    skip_types = {"title", "section_divider"}

    for i, sec in enumerate(sections):
        st = sec.get("slide_type", sec.get("layout", ""))

        # アクションタイトルチェック
        if st not in skip_types and st != "summary":
            title = sec.get("title", "")
            if not title:
                issues.append(f"セクション[{i}] ({st}) の title が空です")

        # source チェック（特殊スライド以外）
        if st not in {"title", "section_divider", "summary", "agenda"}:
            if not sec.get("source"):
                issues.append(f"セクション[{i}] ({st}) に source がありません")

        # notes チェック
        if not sec.get("notes"):
            issues.append(f"セクション[{i}] ({st}) に notes がありません")

        # content スライドの zones チェック
        if st == "content":
            zones = sec.get("zones", {})
            if not zones:
                issues.append(f"セクション[{i}] (content) に zones がありません")

            for zone_name, spec in zones.items():
                diagram_id = spec.get("diagram", "")
                if diagram_id and diagram_id in DIAGRAM_DATA_SCHEMA:
                    data = spec.get("data", {})
                    schema = DIAGRAM_DATA_SCHEMA[diagram_id]
                    for req_field in schema.get("required", []):
                        if not data.get(req_field):
                            issues.append(
                                f"セクション[{i}] ゾーン '{zone_name}' の "
                                f"図解 '{diagram_id}' に必須フィールド "
                                f"'{req_field}' がありません"
                            )

    # 3点ルールチェック
    for i, sec in enumerate(sections):
        for key in ("bullet_points", "key_points"):
            items = sec.get(key, [])
            if len(items) > 3:
                issues.append(
                    f"セクション[{i}] の {key} が {len(items)} 個（3点ルール違反）"
                )
        # zones 内のチェック
        for zone_name, spec in sec.get("zones", {}).items():
            data = spec.get("data", {})
            diag = spec.get("diagram", "")
            # matrix/bar_chart/waterfall は多項目が許容される
            skip_diags = {"matrix", "bar_chart", "waterfall", "stacked_bar", "table"}
            if diag not in skip_diags:
                for key in ("items", "structured_items"):
                    items = data.get(key, [])
                    if len(items) > 5:
                        issues.append(
                            f"セクション[{i}] ゾーン '{zone_name}' の "
                            f"{key} が {len(items)} 個（多すぎる可能性）"
                        )

    return (len(issues) == 0, issues)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# スライド品質評価・改善ループ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _score_information_density(section):
    """情報密度スコアを算出する（1-4点）。

    500文字超は情報過多としてペナルティ（3点に戻す）。
    """
    text_len = len(section.get("title", ""))
    for zone_name, spec in section.get("zones", {}).items():
        data = spec.get("data", {})
        # データ内の全テキスト値を走査
        text_len += _count_text_chars(data)
    if text_len >= 500:
        return 3  # 情報過多ペナルティ
    elif text_len >= 300:
        return 4  # 最適なコンサルティング密度
    elif text_len >= 250:
        return 3
    elif text_len >= 150:
        return 2
    return 1


def _count_text_chars(obj):
    """再帰的にオブジェクト内の全テキスト文字数を合計する。"""
    if isinstance(obj, str):
        return len(obj)
    elif isinstance(obj, list):
        return sum(_count_text_chars(item) for item in obj)
    elif isinstance(obj, dict):
        return sum(_count_text_chars(v) for v in obj.values())
    return 0


def _score_specificity(section):
    """具体性スコアを算出する（0-2点）。

    数値データ（数字、%、¥、$）と比較表現の有無で判定。
    """
    full_text = _extract_all_text(section)
    score = 0
    # 数値データの存在チェック
    if re.search(r'[\d]+[%％]|¥[\d]|[$][\d]|\d{2,}', full_text):
        score += 1
    # 比較表現の存在チェック
    if re.search(r'比較|より|対|vs|倍|増加|減少|上回|下回', full_text):
        score += 1
    return score


def _score_data_richness(section):
    """データ豊富さスコアを算出する（1-4点）。

    zones内のdata要素数を計数し、ダイアグラム種別ごとの閾値で評価。
    各ゾーンのダイアグラムタイプに応じたスコアの最大値を返す。
    """
    # ダイアグラム種別ごとの閾値テーブル (2pt下限, 3pt下限, 4pt下限)
    _THRESHOLDS = {
        "structured_text":   (2, 3, 4),
        "bullet_list":       (2, 3, 3),
        "bar_chart":         (3, 5, 7),
        "table":             (3, 5, 7),
        "flow":              (3, 4, 5),
        "timeline":          (2, 4, 5),
        "kpi_card":          (2, 3, 3),
        "matrix":            (3, 5, 7),
        "comparison_panel":  (2, 4, 5),
    }
    _DEFAULT_THRESHOLDS = (2, 4, 6)

    _DATA_KEYS = (
        "structured_items", "items", "rows", "flow_steps",
        "series", "categories", "columns", "cells", "nodes",
        "timeline_items", "cycle_items", "funnel_items",
        "waterfall_items", "pyramid_levels", "kpi_items",
    )

    best_score = 1  # 最低1点

    for zone_name, spec in section.get("zones", {}).items():
        data = spec.get("data", {})
        diagram = spec.get("diagram", "")

        # このゾーンのアイテム数を集計
        zone_items = 0
        for key in _DATA_KEYS:
            val = data.get(key, [])
            if isinstance(val, list):
                zone_items += len(val)

        # kpi_card: value/label ペアでリスト形式でない場合も1件とカウント
        if data.get("value") is not None and not data.get("kpi_items"):
            zone_items += 1

        # ダイアグラム種別に応じた閾値を取得
        t2, t3, t4 = _THRESHOLDS.get(diagram, _DEFAULT_THRESHOLDS)

        if zone_items >= t4:
            zone_score = 4
        elif zone_items >= t3:
            zone_score = 3
        elif zone_items >= t2:
            zone_score = 2
        else:
            zone_score = 1

        if zone_score > best_score:
            best_score = zone_score

    return best_score


def _score_source_quality(section):
    """出典品質スコアを算出する（0-2点）。"""
    source = section.get("source", "")
    if not source:
        return 0
    if len(source) > 20:
        return 2
    return 1


def _score_notes_quality(section):
    """ノート品質スコアを算出する（0-2点）。"""
    notes = section.get("notes", "")
    if not notes:
        return 0
    if len(notes) > 50:
        return 2
    return 1


def _extract_all_text(section):
    """セクション内の全テキストを結合して返す。"""
    parts = [
        section.get("title", ""),
        section.get("slide_title", ""),
        section.get("source", ""),
        section.get("notes", ""),
    ]
    for zone_name, spec in section.get("zones", {}).items():
        parts.append(_collect_strings(spec.get("data", {})))
    return " ".join(parts)


def _collect_strings(obj):
    """再帰的にオブジェクト内の全文字列を結合する。"""
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, list):
        return " ".join(_collect_strings(item) for item in obj)
    elif isinstance(obj, dict):
        return " ".join(_collect_strings(v) for v in obj.values())
    return ""


def evaluate_slides(content):
    """各スライドの品質を評価し、スコアと課題リストを返す。

    評価基準（合計最大14点/スライド）:
      - information_density: 1-4点
      - specificity: 0-2点
      - data_richness: 1-4点
      - source_quality: 0-2点
      - notes_quality: 0-2点

    8点未満のスライドは「弱い」と判定される。

    Returns:
        dict: slide_evaluations, weak_slide_indices, average_score, overall_grade
    """
    sections = content.get("sections", [])
    skip_types = {"title", "section_divider", "agenda", "summary"}

    slide_evaluations = []
    weak_indices = []
    total_score_sum = 0
    evaluated_count = 0

    for i, sec in enumerate(sections):
        st = sec.get("slide_type", sec.get("layout", ""))

        # 特殊スライドは評価対象外
        if st in skip_types:
            continue

        scores = {
            "information_density": _score_information_density(sec),
            "specificity": _score_specificity(sec),
            "data_richness": _score_data_richness(sec),
            "source_quality": _score_source_quality(sec),
            "notes_quality": _score_notes_quality(sec),
        }
        total = sum(scores.values())

        # 課題リストの生成
        issues = []
        if scores["information_density"] <= 2:
            issues.append("情報密度が低い")
        if scores["specificity"] == 0:
            issues.append("数値データがない")
        elif scores["specificity"] == 1:
            issues.append("比較表現が不足している")
        if scores["data_richness"] <= 1:
            issues.append("データ要素が少ない")
        if scores["source_quality"] == 0:
            issues.append("出典がない")
        elif scores["source_quality"] == 1:
            issues.append("出典が不十分（詳細を追加すべき）")
        if scores["notes_quality"] == 0:
            issues.append("スピーカーノートがない")
        elif scores["notes_quality"] == 1:
            issues.append("スピーカーノートが短い")

        is_weak = total < 8

        slide_evaluations.append({
            "index": i,
            "slide_title": sec.get("slide_title", sec.get("title", "")),
            "total_score": total,
            "scores": scores,
            "issues": issues,
            "is_weak": is_weak,
        })

        if is_weak:
            weak_indices.append(i)

        total_score_sum += total
        evaluated_count += 1

    average_score = round(total_score_sum / evaluated_count, 1) if evaluated_count > 0 else 0

    # 全体グレード判定
    if average_score >= 12:
        overall_grade = "A"
    elif average_score >= 10:
        overall_grade = "B"
    elif average_score >= 8:
        overall_grade = "C"
    else:
        overall_grade = "D"

    return {
        "slide_evaluations": slide_evaluations,
        "weak_slide_indices": weak_indices,
        "average_score": average_score,
        "overall_grade": overall_grade,
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 改善プロンプトテンプレート
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REFINEMENT_PROMPT_TEMPLATE = """
# Phase 3 改善指示書: コンテンツ品質向上

## 概要
以下のスライドは品質評価で基準（8点/14点）を下回りました。
リサーチデータを参照し、各スライドの指摘事項を改善してください。

## 改善対象スライド
{weak_slides_detail}

## 改善の具体的指示

### 共通ルール
1. **定量データの追加**: 数値、パーセンテージ、比較データを必ず含める
2. **structured_items の充実**: 各項目に keyword + 2〜3文の detail を付ける
3. **文脈的比較の追加**: 例「Xは業界平均の3倍」「前年比Y%増」
4. **アクションタイトルの強化**: 具体的な主張を含む述語文にする
5. **出典の明記**: 信頼性ある出典を20文字以上で記載する
6. **スピーカーノートの充実**: 50文字以上の補足説明を付ける

### スライド別の改善指示
{per_slide_instructions}

## 利用可能なリサーチデータ
{research_data_text}

## 出力形式

元のコンテンツJSON全体を出力してください。
改善対象のスライドのみ内容を更新し、それ以外のスライドはそのまま維持してください。

```json
{output_format_hint}
```
"""


def get_refinement_prompt(content, evaluation, research_data):
    """品質改善プロンプトを生成する。

    弱いスライドの具体的な課題と改善指示、リサーチデータを含む
    プロンプトを生成し、LLMによる改善を指示する。

    Args:
        content: 現在のコンテンツデータ
        evaluation: evaluate_slides() の返り値
        research_data: Phase 1 のリサーチデータ

    Returns:
        str: 改善プロンプト文字列
    """
    weak_indices = set(evaluation.get("weak_slide_indices", []))
    sections = content.get("sections", [])

    # 弱いスライドの詳細リスト
    weak_details = []
    per_slide_instructions = []

    for eval_item in evaluation.get("slide_evaluations", []):
        if not eval_item.get("is_weak"):
            continue

        idx = eval_item["index"]
        title = eval_item.get("slide_title", "")
        score = eval_item["total_score"]
        scores = eval_item.get("scores", {})
        issues = eval_item.get("issues", [])

        weak_details.append(
            f"### スライド {idx + 1}: {title}\n"
            f"- 合計スコア: {score}/14\n"
            f"- 内訳: 情報密度={scores.get('information_density', 0)}, "
            f"具体性={scores.get('specificity', 0)}, "
            f"データ豊富さ={scores.get('data_richness', 0)}, "
            f"出典={scores.get('source_quality', 0)}, "
            f"ノート={scores.get('notes_quality', 0)}\n"
            f"- 課題: {', '.join(issues)}"
        )

        # スライド別の改善指示を生成
        instructions = [f"#### スライド {idx + 1}: {title}"]
        if scores.get("information_density", 0) <= 2:
            instructions.append("- テキスト量を増やし、情報密度を高めてください（250文字以上を目標）")
        if scores.get("specificity", 0) == 0:
            instructions.append("- 定量データを追加してください: 数値、パーセンテージ、比較")
        elif scores.get("specificity", 0) == 1:
            instructions.append("- 比較表現を追加してください（例: 「Xは業界平均の3倍」）")
        if scores.get("data_richness", 0) <= 1:
            instructions.append(
                "- structured_items/items の要素数を増やしてください"
                "（各項目に keyword + 2〜3文の detail）"
            )
        if scores.get("source_quality", 0) < 2:
            instructions.append("- 出典を追加または詳細化してください（20文字以上）")
        if scores.get("notes_quality", 0) < 2:
            instructions.append("- スピーカーノートを充実させてください（50文字以上の補足説明）")
        instructions.append(
            f"- アクションタイトルを強化してください: 具体的な主張を含む述語文にする"
        )
        per_slide_instructions.append("\n".join(instructions))

    # リサーチデータサマリー
    research_lines = []
    for area in research_data.get("research_areas", []):
        research_lines.append(f"\n### {area.get('area_name', '')}")
        for f in area.get("findings", []):
            research_lines.append(f"  - {f}")
        for dp in area.get("data_points", []):
            research_lines.append(
                f"  📊 {dp.get('metric', '')}: {dp.get('value', '')} "
                f"({dp.get('source', '')}, {dp.get('date', '')})"
            )
        for ins in area.get("insights", []):
            research_lines.append(f"  💡 {ins}")

    # 出力形式のヒント
    output_hint = (
        '{{\n'
        f'  "title": "{content.get("title", "")}",\n'
        f'  "subtitle": "{content.get("subtitle", "")}",\n'
        f'  "date": "{content.get("date", "")}",\n'
        '  "sections": [\n'
        '    // 全スライドを出力（改善対象のみ更新、他はそのまま）\n'
        '  ]\n'
        '}}'
    )

    return REFINEMENT_PROMPT_TEMPLATE.format(
        weak_slides_detail="\n\n".join(weak_details),
        per_slide_instructions="\n\n".join(per_slide_instructions),
        research_data_text="\n".join(research_lines),
        output_format_hint=output_hint,
    )
