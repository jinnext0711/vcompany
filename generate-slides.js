const PptxGenJS = require("pptxgenjs");

// ============================
// 絶対禁止チェックリスト（コード書く前に確認）
// - アクセントライン禁止
// - 装飾的な円・楕円禁止
// - ◎○△× 記号禁止 → テキスト+色分け
// - Unicode bullet "•" 禁止 → bullet: true
// - 色コードに # 禁止
// - オプションオブジェクト再利用禁止
// ============================

// ============================
// デザインシステム（v2: LAYOUT_16x9）
// ============================
const C = {
  primary: "1E2761",
  primaryDark: "141C4A",
  accent: "E67E22",
  text: "333333",
  textLight: "FFFFFF",
  surface: "F5F7FA",
  surfaceAlt: "EBF0F7",
  border: "E5E7EB",
  success: "27AE60",
  muted: "8899AA",
  // 評価色（テーブル用）
  evalBest: "0D7C3D",
  evalGood: "333333",
  evalLimited: "F59E0B",
  evalNone: "C62828",
  // 推奨列ハイライト
  highlight: "F0F4FF",
};

// v2 座標テンプレート（LAYOUT_16x9: 10" x 5.625"）
const L = {
  W: 10,
  H: 5.625,
  mx: 0.5,        // 左右マージン
  titleY: 0.3,    // タイトル y
  titleH: 0.6,    // タイトル h
  bodyTop: 1.1,   // ボディ開始 y
  sourceY: 5.15,  // ソース表記 y
  sourceH: 0.3,   // ソース表記 h
};
L.cw = L.W - L.mx * 2;           // コンテンツ幅 = 9.0
L.bodyH = L.sourceY - L.bodyTop;  // ボディ高さ = 4.05

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_16x9";
pptx.author = "vCompany";
let page = 1;

// ============================
// ヘルパー関数
// ============================

// shadow ファクトリ（毎回新規オブジェクト生成）
function makeShadow(opts = {}) {
  return {
    type: "outer",
    blur: opts.blur || 3,
    offset: opts.offset || 2,
    color: opts.color || "000000",
    opacity: opts.opacity || 0.15,
  };
}

function header(s, title) {
  s.addText(title, {
    x: L.mx, y: L.titleY, w: L.cw, h: L.titleH,
    fontSize: 20, fontFace: "Georgia", bold: true,
    color: C.primary, valign: "top", wrap: true,
  });
}

function sourceNote(s, src) {
  if (src) {
    s.addText("Source: " + src, {
      x: L.mx, y: L.sourceY, w: L.cw - 1, h: L.sourceH,
      fontSize: 8, fontFace: "Calibri", color: C.muted,
    });
  }
  s.addText(String(page++), {
    x: L.W - 1, y: L.sourceY, w: 0.5, h: L.sourceH,
    fontSize: 8, fontFace: "Calibri", color: C.muted, align: "right",
  });
}

function sourceDark(s, src) {
  if (src) {
    s.addText("Source: " + src, {
      x: L.mx, y: L.sourceY, w: L.cw - 1, h: L.sourceH,
      fontSize: 8, fontFace: "Calibri", color: "7799BB",
    });
  }
  s.addText(String(page++), {
    x: L.W - 1, y: L.sourceY, w: 0.5, h: L.sourceH,
    fontSize: 8, fontFace: "Calibri", color: "7799BB", align: "right",
  });
}

// 棒グラフ（シェイプベース）
function barChart(s, items, o) {
  const x0 = o.x, y0 = o.y, w = o.w, h = o.h;
  const max = Math.max(...items.map(i => i.value));
  const n = items.length;
  const gap = 0.08;
  const bw = Math.min((w - gap * (n + 1)) / n, 0.85);
  const totalW = n * bw + (n + 1) * gap;
  const sx = x0 + (w - totalW) / 2 + gap;
  const ch = h * 0.68;
  const cb = y0 + h * 0.85;

  // グリッドライン
  for (let i = 0; i <= 3; i++) {
    s.addShape(pptx.shapes.RECTANGLE, {
      x: x0, y: cb - (ch * i) / 3, w, h: 0.006,
      fill: { color: C.border },
    });
  }

  items.forEach((it, i) => {
    const bh = max > 0 ? (it.value / max) * ch : 0;
    const bx = sx + i * (bw + gap);
    const by = cb - bh;
    const hl = o.highlight === it.label;
    const col = hl ? C.accent : C.primary;

    s.addShape(pptx.shapes.RECTANGLE, {
      x: bx, y: by, w: bw, h: bh,
      fill: { color: col }, rectRadius: 0.03,
    });
    s.addText(String(it.value), {
      x: bx, y: by - 0.22, w: bw, h: 0.2,
      fontSize: 9, fontFace: "Calibri", bold: true, color: col, align: "center",
    });
    s.addText(it.label, {
      x: bx - 0.05, y: cb + 0.03, w: bw + 0.1, h: 0.28,
      fontSize: 7, fontFace: "Calibri", color: C.text, align: "center", wrap: true,
    });
  });

  if (o.insight) {
    s.addText(o.insight, {
      x: x0, y: y0 - 0.02, w, h: 0.2,
      fontSize: 8, fontFace: "Calibri", color: C.muted,
    });
  }

  // ハイライト凡例（色分けの理由を明示）
  if (o.highlight) {
    const legY = cb + 0.35;
    s.addShape(pptx.shapes.RECTANGLE, {
      x: x0 + w - 1.8, y: legY, w: 0.15, h: 0.12,
      fill: { color: C.accent }, rectRadius: 0.02,
    });
    s.addText(o.highlight + "（注目）", {
      x: x0 + w - 1.6, y: legY - 0.02, w: 1.5, h: 0.16,
      fontSize: 7, fontFace: "Calibri", color: C.accent,
    });
  }
}

// KPIカード
function kpiCard(s, val, label, o) {
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: o.x, y: o.y, w: o.w, h: o.h,
    fill: { color: C.surfaceAlt }, rectRadius: 0.1,
    line: { color: C.border, width: 0.75 },
    shadow: makeShadow(),
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: o.x + 0.12, y: o.y + 0.15, w: 0.04, h: o.h - 0.3,
    fill: { color: C.accent },
  });
  s.addText(val, {
    x: o.x + 0.28, y: o.y + 0.2, w: o.w - 0.4, h: 0.7,
    fontSize: 28, fontFace: "Georgia", bold: true, color: C.primary,
  });
  s.addText(label, {
    x: o.x + 0.28, y: o.y + 0.9, w: o.w - 0.4, h: o.h - 1.1,
    fontSize: 9, fontFace: "Calibri", color: C.text, wrap: true,
  });
}

// 構造化テキスト（アクセントバー + キーワード + 説明）
function structuredItems(s, items, o) {
  const itemH = Math.min(o.h / items.length, 1.0);
  items.forEach((it, i) => {
    const iy = o.y + i * itemH;
    const col = i % 2 === 0 ? C.primary : C.accent;
    s.addShape(pptx.shapes.RECTANGLE, {
      x: o.x, y: iy + 0.03, w: 0.04, h: itemH - 0.08,
      fill: { color: col },
    });
    s.addText(it.keyword, {
      x: o.x + 0.14, y: iy, w: o.w - 0.2, h: 0.26,
      fontSize: 11, fontFace: "Georgia", bold: true, color: C.primary,
    });
    const d = it.detail.length > 100 ? it.detail.substring(0, 97) + "..." : it.detail;
    s.addText(d, {
      x: o.x + 0.14, y: iy + 0.26, w: o.w - 0.2, h: itemH - 0.32,
      fontSize: 9, fontFace: "Calibri", color: C.text, wrap: true,
    });
  });
}

// テーブルセル生成（評価テキスト+色分け）
function evalCell(text, level) {
  const colorMap = { best: C.evalBest, good: C.evalGood, limited: C.evalLimited, none: C.evalNone };
  const color = colorMap[level] || C.text;
  return {
    text, options: {
      fontSize: 9, fontFace: "Calibri", color,
      align: "center", valign: "middle",
      border: [
        { type: "none" }, { type: "none" },
        { type: "solid", pt: 0.3, color: C.border }, { type: "none" }
      ],
    }
  };
}

// ============================
// SLIDE 1: タイトル
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: C.primaryDark };
  // 装飾的な円やアクセントラインは配置しない
  s.addText("Claude Code とは", {
    x: L.mx, y: 1.2, w: 8, h: 0.7,
    fontSize: 34, fontFace: "Georgia", bold: true, color: C.textLight,
  });
  s.addText("AIコーディングアシスタントの全貌と導入戦略", {
    x: L.mx, y: 1.95, w: 8, h: 0.5,
    fontSize: 18, fontFace: "Georgia", color: "AABBCC",
  });
  s.addText("自律型開発エージェントによる開発生産性革命と段階的導入ロードマップ", {
    x: L.mx, y: 2.7, w: 8, h: 0.4,
    fontSize: 12, fontFace: "Calibri", color: "8899AA", wrap: true,
  });
  s.addText("2026-03-13", {
    x: L.mx, y: 4.2, w: 3, h: 0.3,
    fontSize: 10, fontFace: "Calibri", color: "7799BB",
  });
  sourceDark(s, null);
}

// ============================
// SLIDE 2: 市場規模（棒グラフ + KPI）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "AIコーディングツール市場は年率25%成長、2030年に160億ドル規模に到達する");
  barChart(s, [
    { label: "2023", value: 28 },
    { label: "2024", value: 40 },
    { label: "2025", value: 52 },
    { label: "2027(予)", value: 85 },
    { label: "2030(予)", value: 160 },
  ], {
    x: L.mx, y: L.bodyTop, w: L.cw * 0.58, h: L.bodyH,
    highlight: "2030(予)", insight: "AIコーディングツール市場規模（億ドル）",
  });
  kpiCard(s, "CAGR 25%+", "年平均成長率\nSaaS平均15%の1.7倍", {
    x: L.mx + L.cw * 0.62, y: L.bodyTop + 0.3, w: L.cw * 0.36, h: 2.0,
  });
  sourceNote(s, "Gartner AI Coding Assistant Market Report, 2025");
}

// ============================
// SLIDE 3: 普及率（棒グラフ × 2）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "開発者の76%がAIツールを常用する一方、日本企業の導入率は米国の半分以下");
  const hw = L.cw * 0.47;
  barChart(s, [
    { label: "2022", value: 29 }, { label: "2023", value: 44 },
    { label: "2024", value: 62 }, { label: "2025", value: 76 }, { label: "2026(予)", value: 85 },
  ], { x: L.mx, y: L.bodyTop, w: hw, h: L.bodyH, highlight: "2025", insight: "開発者のAIツール日常使用率（%）" });
  barChart(s, [
    { label: "米国", value: 45 }, { label: "欧州", value: 35 },
    { label: "日本", value: 22 }, { label: "F500", value: 45 }, { label: "F500(26予)", value: 65 },
  ], { x: L.mx + L.cw * 0.53, y: L.bodyTop, w: hw, h: L.bodyH, highlight: "日本", insight: "企業のAIツール導入率（%）" });
  sourceNote(s, "Stack Overflow Developer Survey 2025 / McKinsey Digital 2025");
}

// ============================
// SLIDE 4: 4世代の進化（プロセスフロー）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "補完型から自律型へ4世代の進化 — 生産性差は最大5倍に拡大");
  const steps = [
    { num: "1", title: "コード補完型", sub: "Copilot (2021年〜)", detail: "1行補完\n8K tokens\n+15-30%" },
    { num: "2", title: "マルチファイル編集", sub: "Cursor / Cline (2023年〜)", detail: "ファイル横断編集\n128K tokens" },
    { num: "3", title: "自律エージェント型", sub: "Claude Code (2025年〜)", detail: "自律実行\n200K tokens\n2-10倍" },
    { num: "4", title: "マルチエージェント", sub: "Sub-agent (2025後半〜)", detail: "並列処理\n60-70%短縮" },
  ];
  const bw = (L.cw - 0.3 * 3) / 4;
  steps.forEach((st, i) => {
    const bx = L.mx + i * (bw + 0.3);
    const isHL = i === 2;
    // ステップ番号（小さな四角）
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: bx + bw / 2 - 0.15, y: L.bodyTop, w: 0.3, h: 0.3,
      fill: { color: isHL ? C.accent : C.primary }, rectRadius: 0.05,
    });
    s.addText(st.num, {
      x: bx + bw / 2 - 0.15, y: L.bodyTop, w: 0.3, h: 0.3,
      fontSize: 12, fontFace: "Calibri", bold: true, color: C.textLight, align: "center", valign: "middle",
    });
    s.addText(st.title, {
      x: bx, y: L.bodyTop + 0.38, w: bw, h: 0.35,
      fontSize: 11, fontFace: "Georgia", bold: true, color: isHL ? C.accent : C.primary, align: "center", wrap: true,
    });
    s.addText(st.sub, {
      x: bx, y: L.bodyTop + 0.73, w: bw, h: 0.22,
      fontSize: 8, fontFace: "Calibri", color: C.muted, align: "center", wrap: true,
    });
    // 詳細カード
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: bx, y: L.bodyTop + 1.05, w: bw, h: 2.4,
      fill: { color: isHL ? "FFF7ED" : C.surfaceAlt }, rectRadius: 0.06,
      line: { color: isHL ? C.accent : C.border, width: isHL ? 1.5 : 0.5 },
    });
    s.addText(st.detail, {
      x: bx + 0.08, y: L.bodyTop + 1.15, w: bw - 0.16, h: 2.2,
      fontSize: 9, fontFace: "Calibri", color: C.text, wrap: true, valign: "top",
    });
    // 矢印（最後以外）
    if (i < 3) {
      s.addText("\u2192", {
        x: bx + bw, y: L.bodyTop + 0.38, w: 0.3, h: 0.35,
        fontSize: 16, color: C.accent, align: "center", valign: "middle",
      });
    }
  });
  sourceNote(s, "Gartner 2025 / Anthropic / SWE-bench 2025");
}

// ============================
// SLIDE 5: Claude Code概要（サイクル + KPI）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "Claude Codeは開発ライフサイクル全体を自律実行するCLIエージェント");
  const cx = L.mx + 2.6, cy = L.bodyTop + L.bodyH * 0.48;
  const items = [
    { t: "コード理解", d: "200Kトークンで全体読解" },
    { t: "設計・推論", d: "Extended Thinking" },
    { t: "実装", d: "マルチファイル横断編集" },
    { t: "テスト", d: "自動実行・自動修正" },
    { t: "Git操作", d: "commit/PR/レビュー" },
  ];
  // 中央ラベル（円は情報を持つため装飾ではない）
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: cx - 0.55, y: cy - 0.35, w: 1.1, h: 0.7,
    fill: { color: C.primary }, rectRadius: 0.1,
  });
  s.addText("自律型\nエージェント", {
    x: cx - 0.55, y: cy - 0.35, w: 1.1, h: 0.7,
    fontSize: 10, fontFace: "Georgia", bold: true, color: C.textLight, align: "center", valign: "middle", wrap: true,
  });
  items.forEach((it, i) => {
    const angle = (2 * Math.PI * i) / 5 - Math.PI / 2;
    const rx = 2.1, ry = 1.6;
    const nx = cx + rx * Math.cos(angle);
    const ny = cy + ry * Math.sin(angle);
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: nx - 0.75, y: ny - 0.35, w: 1.5, h: 0.7,
      fill: { color: C.surfaceAlt }, rectRadius: 0.06,
      line: { color: C.primary, width: 0.75 },
    });
    s.addText(it.t, {
      x: nx - 0.7, y: ny - 0.32, w: 1.4, h: 0.28,
      fontSize: 10, fontFace: "Georgia", bold: true, color: C.primary, align: "center",
    });
    s.addText(it.d, {
      x: nx - 0.7, y: ny - 0.02, w: 1.4, h: 0.3,
      fontSize: 8, fontFace: "Calibri", color: C.text, align: "center", wrap: true,
    });
  });
  // KPIカード（右）
  kpiCard(s, "200K", "コンテキスト(tokens)\nCopilotの25倍", {
    x: L.mx + L.cw * 0.68, y: L.bodyTop + 0.2, w: L.cw * 0.3, h: 1.8,
  });
  sourceNote(s, "Anthropic Claude Code 公式ドキュメント, 2025");
}

// ============================
// SLIDE 6: ポジション分析（2x2マトリクス）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "自律性と制御性の両軸で競合を上回る唯一のポジション");
  const px = L.mx + 0.8, py = L.bodyTop + 0.2, pw = L.cw - 1.6, ph = L.bodyH - 0.5;
  const hw = pw / 2, hh = ph / 2;
  const qc = [C.surfaceAlt, "E8F5E9", C.surface, "FFF3E0"];
  for (let q = 0; q < 4; q++) {
    s.addShape(pptx.shapes.RECTANGLE, {
      x: px + (q % 2) * hw, y: py + (q < 2 ? 0 : hh), w: hw, h: hh,
      fill: { color: qc[q] },
    });
  }
  const ql = ["安全だがタスク限定", "高自律・高制御（最適）", "低機能", "自律的だが制御困難"];
  const qp = [[px + 0.1, py + 0.05], [px + hw + 0.1, py + 0.05], [px + 0.1, py + hh + 0.05], [px + hw + 0.1, py + hh + 0.05]];
  ql.forEach((l, i) => {
    s.addText(l, {
      x: qp[i][0], y: qp[i][1], w: hw - 0.2, h: 0.2,
      fontSize: 8, fontFace: "Calibri", color: C.muted, italic: true,
    });
  });
  // 軸ラベル
  s.addText("\u2190 自律性（タスク完結能力）\u2192", {
    x: px, y: py + ph + 0.03, w: pw, h: 0.2,
    fontSize: 8, fontFace: "Calibri", color: C.text, align: "center",
  });
  // Y軸ラベル（制御性）
  s.addText("\u2190 制御性 \u2192", {
    x: px - 0.7, y: py + ph / 2 - 0.1, w: 0.6, h: 0.2,
    fontSize: 8, fontFace: "Calibri", color: C.text, align: "center",
    rotate: 270,
  });
  // ドット
  const dots = [
    { n: "Copilot $39", x: 0.3, y: 0.6 }, { n: "Cursor $20", x: 0.5, y: 0.5 },
    { n: "Amazon Q", x: 0.3, y: 0.7 }, { n: "Claude Code $200", x: 0.8, y: 0.85 },
    { n: "Devin $500", x: 0.9, y: 0.3 },
  ];
  dots.forEach((d) => {
    const dx = px + d.x * pw - 0.18;
    const dy = py + (1 - d.y) * ph - 0.18;
    const isCC = d.n.includes("Claude");
    const dotSize = isCC ? 0.4 : 0.32;
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: dx, y: dy, w: dotSize, h: dotSize,
      fill: { color: isCC ? C.accent : C.primary }, rectRadius: dotSize / 2,
      line: { color: "FFFFFF", width: 1.5 },
    });
    s.addText(d.n, {
      x: dx - 0.25, y: dy + dotSize + 0.02, w: dotSize + 0.5, h: 0.2,
      fontSize: 7, fontFace: "Calibri", bold: isCC, color: isCC ? C.accent : C.text, align: "center",
    });
  });
  sourceNote(s, "各社公式サイト・Gartner 2025");
}

// ============================
// SLIDE 7: 機能比較テーブル（コンサル品質 — 記号禁止）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "7機能軸で自律実行・権限制御・標準化の3点が決定的差別化要因");

  const headers = ["機能", "Claude Code", "Copilot", "Cursor", "Devin"];
  const colW = [1.7, 2.0, 1.7, 1.7, 1.7];

  // テーブルデータ（テキスト+色分け。◎○△×は使用しない）
  const rows = [
    ["コード補完",
      evalCell("標準的", "good"), evalCell("業界トップ", "best"), evalCell("高精度", "best"), evalCell("標準的", "good")],
    ["ファイル自律操作",
      evalCell("完全自律", "best"), evalCell("限定的", "limited"), evalCell("マルチファイル", "good"), evalCell("完全自律", "best")],
    ["Git自律操作",
      evalCell("commit/PR", "best"), evalCell("基本のみ", "limited"), evalCell("限定的", "limited"), evalCell("完全自律", "best")],
    ["テスト実行",
      evalCell("自動修正", "best"), evalCell("未対応", "none"), evalCell("限定的", "limited"), evalCell("完全自律", "best")],
    ["権限制御",
      evalCell("3層構造", "best"), evalCell("基本的", "good"), evalCell("限定的", "limited"), evalCell("ブラックボックス", "none")],
    ["CI/CD統合",
      evalCell("Headless", "best"), evalCell("Actions", "good"), evalCell("未対応", "none"), evalCell("API連携", "good")],
    ["標準化",
      evalCell("CLAUDE.md", "best"), evalCell("未対応", "none"), evalCell("未対応", "none"), evalCell("未対応", "none")],
  ];

  // ヘッダー行
  const tableRows = [];
  tableRows.push(headers.map((h, ci) => ({
    text: h, options: {
      fontSize: 9, fontFace: "Calibri", bold: true,
      color: C.textLight, fill: { color: C.primary },
      align: ci === 0 ? "left" : "center", valign: "middle",
      border: [{ type: "none" }, { type: "none" }, { type: "none" }, { type: "none" }],
    }
  })));

  // データ行
  rows.forEach((row, ri) => {
    const categoryCell = {
      text: row[0], options: {
        fontSize: 9, fontFace: "Calibri", bold: true,
        color: C.text,
        fill: { color: ri % 2 === 0 ? C.surface : "FFFFFF" },
        align: "left", valign: "middle",
        border: [
          { type: "none" }, { type: "none" },
          { type: "solid", pt: 0.3, color: C.border }, { type: "none" }
        ],
      }
    };
    const dataCells = row.slice(1).map((cell, ci) => {
      // Claude Code列（ci===0）にハイライト背景
      const bgColor = ci === 0 ? C.highlight : (ri % 2 === 0 ? C.surface : "FFFFFF");
      return {
        text: cell.text,
        options: { ...cell.options, fill: { color: bgColor } },
      };
    });
    tableRows.push([categoryCell, ...dataCells]);
  });

  const rowH = 0.42;
  const tableH = rowH * (rows.length + 1);
  const tableY = L.bodyTop + (L.bodyH - tableH) / 2;

  s.addTable(tableRows, {
    x: L.mx + 0.15, y: tableY, w: L.cw - 0.3, colW, rowH,
  });
  sourceNote(s, "各社公式ドキュメント, 2025年3月時点");
}

// ============================
// SLIDE 8: Intercom事例（タイムライン + Before/After）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "Intercom: 300名全員導入で10倍高速化、PR時間30%削減を3.5ヶ月で達成");

  // タイムライン（上半分）
  const lineY = L.bodyTop + 0.6;
  s.addShape(pptx.shapes.RECTANGLE, {
    x: L.mx, y: lineY, w: L.cw, h: 0.03, fill: { color: C.primary },
  });
  const phases = [
    { p: "Phase 1: チャンピオン試用", dur: "2週間", tasks: ["チャンピオン10名選定", "CLAUDE.md初版作成"], hl: false },
    { p: "Phase 2: チームリード展開", dur: "1ヶ月", tasks: ["リード50名に展開", "成功事例をSlack共有"], hl: false },
    { p: "Phase 3: 全社展開", dur: "2ヶ月", tasks: ["全300名に展開", ".claudeignore全社適用"], hl: true },
  ];
  const sw = L.cw / 3;
  phases.forEach((ph, i) => {
    const pcx = L.mx + i * sw + sw / 2;
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: pcx - 0.1, y: lineY - 0.1, w: 0.2, h: 0.2,
      fill: { color: ph.hl ? C.accent : C.primary }, rectRadius: 0.1,
    });
    s.addText(ph.p, {
      x: pcx - sw / 2 + 0.05, y: L.bodyTop, w: sw - 0.1, h: 0.48,
      fontSize: 9, fontFace: "Georgia", bold: true,
      color: ph.hl ? C.accent : C.primary, align: "center", wrap: true,
    });
    s.addText(ph.dur, {
      x: pcx - 0.4, y: lineY + 0.15, w: 0.8, h: 0.2,
      fontSize: 8, fontFace: "Calibri", bold: true, color: ph.hl ? C.accent : C.primary, align: "center",
    });
    ph.tasks.forEach((t, ti) => {
      s.addText(t, {
        x: pcx - sw / 2 + 0.1, y: lineY + 0.4 + ti * 0.22, w: sw - 0.2, h: 0.2,
        fontSize: 8, fontFace: "Calibri", color: C.text, wrap: true, bullet: true,
      });
    });
  });

  // Before/After パネル（下半分）
  const panY = L.bodyTop + 2.0;
  const panH = L.sourceY - panY - 0.1;
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: L.mx, y: panY, w: L.cw, h: panH,
    fill: { color: C.surfaceAlt }, rectRadius: 0.08,
    line: { color: C.primary, width: 0.75 },
  });
  s.addText("導入効果（Before \u2192 After）", {
    x: L.mx + 0.15, y: panY + 0.05, w: 5, h: 0.28,
    fontSize: 11, fontFace: "Georgia", bold: true, color: C.primary,
  });
  s.addText("10\u00D7", {
    x: L.mx + L.cw - 1.2, y: panY + 0.05, w: 1, h: 0.28,
    fontSize: 18, fontFace: "Georgia", bold: true, color: C.accent, align: "right",
  });
  const bfItems = [
    "開発速度: 1機能2週間 \u2192 1-2日（10倍高速化）",
    "PR対応: マージまで48h \u2192 33.6h（30%削減）",
    "満足度: レガシー作業32% \u2192 AI支援78%（+46pt）",
  ];
  bfItems.forEach((it, i) => {
    s.addText(it, {
      x: L.mx + 0.2, y: panY + 0.38 + i * 0.28, w: L.cw - 0.4, h: 0.26,
      fontSize: 9, fontFace: "Calibri", color: C.text, bullet: true,
    });
  });
  sourceNote(s, "Intercom Engineering Blog, 2025");
}

// ============================
// SLIDE 9: Shopify事例（ウォーターフォール + 構造化テキスト）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "Shopify: CEO主導でAI活用率を20%→92%に引き上げ、非エンジニアも参加");

  // ウォーターフォール（左50%）
  const wfX = L.mx, wfY = L.bodyTop, wfW = L.cw * 0.46, wfH = L.bodyH;
  const wfItems = [
    { label: "導入前", value: 20, type: "start" },
    { label: "CEO宣言", value: 25, type: "inc" },
    { label: "ツール教育", value: 22, type: "inc" },
    { label: "標準推奨", value: 25, type: "inc" },
    { label: "導入後", value: 92, type: "total" },
  ];
  const wfMax = 100;
  const wfN = wfItems.length;
  const wfBw = (wfW - 0.15 * (wfN + 1)) / wfN;
  const wfCh = wfH * 0.6;
  const wfCb = wfY + wfH * 0.8;
  let cum = 0;
  wfItems.forEach((it, i) => {
    const bx = wfX + 0.15 + i * (wfBw + 0.15);
    let barH, barY;
    const isT = it.type === "total" || it.type === "start";
    if (isT) {
      barH = (it.value / wfMax) * wfCh;
      barY = wfCb - barH;
      cum = it.value;
    } else {
      barH = (it.value / wfMax) * wfCh;
      barY = wfCb - ((cum + it.value) / wfMax) * wfCh;
      cum += it.value;
    }
    s.addShape(pptx.shapes.RECTANGLE, {
      x: bx, y: barY, w: wfBw, h: Math.max(barH, 0.02),
      fill: { color: isT ? C.primary : C.accent }, rectRadius: 0.02,
    });
    s.addText((isT ? "" : "+") + it.value + "%", {
      x: bx, y: barY - 0.2, w: wfBw, h: 0.18,
      fontSize: 8, fontFace: "Calibri", bold: true, color: isT ? C.primary : C.accent, align: "center",
    });
    s.addText(it.label, {
      x: bx - 0.03, y: wfCb + 0.03, w: wfBw + 0.06, h: 0.24,
      fontSize: 7, fontFace: "Calibri", color: C.text, align: "center", wrap: true,
    });
  });

  // 構造化テキスト（右50%）
  structuredItems(s, [
    { keyword: "CEOトップダウン宣言", detail: "『AI活用は昇進の前提条件』と全社方針を宣言。活用率が20%→45%へ即座に上昇" },
    { keyword: "非エンジニアへの展開", detail: "PM・デザイナーの30%がプロトタイプ作成やCSS修正に活用。作成期間を1/5に短縮" },
    { keyword: "用途別ツール使い分け", detail: "補完はCopilot、自律タスクはClaude Codeと使い分ける現実的アプローチ" },
  ], { x: L.mx + L.cw * 0.52, y: L.bodyTop + 0.15, w: L.cw * 0.46, h: L.bodyH });
  sourceNote(s, "Shopify公式発表・各種報道, 2025");
}

// ============================
// SLIDE 10: 用途別効果（棒グラフ）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "用途別の生産性向上は2-10倍 — レガシー移行が最もROIが高い");
  barChart(s, [
    { label: "日常コーディング", value: 2.5 },
    { label: "コードレビュー", value: 3.0 },
    { label: "テスト作成", value: 4.0 },
    { label: "大規模リファクタ", value: 6.0 },
    { label: "レガシー移行", value: 10.0 },
  ], {
    x: L.mx, y: L.bodyTop, w: L.cw, h: L.bodyH,
    highlight: "レガシー移行",
    insight: "タスク種別ごとの生産性向上倍率 — 複雑性・反復性が高いほど効果大",
  });
  sourceNote(s, "Intercom Blog / Anthropicレポート / 業界推計, 2025");
}

// ============================
// SLIDE 11: 3大リスク（3カラム）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "3大リスクの本質は「AI固有の問題」ではなく「既存課題の顕在化」であり管理可能");
  const colW = (L.cw - 0.3) / 3;
  const cols = [
    { color: C.primary, items: [
      { keyword: "セキュリティ", detail: "コードベースへのアクセス権限が必要。API鍵漏洩リスクあり" },
      { keyword: "対策", detail: "allowedTools + .claudeignore + 環境変数管理の3層で防御" },
    ]},
    { color: C.accent, items: [
      { keyword: "品質", detail: "AI生成コードの25-40%に脆弱性。ただし人間のコードも15-20%" },
      { keyword: "対策", detail: "SASTツール併用 + CLAUDE.md規約強制（遵守率95%以上）" },
    ]},
    { color: C.success, items: [
      { keyword: "コスト", detail: "API従量で月$300-500に達する場合あり。予算管理が課題" },
      { keyword: "対策", detail: "Max Plan $200/月定額 + 月次モニタリング。ROI 11倍で回収可能" },
    ]},
  ];
  cols.forEach((col, ci) => {
    const cx = L.mx + ci * (colW + 0.15);
    col.items.forEach((it, ii) => {
      const iy = L.bodyTop + ii * 1.9;
      s.addShape(pptx.shapes.RECTANGLE, {
        x: cx, y: iy + 0.03, w: 0.04, h: 1.7,
        fill: { color: col.color },
      });
      s.addText(it.keyword, {
        x: cx + 0.14, y: iy, w: colW - 0.2, h: 0.28,
        fontSize: 11, fontFace: "Georgia", bold: true, color: col.color,
      });
      s.addText(it.detail, {
        x: cx + 0.14, y: iy + 0.3, w: colW - 0.2, h: 1.4,
        fontSize: 9, fontFace: "Calibri", color: C.text, wrap: true,
      });
    });
  });
  sourceNote(s, "Stanford研究 2024 / GitHub Survey 2025 / Anthropic 2025");
}

// ============================
// SLIDE 12: 導入リスク vs 未導入リスク
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "導入リスクより未導入リスクが大きい — 最大のリスクは何もしないこと");
  structuredItems(s, [
    { keyword: "セキュリティの過大評価を正す", detail: "既存コードにも脆弱性15-20%。AI導入をきっかけにSASTツール導入で全体品質が向上する" },
    { keyword: "品質リスクの過大評価を正す", detail: "CLAUDE.md規約強制で遵守率95%以上。Intercom社ではレビュー指摘40%減を実現" },
    { keyword: "コストの過大評価を正す", detail: "年収2,000万円エンジニアの20%向上（400万円相当）に対し年間コスト36万円。ROI 11倍" },
    { keyword: "未導入リスクの過小評価を正す", detail: "76%がAI使用する市場で非導入は採用力低下・開発速度2-5倍差・AI活用ギャップの3重損失" },
  ], { x: L.mx, y: L.bodyTop, w: L.cw, h: L.bodyH * 0.72 });

  // ボトムノート
  const ny = L.sourceY - 0.55;
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: L.mx, y: ny, w: L.cw, h: 0.45,
    fill: { color: C.primary }, rectRadius: 0.06,
  });
  s.addText("10年前のクラウド移行判断と同じ構図。リスクを管理しながら導入する", {
    x: L.mx + 0.15, y: ny + 0.03, w: L.cw - 0.3, h: 0.4,
    fontSize: 11, fontFace: "Georgia", bold: true, color: C.textLight, valign: "middle",
  });
  sourceNote(s, "Stanford研究 2024 / GitHub Survey 2025 / 業界推計 2025");
}

// ============================
// SLIDE 13: 3段階導入ロードマップ（タイムライン）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "個人→チーム→CI/CD統合の3段階で成功率80%、月9万円から開始可能");
  const lineY = L.bodyTop + 0.6;
  s.addShape(pptx.shapes.RECTANGLE, {
    x: L.mx, y: lineY, w: L.cw, h: 0.03, fill: { color: C.primary },
  });
  const phases = [
    { p: "Phase 1: 個人利用（月$600〜）", dur: "2-4週間", tasks: ["チャンピオン3-5名選定", "Max Plan契約・CLAUDE.md初版", "セキュリティポリシー策定"], hl: false },
    { p: "Phase 2: チーム展開（月$1-2K）", dur: "1-2ヶ月", tasks: ["1チーム5-10名に展開", "CLAUDE.md Level 2-3に成熟", "PR処理速度30%短縮目標"], hl: false },
    { p: "Phase 3: CI/CD統合（年$120-240K）", dur: "3-6ヶ月", tasks: ["Headlessモードで自動PR", "全チーム展開・活用率80%目標", "定型タスク60-70%自動化"], hl: true },
  ];
  const sw = L.cw / 3;
  phases.forEach((ph, i) => {
    const pcx = L.mx + i * sw + sw / 2;
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: pcx - 0.1, y: lineY - 0.1, w: 0.2, h: 0.2,
      fill: { color: ph.hl ? C.accent : C.primary }, rectRadius: 0.1,
    });
    s.addText(ph.p, {
      x: pcx - sw / 2 + 0.05, y: L.bodyTop, w: sw - 0.1, h: 0.48,
      fontSize: 9, fontFace: "Georgia", bold: true,
      color: ph.hl ? C.accent : C.primary, align: "center", wrap: true,
    });
    s.addText(ph.dur, {
      x: pcx - 0.45, y: lineY + 0.15, w: 0.9, h: 0.2,
      fontSize: 8, fontFace: "Calibri", bold: true, color: ph.hl ? C.accent : C.primary, align: "center",
    });
    ph.tasks.forEach((t, ti) => {
      s.addText(t, {
        x: pcx - sw / 2 + 0.12, y: lineY + 0.4 + ti * 0.24, w: sw - 0.24, h: 0.22,
        fontSize: 8, fontFace: "Calibri", color: C.text, wrap: true, bullet: true,
      });
    });
  });
  sourceNote(s, "業界推計 / Intercom・Shopify・GitLab事例, 2025");
}

// ============================
// SLIDE 14: 成功要因（2x2グリッド）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "成功企業に共通する4要因 — 技術選定より組織的準備が導入成否を決める");
  const cellW = (L.cw - 0.2) / 2;
  const cellH = (L.bodyH - 0.2) / 2;
  const grid = [
    { x: L.mx, y: L.bodyTop, kw: "経営コミットメント", detail: "CTO/VPoE主導の予算承認とKPI設定。Shopify CEO宣言で活用率が25pt上昇", col: C.primary },
    { x: L.mx + cellW + 0.2, y: L.bodyTop, kw: "チャンピオン選定", detail: "技術力と社内影響力を持つ先行ユーザー3-5名。成功体験の可視化で自然拡散を促進", col: C.accent },
    { x: L.mx, y: L.bodyTop + cellH + 0.2, kw: "CLAUDE.md整備", detail: "導入初日に着手すべき最優先施策。導入チームは未導入比+40%の生産性向上を実現", col: C.accent },
    { x: L.mx + cellW + 0.2, y: L.bodyTop + cellH + 0.2, kw: "セキュリティ先行整備", detail: ".claudeignoreポリシー事前策定が必須。Intercom社は導入後インシデントゼロを達成", col: C.primary },
  ];
  grid.forEach((g) => {
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: g.x, y: g.y, w: cellW, h: cellH,
      fill: { color: C.surfaceAlt }, rectRadius: 0.08,
      line: { color: C.border, width: 0.5 },
      shadow: makeShadow(),
    });
    s.addShape(pptx.shapes.RECTANGLE, {
      x: g.x + 0.1, y: g.y + 0.12, w: 0.04, h: cellH - 0.24,
      fill: { color: g.col },
    });
    s.addText(g.kw, {
      x: g.x + 0.22, y: g.y + 0.12, w: cellW - 0.35, h: 0.3,
      fontSize: 11, fontFace: "Georgia", bold: true, color: C.primary,
    });
    s.addText(g.detail, {
      x: g.x + 0.22, y: g.y + 0.45, w: cellW - 0.35, h: cellH - 0.6,
      fontSize: 9, fontFace: "Calibri", color: C.text, wrap: true,
    });
  });
  sourceNote(s, "Intercom Blog / Shopify公式 / 匿名A社事例, 2025");
}

// ============================
// SLIDE 15: まとめ & Next Steps
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: C.primaryDark };
  // タイトル（アクセントラインなし）
  s.addText("まとめと Next Steps", {
    x: L.mx, y: 0.3, w: L.cw, h: 0.5,
    fontSize: 22, fontFace: "Georgia", bold: true, color: C.textLight,
  });

  s.addText("Key Takeaways", {
    x: L.mx, y: 0.95, w: 4, h: 0.28,
    fontSize: 12, fontFace: "Georgia", bold: true, color: C.accent,
  });
  const takeaways = [
    "Claude Codeはコード補完ではなく自律型エージェント。200Kトークンで開発タスク全体を完遂する新カテゴリ",
    "Intercom 10倍高速化、Shopify 92%浸透を実証。ROI回収は3-6ヶ月でSaaS平均の1/3",
    "3段階導入で成功率80%。セキュリティ・品質・コストの3大リスクは全て管理可能",
  ];
  takeaways.forEach((t, i) => {
    const ty = 1.35 + i * 0.48;
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: L.mx + 0.05, y: ty + 0.03, w: 0.24, h: 0.24,
      fill: { color: C.accent }, rectRadius: 0.04,
    });
    s.addText(String(i + 1), {
      x: L.mx + 0.05, y: ty + 0.03, w: 0.24, h: 0.24,
      fontSize: 10, fontFace: "Calibri", bold: true, color: C.textLight, align: "center", valign: "middle",
    });
    s.addText(t, {
      x: L.mx + 0.4, y: ty, w: L.cw - 0.6, h: 0.4,
      fontSize: 9, fontFace: "Calibri", color: "CCDDEE", valign: "middle", wrap: true,
    });
  });

  s.addText("Next Steps", {
    x: L.mx, y: 2.95, w: 4, h: 0.28,
    fontSize: 12, fontFace: "Georgia", bold: true, color: C.accent,
  });
  const steps = [
    "今週中: セキュリティポリシー初期検討とチャンピオン候補3-5名リストアップ",
    "2週間以内: CLAUDE.md初版作成とMax Plan契約でPoC環境セットアップ",
    "1ヶ月後: チャンピオンPoC開始、速度向上率のベースラインデータ収集",
    "四半期末: 定量効果レポート、経営会議でPhase 2移行判断",
  ];
  steps.forEach((t, i) => {
    const ty = 3.35 + i * 0.42;
    s.addText("\u2192", {
      x: L.mx + 0.05, y: ty, w: 0.28, h: 0.32,
      fontSize: 13, color: C.accent, align: "center", valign: "middle",
    });
    s.addText(t, {
      x: L.mx + 0.38, y: ty, w: L.cw - 0.55, h: 0.32,
      fontSize: 9, fontFace: "Calibri", color: "CCDDEE", valign: "middle", wrap: true,
    });
  });

  sourceDark(s, "本資料全体のまとめ");
}

// ============================
// 出力
// ============================
const now = new Date();
const ts = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, "0")}${String(now.getDate()).padStart(2, "0")}_${String(now.getHours()).padStart(2, "0")}${String(now.getMinutes()).padStart(2, "0")}`;
const outPath = `output/pptx/Claude_Code_v2_${ts}.pptx`;

pptx.writeFile({ fileName: outPath }).then(() => {
  console.log("生成完了: " + outPath);
  console.log("スライド数: " + (page - 1));
}).catch(err => console.error("エラー:", err));
