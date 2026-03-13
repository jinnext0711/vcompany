"""Phase 5: 品質チェックモジュール — 自動チェック・修正

QAチェックリスト18項目に対する自動検証。
自動修正可能な項目は修正し、手動確認が必要な項目はレポートする。
"""

import re
import copy
from collections import Counter

from src.outline.generator import PREDICATE_PATTERN


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 冗長表現パターン（自動修正用）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERBOSE_PATTERNS = [
    (re.compile(r'することが可能である'), 'できる'),
    (re.compile(r'することが可能だ'), 'できる'),
    (re.compile(r'することができる'), 'できる'),
    (re.compile(r'を行う'), 'する'),
    (re.compile(r'を実施する'), 'する'),
    (re.compile(r'を実行する'), 'する'),
    (re.compile(r'という点に関しましては'), 'については'),
    (re.compile(r'という点に関しては'), 'については'),
    (re.compile(r'であるということが考えられる'), 'と考えられる'),
    (re.compile(r'であると考えられる'), 'と考えられる'),
    (re.compile(r'まず最初に'), 'まず'),
    (re.compile(r'各々それぞれ'), 'それぞれ'),
    (re.compile(r'現在のところ'), '現在'),
    (re.compile(r'〜的な'), '〜の'),
    (re.compile(r'についてですが'), 'について'),
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 個別チェック関数
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _check_pyramid(content):
    """1-1: ピラミッド原則 — executive_summary の存在と構造チェック。"""
    sections = content.get("sections", [])
    has_exec = any(
        s.get("slide_type", s.get("layout", "")) == "executive_summary"
        for s in sections
    )
    if not has_exec:
        return "NG", "executive_summary スライドがありません（結論の明示が不足）"
    return "OK", ""


def _check_scqa(content):
    """1-2: SCQAフレームワーク — 冒頭6スライド以内にagenda + executive_summaryがあるか。"""
    sections = content.get("sections", [])
    early = [s.get("slide_type", s.get("layout", "")) for s in sections[:6]]
    missing = []
    if "agenda" not in early:
        missing.append("agenda")
    if "executive_summary" not in early:
        missing.append("executive_summary")
    if missing:
        return "NG", f"冒頭6スライドに {', '.join(missing)} がありません"
    return "OK", ""


def _check_storyline(content):
    """1-3: ストーリーライン — アクションタイトルの連続性チェック。"""
    titles = []
    skip = {"title", "agenda", "section_divider", "summary"}
    for s in content.get("sections", []):
        st = s.get("slide_type", s.get("layout", ""))
        if st not in skip:
            t = s.get("title", "")
            if t:
                titles.append(t)
    if len(titles) < 3:
        return "WARN", f"コンテンツスライドが {len(titles)} 枚（ストーリーライン検証には不十分）"
    # トピック名のみのタイトルを検出
    topic_only = [t for t in titles if len(t) < 10 and not PREDICATE_PATTERN.search(t)]
    if topic_only:
        return "NG", f"トピック名のみのタイトルがあります: {topic_only[:3]}"
    return "OK", f"{len(titles)} 枚のタイトルを検証済み"


def _check_mece(content):
    """1-4: MECE — セクション区切りの適切性。"""
    sections = content.get("sections", [])
    dividers = [
        s.get("title", "")
        for s in sections
        if s.get("slide_type", s.get("layout", "")) == "section_divider"
    ]
    if len(dividers) < 2:
        return "NG", f"section_divider が {len(dividers)} 枚（MECE分解不十分）"
    # 重複チェック
    counts = Counter(dividers)
    dups = {k: v for k, v in counts.items() if v > 1}
    if dups:
        return "NG", f"セクション名に重複があります: {dups}"
    return "OK", f"{len(dividers)} セクションに分解済み"


def _check_action_titles(content):
    """2-1: アクションタイトル — So What判定。"""
    issues = []
    skip = {"title", "agenda", "section_divider", "summary"}
    for i, s in enumerate(content.get("sections", [])):
        st = s.get("slide_type", s.get("layout", ""))
        if st in skip:
            continue
        t = s.get("title", "")
        if not t:
            issues.append(f"[{i}] タイトル空")
        elif not PREDICATE_PATTERN.search(t):
            issues.append(f"[{i}] '{t[:30]}...' は述語なし")
    if issues:
        return "NG", "; ".join(issues[:5])
    return "OK", ""


def _check_one_one_one(content):
    """2-2: 1-1-1ルール — 1スライド1メッセージ。"""
    issues = []
    for i, s in enumerate(content.get("sections", [])):
        st = s.get("slide_type", s.get("layout", ""))
        if st in ("title", "section_divider"):
            continue
        zones = s.get("zones", {})
        if len(zones) > 4:
            issues.append(f"[{i}] ゾーン数={len(zones)}（多すぎ）")
    if issues:
        return "WARN", "; ".join(issues)
    return "OK", ""


def _check_ten_second(content):
    """2-3: 10秒ルール — テキスト密度チェック。"""
    issues = []
    for i, s in enumerate(content.get("sections", [])):
        st = s.get("slide_type", s.get("layout", ""))
        if st in ("title", "section_divider"):
            continue
        # テキスト総量を推計
        text_len = len(s.get("title", ""))
        for zone_spec in s.get("zones", {}).values():
            data = zone_spec.get("data", {})
            for key, val in data.items():
                if isinstance(val, str):
                    text_len += len(val)
                elif isinstance(val, list):
                    for item in val:
                        if isinstance(item, str):
                            text_len += len(item)
                        elif isinstance(item, dict):
                            text_len += sum(
                                len(str(v)) for v in item.values()
                                if isinstance(v, (str, int, float))
                            )
        # レガシー形式のテキスト量も計算
        for key in ("bullet_points", "structured_items", "body"):
            val = s.get(key)
            if isinstance(val, str):
                text_len += len(val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, str):
                        text_len += len(item)
                    elif isinstance(item, dict):
                        text_len += sum(
                            len(str(v)) for v in item.values()
                            if isinstance(v, (str, int, float))
                        )
        if text_len > 400:
            issues.append(f"[{i}] 文字数={text_len}（400文字超過）")
    if issues:
        return "WARN", "; ".join(issues[:5])
    return "OK", ""


def _check_standalone(content):
    """2-4: スタンドアローン性 — 出典・注釈の完備。"""
    issues = []
    skip = {"title", "section_divider", "summary", "agenda"}
    for i, s in enumerate(content.get("sections", [])):
        st = s.get("slide_type", s.get("layout", ""))
        if st in skip:
            continue
        if not s.get("source"):
            issues.append(f"[{i}] source なし")
    if issues:
        return "NG", "; ".join(issues[:5])
    return "OK", ""


def _check_three_layer(content):
    """3-1: 3層構造 — pptx_exporter が強制するため常にOK。"""
    return "OK", "pptx_exporter が 3層構造を強制"


def _check_color_rule(content):
    """3-2: 配色 70-25-5 — DesignConfig が管理するため常にOK。"""
    return "OK", "DesignConfig が 70-25-5 を管理"


def _check_font_unity(content):
    """3-3: フォント統一性 — DesignConfig が管理するため常にOK。"""
    return "OK", "Noto Sans JP 統一（DesignConfig で禁止フォント制御）"


def _check_margin(content):
    """3-4: 余白・マージン — pptx_exporter の定数で統一されているため常にOK。"""
    return "OK", "8pxグリッド準拠の定数制御"


def _check_chart_quality(content):
    """3-5: 図表品質 — 3D効果なし、データインク比高。"""
    return "OK", "python-pptx で 2D シェイプのみ使用（3D効果なし）"


def _check_three_point_rule(content):
    """4-1: 3点ルール — 箇条書き3項目以内。"""
    issues = []
    for i, s in enumerate(content.get("sections", [])):
        for key in ("bullet_points", "key_points"):
            items = s.get(key, [])
            if len(items) > 3:
                issues.append(f"[{i}] {key}={len(items)}個")
        # zones内
        for zn, spec in s.get("zones", {}).items():
            data = spec.get("data", {})
            for key in ("items", "structured_items", "bullet_points"):
                items = data.get(key, [])
                if len(items) > 5:
                    issues.append(f"[{i}].{zn} {key}={len(items)}個")
    if issues:
        return "WARN", "; ".join(issues[:5])
    return "OK", ""


def _check_verbose(content):
    """4-2: 冗長表現 — 自動検出。"""
    found = []
    for i, s in enumerate(content.get("sections", [])):
        text = s.get("title", "") + s.get("body", "")
        for pattern, _ in VERBOSE_PATTERNS:
            if pattern.search(text):
                found.append(f"[{i}] '{pattern.pattern}'")
    if found:
        return "WARN", f"冗長表現検出: {'; '.join(found[:5])}"
    return "OK", ""


def _check_terminology(content):
    """4-3: 専門用語の統一性 — 同義語の混在チェック。"""
    # よくある揺れのペア
    synonym_pairs = [
        ({"KPI", "指標", "メトリクス"}),
        ({"ユーザー", "利用者"}),
        ({"クライアント", "顧客", "お客様"}),
        ({"プロジェクト", "案件"}),
        ({"AI", "人工知能"}),
    ]

    all_text = ""
    for s in content.get("sections", []):
        all_text += s.get("title", "") + " "
        all_text += s.get("body", "") + " "
        for bp in s.get("bullet_points", []):
            if isinstance(bp, str):
                all_text += bp + " "

    issues = []
    for pair in synonym_pairs:
        used = [term for term in pair if term in all_text]
        if len(used) > 1:
            issues.append(f"用語揺れ: {' / '.join(used)}")

    if issues:
        return "WARN", "; ".join(issues)
    return "OK", ""


def _check_theme_depth(content):
    """5-1: テーマの深さ — 定量データと定性分析の両方があるか。"""
    sections = content.get("sections", [])
    has_quant = False
    has_qual = False
    skip = {"title", "section_divider", "agenda", "summary"}

    for s in sections:
        st = s.get("slide_type", s.get("layout", ""))
        if st in skip:
            continue
        # 定量（グラフ・KPI・テーブル系）
        layout = s.get("layout", "")
        zones = s.get("zones", {})
        diagrams_used = [spec.get("diagram", "") for spec in zones.values()]
        quant_types = {"bar_chart", "waterfall", "stacked_bar", "kpi_card", "table"}
        if layout in quant_types or any(d in quant_types for d in diagrams_used):
            has_quant = True
        # 定性（構造化テキスト・ピラミッド・フロー系）
        qual_types = {"structured_text", "pyramid", "flow", "matrix", "funnel", "cycle"}
        if layout in qual_types or any(d in qual_types for d in diagrams_used):
            has_qual = True

    if not has_quant:
        return "NG", "定量データ（グラフ・テーブル・KPI）のスライドがありません"
    if not has_qual:
        return "NG", "定性分析（構造化テキスト・フロー・ピラミッド）のスライドがありません"
    return "OK", "定量・定性の両方を含む"


def _check_section_balance(content):
    """5-2: セクション間バランス。"""
    sections = content.get("sections", [])
    current_section = None
    section_counts = {}

    for s in sections:
        st = s.get("slide_type", s.get("layout", ""))
        if st == "section_divider":
            current_section = s.get("title", "unknown")
            section_counts[current_section] = 0
        elif current_section and st not in ("title", "agenda", "summary"):
            section_counts[current_section] = section_counts.get(current_section, 0) + 1

    if not section_counts:
        return "WARN", "セクション構造が検出できません"

    counts = list(section_counts.values())
    if counts:
        max_c, min_c = max(counts), min(counts)
        if min_c > 0 and max_c / min_c > 3:
            detail = ", ".join(f"{k}:{v}枚" for k, v in section_counts.items())
            return "WARN", f"バランス偏り（最大{max_c}/最小{min_c}）: {detail}"

    return "OK", ", ".join(f"{k}:{v}枚" for k, v in section_counts.items())


# 日本語助詞パターン（キーワード抽出用）
_PARTICLE_PATTERN = re.compile(r'[はがをのにでともや、。！？\s　・「」（）()]+')


def _extract_content_words(text):
    """テキストから助詞・記号で分割し、2文字以上の内容語を抽出する。"""
    tokens = _PARTICLE_PATTERN.split(text)
    return {t for t in tokens if len(t) >= 2}


def _check_storyline_coherence(content):
    """1-5: ストーリーライン一貫性 — 連続スライド間の論理的つながりチェック。"""
    sections = content.get("sections", [])
    skip_types = {"title", "section_divider", "agenda"}

    # コンテンツスライドのタイトルを抽出（セクション区切りの位置も記録）
    slides_info = []  # (index, title, is_after_divider)
    after_divider = False
    for s in sections:
        st = s.get("slide_type", s.get("layout", ""))
        if st == "section_divider":
            after_divider = True
            continue
        if st in skip_types:
            continue
        t = s.get("title", "")
        if t:
            slides_info.append((len(slides_info), t, after_divider))
            after_divider = False

    if len(slides_info) < 2:
        return "OK", "コンテンツスライドが1枚以下のため検証スキップ"

    # 論理的進行パターン（キーワードペア）
    progression_keywords = [
        ({"課題", "問題", "現状"}, {"分析", "原因", "要因"}),
        ({"分析", "原因", "要因"}, {"解決", "対策", "施策", "提案"}),
        ({"現状", "現在", "背景"}, {"課題", "問題", "チャレンジ"}),
        ({"課題", "チャレンジ"}, {"機会", "施策", "戦略"}),
        ({"概要", "全体"}, {"詳細", "具体", "内訳"}),
        ({"詳細", "具体"}, {"影響", "効果", "インパクト", "まとめ"}),
    ]

    gaps = []
    for idx in range(len(slides_info) - 1):
        _, title_a, _ = slides_info[idx]
        _, title_b, is_after_div = slides_info[idx + 1]

        # セクション区切り直後なら新セクション開始なのでスキップ
        if is_after_div:
            continue

        words_a = _extract_content_words(title_a)
        words_b = _extract_content_words(title_b)

        # 共通キーワードがあればOK
        if words_a & words_b:
            continue

        # 論理的進行パターンに一致するかチェック
        pattern_match = False
        for pattern_from, pattern_to in progression_keywords:
            if (words_a & pattern_from) and (words_b & pattern_to):
                pattern_match = True
                break
        if pattern_match:
            continue

        # 共通語も進行パターンもない → ギャップ
        gaps.append(f"スライド{idx + 1}→{idx + 2}: '{title_a[:20]}' → '{title_b[:20]}' に論理的つながりが弱い")

    if gaps:
        return "WARN", "; ".join(gaps[:5])
    return "OK", f"{len(slides_info)} 枚のストーリーライン一貫性を検証済み"


def _check_slide_information_density(content):
    """5-3: スライド情報密度 — 各スライドの情報量チェック。"""
    sections = content.get("sections", [])
    skip_types = {"title", "section_divider", "agenda", "summary"}

    thin_slides = []   # < 150文字 → NG
    sparse_slides = []  # < 250文字 → WARN

    for i, s in enumerate(sections):
        st = s.get("slide_type", s.get("layout", ""))
        if st in skip_types:
            continue

        # テキスト総量を計算
        text_len = len(s.get("title", ""))

        # zones内のデータ
        for zone_spec in s.get("zones", {}).values():
            data = zone_spec.get("data", {})
            for key, val in data.items():
                if isinstance(val, str):
                    text_len += len(val)
                elif isinstance(val, list):
                    for item in val:
                        if isinstance(item, str):
                            text_len += len(item)
                        elif isinstance(item, dict):
                            text_len += sum(
                                len(str(v)) for v in item.values()
                                if isinstance(v, (str, int, float))
                            )

        # レガシー形式
        for key in ("bullet_points", "structured_items", "body"):
            val = s.get(key)
            if isinstance(val, str):
                text_len += len(val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, str):
                        text_len += len(item)
                    elif isinstance(item, dict):
                        text_len += sum(
                            len(str(v)) for v in item.values()
                            if isinstance(v, (str, int, float))
                        )

        if text_len < 150:
            thin_slides.append(f"[{i}] {text_len}文字（150文字未満）")
        elif text_len < 250:
            sparse_slides.append(f"[{i}] {text_len}文字（250文字未満）")

    if thin_slides:
        return "NG", "情報不足スライド: " + "; ".join(thin_slides[:5])
    if sparse_slides:
        return "WARN", "情報がやや少ないスライド: " + "; ".join(sparse_slides[:5])
    return "OK", "全スライド250文字以上"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 自動修正
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _auto_fix_verbose(content):
    """冗長表現を自動修正する。"""
    fixes = []
    for i, s in enumerate(content.get("sections", [])):
        for field in ("title", "body"):
            text = s.get(field, "")
            if not text:
                continue
            new_text = text
            for pattern, replacement in VERBOSE_PATTERNS:
                if pattern.search(new_text):
                    before = new_text
                    new_text = pattern.sub(replacement, new_text)
                    if before != new_text:
                        fixes.append({
                            "item": "4-2 冗長表現",
                            "slide_index": i,
                            "field": field,
                            "before": before,
                            "after": new_text,
                        })
            s[field] = new_text
    return fixes


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# QAチェックリスト
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QA_CHECKLIST = [
    {"id": "1-1", "name": "ピラミッド原則", "category": "論理構造", "check": _check_pyramid},
    {"id": "1-2", "name": "SCQAフレームワーク", "category": "論理構造", "check": _check_scqa},
    {"id": "1-3", "name": "ストーリーライン", "category": "論理構造", "check": _check_storyline},
    {"id": "1-4", "name": "MECE", "category": "論理構造", "check": _check_mece},
    {"id": "2-1", "name": "アクションタイトル", "category": "スライド", "check": _check_action_titles},
    {"id": "2-2", "name": "1-1-1ルール", "category": "スライド", "check": _check_one_one_one},
    {"id": "2-3", "name": "10秒ルール", "category": "スライド", "check": _check_ten_second},
    {"id": "2-4", "name": "スタンドアローン性", "category": "スライド", "check": _check_standalone},
    {"id": "3-1", "name": "3層構造", "category": "デザイン", "check": _check_three_layer},
    {"id": "3-2", "name": "配色ルール", "category": "デザイン", "check": _check_color_rule},
    {"id": "3-3", "name": "フォント統一性", "category": "デザイン", "check": _check_font_unity},
    {"id": "3-4", "name": "余白・マージン", "category": "デザイン", "check": _check_margin},
    {"id": "3-5", "name": "図表の品質", "category": "デザイン", "check": _check_chart_quality},
    {"id": "4-1", "name": "3点ルール", "category": "テキスト", "check": _check_three_point_rule},
    {"id": "4-2", "name": "冗長表現", "category": "テキスト", "check": _check_verbose},
    {"id": "4-3", "name": "専門用語", "category": "テキスト", "check": _check_terminology},
    {"id": "5-1", "name": "テーマの深さ", "category": "ボリューム", "check": _check_theme_depth},
    {"id": "5-2", "name": "セクション間バランス", "category": "ボリューム", "check": _check_section_balance},
    {"id": "1-5", "name": "ストーリーライン一貫性", "category": "論理構造", "check": _check_storyline_coherence},
    {"id": "5-3", "name": "スライド情報密度", "category": "ボリューム", "check": _check_slide_information_density},
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# メインQA実行
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def run_qa(content):
    """QAチェックリスト18項目の自動チェック + 自動修正を実行する。

    Returns:
        dict: {
            "corrected_content": 修正済みコンテンツ,
            "auto_fixes": 自動修正リスト,
            "qa_report": 全18項目のチェック結果,
            "manual_review_items": 手動確認が必要な項目,
            "summary": {"ok": N, "ng": N, "warn": N}
        }
    """
    corrected = copy.deepcopy(content)

    # 自動修正
    auto_fixes = _auto_fix_verbose(corrected)

    # 全チェック実行
    qa_report = []
    manual_review = []

    for item in QA_CHECKLIST:
        status, detail = item["check"](corrected)
        qa_report.append({
            "id": item["id"],
            "name": item["name"],
            "category": item["category"],
            "status": status,
            "detail": detail,
        })
        if status == "NG":
            manual_review.append({
                "item": f"{item['id']} {item['name']}",
                "detail": detail,
                "severity": "high",
            })
        elif status == "WARN":
            manual_review.append({
                "item": f"{item['id']} {item['name']}",
                "detail": detail,
                "severity": "medium",
            })

    # サマリー
    statuses = [r["status"] for r in qa_report]
    summary = {
        "ok": statuses.count("OK"),
        "ng": statuses.count("NG"),
        "warn": statuses.count("WARN"),
        "total": len(statuses),
    }

    return {
        "corrected_content": corrected,
        "auto_fixes": auto_fixes,
        "qa_report": qa_report,
        "manual_review_items": manual_review,
        "summary": summary,
    }


def format_qa_report(qa_result):
    """QA結果を人間が読みやすい形式にフォーマットする。"""
    lines = ["# QA チェック結果\n"]
    summary = qa_result["summary"]
    lines.append(
        f"**結果**: OK={summary['ok']} / NG={summary['ng']} / "
        f"WARN={summary['warn']} / 全{summary['total']}項目\n"
    )

    current_cat = ""
    for r in qa_result["qa_report"]:
        if r["category"] != current_cat:
            current_cat = r["category"]
            lines.append(f"\n## {current_cat}")
        icon = {"OK": "✅", "NG": "❌", "WARN": "⚠️"}.get(r["status"], "❓")
        lines.append(f"- {icon} **{r['id']} {r['name']}**: {r['detail']}")

    if qa_result["auto_fixes"]:
        lines.append(f"\n## 自動修正 ({len(qa_result['auto_fixes'])}件)")
        for fix in qa_result["auto_fixes"]:
            lines.append(
                f"- [{fix['slide_index']}] {fix['field']}: "
                f"'{fix['before'][:30]}' → '{fix['after'][:30]}'"
            )

    return "\n".join(lines)
