const PptxGenJS = require("pptxgenjs");
const fs = require("fs");

// ============================
// デザインシステム
// ============================
const C = {
  primary: "2E5090",
  primaryDark: "1E3A6E",
  accent: "E67E22",
  text: "333333",
  textLight: "FFFFFF",
  surface: "F5F7FA",
  surfaceAlt: "EBF0F7",
  border: "E0E0E0",
  success: "27AE60",
  muted: "8899AA",
  green: "E8F5E9",
  orange: "FFF3E0",
};

const L = {
  mx: 0.7,       // 左右マージン
  titleY: 0.35,
  bodyTop: 1.35,
  bodyBot: 6.85,
  footerY: 7.1,
  W: 13.333,
  H: 7.5,
};
L.bodyH = L.bodyBot - L.bodyTop;
L.cw = L.W - L.mx * 2;  // コンテンツ幅

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "vCompany";
let page = 1;

// ============================
// ヘルパー
// ============================
function header(s, title) {
  s.addText(title, {
    x: L.mx, y: L.titleY, w: L.cw, h: 0.8,
    fontSize: 17, fontFace: "Georgia", bold: true,
    color: C.primary, valign: "top", wrap: true,
  });
}

function footer(s, src, opts = {}) {
  const c = opts.dark ? "7799BB" : C.muted;
  if (src) {
    s.addText("Source: " + src, {
      x: L.mx, y: L.footerY, w: 9, h: 0.25,
      fontSize: 8, fontFace: "Calibri", color: c,
    });
  }
  s.addText(String(page++), {
    x: 12.2, y: L.footerY, w: 0.8, h: 0.25,
    fontSize: 8, fontFace: "Calibri", color: c, align: "right",
  });
}

function barChart(s, items, o) {
  const x0 = o.x, y0 = o.y, w = o.w, h = o.h;
  const max = Math.max(...items.map(i => i.value));
  const n = items.length;
  const gap = 0.12;
  const bw = Math.min((w - gap * (n + 1)) / n, 1.1);
  const totalW = n * bw + (n + 1) * gap;
  const sx = x0 + (w - totalW) / 2 + gap;
  const ch = h * 0.68;
  const cb = y0 + h * 0.82;

  for (let i = 0; i <= 3; i++) {
    s.addShape(pptx.shapes.RECTANGLE, {
      x: x0, y: cb - (ch * i) / 3, w, h: 0.008, fill: { color: C.border },
    });
  }

  items.forEach((it, i) => {
    const bh = max > 0 ? (it.value / max) * ch : 0;
    const bx = sx + i * (bw + gap);
    const by = cb - bh;
    const hl = o.highlight === it.label;
    const col = hl ? C.accent : C.primary;

    s.addShape(pptx.shapes.RECTANGLE, {
      x: bx, y: by, w: bw, h: bh, fill: { color: col }, rectRadius: 0.04,
    });
    s.addText(String(it.value), {
      x: bx, y: by - 0.28, w: bw, h: 0.26,
      fontSize: 10, fontFace: "Calibri", bold: true, color: col, align: "center",
    });
    s.addText(it.label, {
      x: bx, y: cb + 0.04, w: bw, h: 0.32,
      fontSize: 7.5, fontFace: "Calibri", color: C.text, align: "center", wrap: true,
    });
  });

  if (o.insight) {
    s.addText(o.insight, {
      x: x0, y: y0 - 0.02, w, h: 0.25,
      fontSize: 9, fontFace: "Calibri", color: C.muted,
    });
  }
}

function kpiCard(s, val, label, o) {
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: o.x, y: o.y, w: o.w, h: o.h,
    fill: { color: C.surfaceAlt }, rectRadius: 0.12,
    line: { color: C.border, width: 0.75 },
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: o.x + 0.15, y: o.y + 0.2, w: 0.05, h: o.h - 0.4,
    fill: { color: C.accent },
  });
  s.addText(val, {
    x: o.x + 0.35, y: o.y + 0.25, w: o.w - 0.5, h: 1,
    fontSize: 34, fontFace: "Georgia", bold: true, color: C.primary,
  });
  s.addText(label, {
    x: o.x + 0.35, y: o.y + 1.3, w: o.w - 0.5, h: 0.8,
    fontSize: 10, fontFace: "Calibri", color: C.text, wrap: true,
  });
}

function structuredItems(s, items, o) {
  const itemH = Math.min(o.h / items.length, 1.25);
  items.forEach((it, i) => {
    const iy = o.y + i * itemH;
    const col = i % 2 === 0 ? C.primary : C.accent;
    s.addShape(pptx.shapes.RECTANGLE, {
      x: o.x, y: iy + 0.04, w: 0.05, h: itemH - 0.12, fill: { color: col },
    });
    s.addText(it.keyword, {
      x: o.x + 0.18, y: iy, w: o.w - 0.25, h: 0.32,
      fontSize: 12, fontFace: "Georgia", bold: true, color: C.primary,
    });
    const d = it.detail.length > 85 ? it.detail.substring(0, 82) + "..." : it.detail;
    s.addText(d, {
      x: o.x + 0.18, y: iy + 0.32, w: o.w - 0.25, h: itemH - 0.38,
      fontSize: 10, fontFace: "Calibri", color: C.text, wrap: true,
    });
  });
}

// ============================
// SLIDE 1: タイトル
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: C.primaryDark };
  s.addShape(pptx.shapes.OVAL, {
    x: 9.5, y: 4.2, w: 5.5, h: 5.5, fill: { color: C.primary, transparency: 85 },
  });
  s.addShape(pptx.shapes.OVAL, {
    x: 10.8, y: 2.5, w: 3.5, h: 3.5, fill: { color: C.accent, transparency: 90 },
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: L.mx, y: 3.4, w: 2.5, h: 0.05, fill: { color: C.accent },
  });
  s.addText("Claude Code とは", {
    x: L.mx, y: 1.4, w: 9, h: 0.8,
    fontSize: 38, fontFace: "Georgia", bold: true, color: C.textLight,
  });
  s.addText("AIコーディングアシスタントの全貌と導入戦略", {
    x: L.mx, y: 2.2, w: 9, h: 0.7,
    fontSize: 22, fontFace: "Georgia", color: "AABBCC",
  });
  s.addText("自律型開発エージェントによる開発生産性革命と段階的導入ロードマップ", {
    x: L.mx, y: 3.7, w: 9, h: 0.5,
    fontSize: 14, fontFace: "Calibri", color: "8899AA", wrap: true,
  });
  s.addText("2026-03-13", {
    x: L.mx, y: 5.5, w: 3, h: 0.3,
    fontSize: 11, fontFace: "Calibri", color: "7799BB",
  });
  footer(s, null, { dark: true });
}

// ============================
// SLIDE 2: 市場規模
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
  ], { x: L.mx, y: L.bodyTop, w: L.cw * 0.58, h: L.bodyH, highlight: "2030(予)", insight: "AIコーディングツール市場規模（億ドル）" });
  kpiCard(s, "CAGR 25%+", "年平均成長率\nSaaS平均15%の1.7倍", {
    x: L.mx + L.cw * 0.62, y: L.bodyTop + 0.5, w: L.cw * 0.36, h: 2.5,
  });
  footer(s, "Gartner AI Coding Assistant Market Report, 2025");
}

// ============================
// SLIDE 3: 普及率
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
  footer(s, "Stack Overflow Developer Survey 2025 / McKinsey Digital 2025");
}

// ============================
// SLIDE 4: パラダイム転換（フロー）
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
  const bw = (L.cw - 0.4 * 3) / 4;
  steps.forEach((st, i) => {
    const bx = L.mx + i * (bw + 0.4);
    const isHL = i === 2;
    s.addShape(pptx.shapes.OVAL, {
      x: bx + bw / 2 - 0.2, y: L.bodyTop, w: 0.4, h: 0.4,
      fill: { color: isHL ? C.accent : C.primary },
    });
    s.addText(st.num, {
      x: bx + bw / 2 - 0.2, y: L.bodyTop, w: 0.4, h: 0.4,
      fontSize: 14, fontFace: "Calibri", bold: true, color: C.textLight, align: "center", valign: "middle",
    });
    s.addText(st.title, {
      x: bx, y: L.bodyTop + 0.5, w: bw, h: 0.45,
      fontSize: 12, fontFace: "Georgia", bold: true, color: isHL ? C.accent : C.primary, align: "center", wrap: true,
    });
    s.addText(st.sub, {
      x: bx, y: L.bodyTop + 0.95, w: bw, h: 0.3,
      fontSize: 9, fontFace: "Calibri", color: C.muted, align: "center", wrap: true,
    });
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: bx, y: L.bodyTop + 1.4, w: bw, h: 1.8,
      fill: { color: isHL ? "FFF7ED" : C.surfaceAlt }, rectRadius: 0.08,
      line: { color: isHL ? C.accent : C.border, width: isHL ? 1.5 : 0.5 },
    });
    s.addText(st.detail, {
      x: bx + 0.1, y: L.bodyTop + 1.5, w: bw - 0.2, h: 1.6,
      fontSize: 10, fontFace: "Calibri", color: C.text, wrap: true, valign: "top",
    });
    if (i < 3) {
      s.addText("\u2192", {
        x: bx + bw, y: L.bodyTop + 0.5, w: 0.4, h: 0.45,
        fontSize: 18, color: C.accent, align: "center", valign: "middle",
      });
    }
  });
  footer(s, "Gartner 2025 / Anthropic / SWE-bench 2025");
}

// ============================
// SLIDE 5: 基本設計（サイクル + KPI）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "Claude Codeは開発ライフサイクル全体を自律実行するCLIエージェント");
  const cx = L.mx + 3.5, cy = L.bodyTop + L.bodyH * 0.48;
  const items = [
    { t: "コード理解", d: "200Kトークンで全体読解" },
    { t: "設計・推論", d: "Extended Thinking" },
    { t: "実装", d: "マルチファイル横断編集" },
    { t: "テスト", d: "自動実行・自動修正" },
    { t: "Git操作", d: "commit/PR/レビュー" },
  ];
  // 中央円
  s.addShape(pptx.shapes.OVAL, {
    x: cx - 0.65, y: cy - 0.5, w: 1.3, h: 1.0,
    fill: { color: C.primary },
  });
  s.addText("自律型\nエージェント", {
    x: cx - 0.65, y: cy - 0.5, w: 1.3, h: 1.0,
    fontSize: 11, fontFace: "Georgia", bold: true, color: C.textLight, align: "center", valign: "middle", wrap: true,
  });
  items.forEach((it, i) => {
    const angle = (2 * Math.PI * i) / 5 - Math.PI / 2;
    const rx = 2.8, ry = 2.0;
    const nx = cx + rx * Math.cos(angle);
    const ny = cy + ry * Math.sin(angle);
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: nx - 0.95, y: ny - 0.45, w: 1.9, h: 0.9,
      fill: { color: C.surfaceAlt }, rectRadius: 0.08,
      line: { color: C.primary, width: 1 },
    });
    s.addText(it.t, {
      x: nx - 0.9, y: ny - 0.4, w: 1.8, h: 0.35,
      fontSize: 11, fontFace: "Georgia", bold: true, color: C.primary, align: "center",
    });
    s.addText(it.d, {
      x: nx - 0.9, y: ny - 0.02, w: 1.8, h: 0.4,
      fontSize: 9, fontFace: "Calibri", color: C.text, align: "center", wrap: true,
    });
  });
  // KPIカード右
  kpiCard(s, "200K", "コンテキスト(tokens)\nCopilotの25倍", {
    x: L.mx + L.cw * 0.66, y: L.bodyTop + 0.3, w: L.cw * 0.32, h: 2.2,
  });
  footer(s, "Anthropic Claude Code 公式ドキュメント, 2025");
}

// ============================
// SLIDE 6: ポジション分析（マトリクス）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "自律性と制御性の両軸で競合を上回る唯一のポジション");
  const px = L.mx + 1.2, py = L.bodyTop + 0.3, pw = L.cw - 2.4, ph = L.bodyH - 0.8;
  const hw = pw / 2, hh = ph / 2;
  const qc = [C.surfaceAlt, C.green, C.surface, C.orange];
  for (let q = 0; q < 4; q++) {
    s.addShape(pptx.shapes.RECTANGLE, {
      x: px + (q % 2) * hw, y: py + (q < 2 ? 0 : hh), w: hw, h: hh,
      fill: { color: qc[q] },
    });
  }
  const ql = ["安全だがタスク限定", "高自律・高制御（最適）", "低機能", "自律的だが制御困難"];
  const qp = [[px + 0.15, py + 0.1], [px + hw + 0.15, py + 0.1], [px + 0.15, py + hh + 0.1], [px + hw + 0.15, py + hh + 0.1]];
  ql.forEach((l, i) => {
    s.addText(l, {
      x: qp[i][0], y: qp[i][1], w: hw - 0.3, h: 0.25,
      fontSize: 9, fontFace: "Calibri", color: C.muted, italic: true,
    });
  });
  s.addText("\u2190 自律性（タスク完結能力）\u2192", {
    x: px, y: py + ph + 0.05, w: pw, h: 0.25,
    fontSize: 9, fontFace: "Calibri", color: C.text, align: "center",
  });
  const dots = [
    { n: "Copilot $39", x: 0.3, y: 0.6 }, { n: "Cursor $20", x: 0.5, y: 0.5 },
    { n: "Amazon Q", x: 0.3, y: 0.7 }, { n: "Claude Code $200", x: 0.8, y: 0.85 },
    { n: "Devin $500", x: 0.9, y: 0.3 },
  ];
  dots.forEach((d) => {
    const dx = px + d.x * pw - 0.25;
    const dy = py + (1 - d.y) * ph - 0.25;
    const isCC = d.n.includes("Claude");
    s.addShape(pptx.shapes.OVAL, {
      x: dx, y: dy, w: 0.5, h: 0.5,
      fill: { color: isCC ? C.accent : C.primary },
      line: { color: "FFFFFF", width: 2 },
    });
    s.addText(d.n, {
      x: dx - 0.35, y: dy + 0.52, w: 1.2, h: 0.25,
      fontSize: 8, fontFace: "Calibri", bold: isCC, color: isCC ? C.accent : C.text, align: "center",
    });
  });
  footer(s, "各社公式サイト・Gartner 2025");
}

// ============================
// SLIDE 7: 機能比較テーブル（コンサル品質）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "7機能軸で自律実行・権限制御・標準化の3点が決定的差別化要因");
  const headers = ["機能", "Claude Code", "Copilot", "Cursor", "Devin"];
  const rows = [
    ["コード補完", "\u25CB 標準的", "\u25CE 業界最高", "\u25CE 高精度", "\u25CB 標準的"],
    ["ファイル自律操作", "\u25CE 完全自律", "\u25B3 限定的", "\u25CB マルチファイル", "\u25CE 完全自律"],
    ["Git自律操作", "\u25CE commit/PR", "\u25B3 基本のみ", "\u25B3 限定的", "\u25CE 完全自律"],
    ["テスト実行", "\u25CE 自動修正", "\u00D7 未対応", "\u25B3 限定的", "\u25CE 完全自律"],
    ["権限制御", "\u25CE 3層構造", "\u25CB 基本的", "\u25B3 限定的", "\u00D7 ブラックボックス"],
    ["CI/CD統合", "\u25CE Headless", "\u25CB Actions", "\u00D7 未対応", "\u25CB API連携"],
    ["標準化", "\u25CE CLAUDE.md", "\u00D7 なし", "\u00D7 なし", "\u00D7 なし"],
  ];
  const colW = [2.2, 2.5, 2.2, 2.2, 2.2];
  const tableRows = [];
  tableRows.push(headers.map((h, ci) => ({
    text: h, options: {
      fontSize: 10, fontFace: "Calibri", bold: true,
      color: C.textLight, fill: { color: C.primary },
      align: ci === 0 ? "left" : "center", valign: "middle",
      border: [{ type: "none" }, { type: "none" }, { type: "none" }, { type: "none" }],
    }
  })));
  rows.forEach((row, ri) => {
    tableRows.push(row.map((cell, ci) => ({
      text: cell, options: {
        fontSize: 9, fontFace: "Calibri",
        color: C.text,
        fill: { color: ci === 1 ? "F0F4FF" : (ri % 2 === 0 ? C.surface : "FFFFFF") },
        align: ci === 0 ? "left" : "center", valign: "middle",
        border: [{ type: "none" }, { type: "none" },
          { type: "solid", pt: 0.3, color: C.border }, { type: "none" }],
      }
    })));
  });
  s.addTable(tableRows, {
    x: L.mx + 0.2, y: L.bodyTop + 0.1, w: 11.3, colW, rowH: 0.42,
  });
  footer(s, "各社公式ドキュメント, 2025年3月時点");
}

// ============================
// SLIDE 8: Intercom事例（タイムライン + Before/After）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "Intercom: 300名全員導入で10倍高速化、PR時間30%削減を3.5ヶ月で達成");
  // タイムライン
  const tly = L.bodyTop, tlh = L.bodyH * 0.5;
  const lineY = tly + 0.8;
  s.addShape(pptx.shapes.RECTANGLE, {
    x: L.mx, y: lineY, w: L.cw, h: 0.04, fill: { color: C.primary },
  });
  const phases = [
    { p: "Phase 1: チャンピオン試用", dur: "2週間", tasks: ["チャンピオン10名選定", "CLAUDE.md初版作成"], hl: false },
    { p: "Phase 2: チームリード展開", dur: "1ヶ月", tasks: ["リード50名に展開", "成功事例をSlack共有"], hl: false },
    { p: "Phase 3: 全社展開", dur: "2ヶ月", tasks: ["全300名に展開", ".claudeignore全社適用"], hl: true },
  ];
  const sw = L.cw / 3;
  phases.forEach((ph, i) => {
    const pcx = L.mx + i * sw + sw / 2;
    s.addShape(pptx.shapes.OVAL, {
      x: pcx - 0.15, y: lineY - 0.13, w: 0.3, h: 0.3,
      fill: { color: ph.hl ? C.accent : C.primary },
    });
    s.addText(ph.p, {
      x: pcx - sw / 2 + 0.05, y: tly, w: sw - 0.1, h: 0.6,
      fontSize: 10, fontFace: "Georgia", bold: true,
      color: ph.hl ? C.accent : C.primary, align: "center", wrap: true,
    });
    s.addText(ph.dur, {
      x: pcx - 0.5, y: lineY + 0.2, w: 1, h: 0.25,
      fontSize: 9, fontFace: "Calibri", bold: true, color: ph.hl ? C.accent : C.primary, align: "center",
    });
    ph.tasks.forEach((t, ti) => {
      s.addText("\u2022 " + t, {
        x: pcx - sw / 2 + 0.1, y: lineY + 0.5 + ti * 0.28, w: sw - 0.2, h: 0.26,
        fontSize: 9, fontFace: "Calibri", color: C.text, wrap: true,
      });
    });
  });
  // Before/After パネル
  const panY = L.bodyTop + tlh + 0.15;
  const panH = L.bodyH - tlh - 0.2;
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: L.mx, y: panY, w: L.cw, h: panH,
    fill: { color: C.surfaceAlt }, rectRadius: 0.1, line: { color: C.primary, width: 1 },
  });
  s.addText("導入効果（Before \u2192 After）", {
    x: L.mx + 0.2, y: panY + 0.05, w: 6, h: 0.35,
    fontSize: 12, fontFace: "Georgia", bold: true, color: C.primary,
  });
  s.addText("10\u00D7", {
    x: L.mx + L.cw - 1.5, y: panY + 0.05, w: 1.3, h: 0.35,
    fontSize: 22, fontFace: "Georgia", bold: true, color: C.accent, align: "right",
  });
  const bfItems = [
    "開発速度: 1機能2週間 \u2192 1-2日（10倍高速化）",
    "PR対応: マージまで48h \u2192 33.6h（30%削減）",
    "満足度: レガシー作業32% \u2192 AI支援78%（+46pt）",
  ];
  bfItems.forEach((it, i) => {
    s.addText("\u2022 " + it, {
      x: L.mx + 0.3, y: panY + 0.45 + i * 0.35, w: L.cw - 0.6, h: 0.33,
      fontSize: 10, fontFace: "Calibri", color: C.text,
    });
  });
  footer(s, "Intercom Engineering Blog, 2025");
}

// ============================
// SLIDE 9: Shopify事例
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "Shopify: CEO主導でAI活用率を20%→92%に引き上げ、非エンジニアも参加");
  // ウォーターフォール（左）
  const wfItems = [
    { label: "導入前", value: 20, type: "start" },
    { label: "CEO宣言", value: 25, type: "inc" },
    { label: "ツール教育", value: 22, type: "inc" },
    { label: "標準推奨", value: 25, type: "inc" },
    { label: "導入後", value: 92, type: "total" },
  ];
  const wfX = L.mx, wfY = L.bodyTop, wfW = L.cw * 0.46, wfH = L.bodyH;
  const wfMax = 100;
  const wfN = wfItems.length;
  const wfBw = (wfW - 0.2 * (wfN + 1)) / wfN;
  const wfCh = wfH * 0.6;
  const wfCb = wfY + wfH * 0.8;
  let cum = 0;
  wfItems.forEach((it, i) => {
    const bx = wfX + 0.2 + i * (wfBw + 0.2);
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
      x: bx, y: barY, w: wfBw, h: Math.max(barH, 0.03),
      fill: { color: isT ? C.primary : C.accent }, rectRadius: 0.03,
    });
    s.addText((isT ? "" : "+") + it.value + "%", {
      x: bx, y: barY - 0.25, w: wfBw, h: 0.23,
      fontSize: 9, fontFace: "Calibri", bold: true, color: isT ? C.primary : C.accent, align: "center",
    });
    s.addText(it.label, {
      x: bx - 0.05, y: wfCb + 0.04, w: wfBw + 0.1, h: 0.3,
      fontSize: 8, fontFace: "Calibri", color: C.text, align: "center", wrap: true,
    });
  });
  // 右: 構造化テキスト
  structuredItems(s, [
    { keyword: "CEOトップダウン宣言", detail: "『AI活用は昇進の前提条件』と全社方針を宣言。活用率が20%→45%へ即座に上昇" },
    { keyword: "非エンジニアへの展開", detail: "PM・デザイナーの30%がプロトタイプ作成やCSS修正に活用。作成期間を1/5に短縮" },
    { keyword: "用途別ツール使い分け", detail: "補完はCopilot、自律タスクはClaude Codeと使い分ける現実的アプローチ" },
  ], { x: L.mx + L.cw * 0.52, y: L.bodyTop + 0.2, w: L.cw * 0.46, h: L.bodyH });
  footer(s, "Shopify公式発表・各種報道, 2025");
}

// ============================
// SLIDE 10: 効果サマリー
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
  ], { x: L.mx, y: L.bodyTop, w: L.cw, h: L.bodyH, highlight: "レガシー移行", insight: "タスク種別ごとの生産性向上倍率 — 複雑性・反復性が高いほど効果大" });
  footer(s, "Intercom Blog / Anthropicレポート / 業界推計, 2025");
}

// ============================
// SLIDE 11: 3大リスク
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "3大リスクの本質は「AI固有の問題」ではなく「既存課題の顕在化」であり管理可能");
  const colW2 = (L.cw - 0.4) / 3;
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
    const cx = L.mx + ci * (colW2 + 0.2);
    col.items.forEach((it, ii) => {
      const iy = L.bodyTop + ii * 2.4;
      s.addShape(pptx.shapes.RECTANGLE, {
        x: cx, y: iy + 0.04, w: 0.05, h: 2.1, fill: { color: col.color },
      });
      s.addText(it.keyword, {
        x: cx + 0.18, y: iy, w: colW2 - 0.25, h: 0.35,
        fontSize: 13, fontFace: "Georgia", bold: true, color: col.color,
      });
      s.addText(it.detail, {
        x: cx + 0.18, y: iy + 0.38, w: colW2 - 0.25, h: 1.7,
        fontSize: 10, fontFace: "Calibri", color: C.text, wrap: true,
      });
    });
  });
  footer(s, "Stanford研究 2024 / GitHub Survey 2025 / Anthropic 2025");
}

// ============================
// SLIDE 12: リスク管理方針
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
  ], { x: L.mx, y: L.bodyTop, w: L.cw, h: L.bodyH * 0.78 });
  // ボトムノート
  const ny = L.bodyBot - 0.7;
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: L.mx, y: ny, w: L.cw, h: 0.55,
    fill: { color: C.primary }, rectRadius: 0.08,
  });
  s.addText("10年前のクラウド移行判断と同じ構図。リスクを管理しながら導入する", {
    x: L.mx + 0.2, y: ny + 0.05, w: L.cw - 0.4, h: 0.45,
    fontSize: 12, fontFace: "Georgia", bold: true, color: C.textLight, valign: "middle",
  });
  footer(s, "Stanford研究 2024 / GitHub Survey 2025 / 業界推計 2025");
}

// ============================
// SLIDE 13: 3段階戦略（タイムライン）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "個人→チーム→CI/CD統合の3段階で成功率80%、月9万円から開始可能");
  const tly = L.bodyTop, lineY2 = tly + 0.8;
  s.addShape(pptx.shapes.RECTANGLE, {
    x: L.mx, y: lineY2, w: L.cw, h: 0.04, fill: { color: C.primary },
  });
  const phases2 = [
    { p: "Phase 1: 個人利用（月$600〜）", dur: "2-4週間", tasks: ["チャンピオン3-5名選定", "Max Plan契約・CLAUDE.md初版", "セキュリティポリシー策定"], hl: false },
    { p: "Phase 2: チーム展開（月$1-2K）", dur: "1-2ヶ月", tasks: ["1チーム5-10名に展開", "CLAUDE.md Level 2-3に成熟", "PR処理速度30%短縮目標"], hl: false },
    { p: "Phase 3: CI/CD統合（年$120-240K）", dur: "3-6ヶ月", tasks: ["Headlessモードで自動PR", "全チーム展開・活用率80%目標", "定型タスク60-70%自動化"], hl: true },
  ];
  const sw2 = L.cw / 3;
  phases2.forEach((ph, i) => {
    const pcx = L.mx + i * sw2 + sw2 / 2;
    s.addShape(pptx.shapes.OVAL, {
      x: pcx - 0.15, y: lineY2 - 0.13, w: 0.3, h: 0.3,
      fill: { color: ph.hl ? C.accent : C.primary },
    });
    s.addText(ph.p, {
      x: pcx - sw2 / 2 + 0.05, y: tly, w: sw2 - 0.1, h: 0.6,
      fontSize: 10, fontFace: "Georgia", bold: true,
      color: ph.hl ? C.accent : C.primary, align: "center", wrap: true,
    });
    s.addText(ph.dur, {
      x: pcx - 0.6, y: lineY2 + 0.2, w: 1.2, h: 0.25,
      fontSize: 10, fontFace: "Calibri", bold: true, color: ph.hl ? C.accent : C.primary, align: "center",
    });
    ph.tasks.forEach((t, ti) => {
      s.addText("\u2022 " + t, {
        x: pcx - sw2 / 2 + 0.15, y: lineY2 + 0.55 + ti * 0.3, w: sw2 - 0.3, h: 0.28,
        fontSize: 9, fontFace: "Calibri", color: C.text, wrap: true,
      });
    });
  });
  footer(s, "業界推計 / Intercom・Shopify・GitLab事例, 2025");
}

// ============================
// SLIDE 14: 成功要因（2x2グリッド）
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: "FFFFFF" };
  header(s, "成功企業に共通する4要因 — 技術選定より組織的準備が導入成否を決める");
  const cellW = (L.cw - 0.3) / 2;
  const cellH = (L.bodyH - 0.3) / 2;
  const grid = [
    { x: L.mx, y: L.bodyTop, kw: "経営コミットメント", detail: "CTO/VPoE主導の予算承認とKPI設定。Shopify CEO宣言で活用率が25pt上昇", col: C.primary },
    { x: L.mx + cellW + 0.3, y: L.bodyTop, kw: "チャンピオン選定", detail: "技術力と社内影響力を持つ先行ユーザー3-5名。成功体験の可視化で自然拡散を促進", col: C.accent },
    { x: L.mx, y: L.bodyTop + cellH + 0.3, kw: "CLAUDE.md整備", detail: "導入初日に着手すべき最優先施策。導入チームは未導入比+40%の生産性向上を実現", col: C.accent },
    { x: L.mx + cellW + 0.3, y: L.bodyTop + cellH + 0.3, kw: "セキュリティ先行整備", detail: ".claudeignoreポリシー事前策定が必須。Intercom社は導入後インシデントゼロを達成", col: C.primary },
  ];
  grid.forEach((g) => {
    s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: g.x, y: g.y, w: cellW, h: cellH,
      fill: { color: C.surfaceAlt }, rectRadius: 0.1,
      line: { color: C.border, width: 0.5 },
    });
    s.addShape(pptx.shapes.RECTANGLE, {
      x: g.x + 0.12, y: g.y + 0.15, w: 0.05, h: cellH - 0.3,
      fill: { color: g.col },
    });
    s.addText(g.kw, {
      x: g.x + 0.3, y: g.y + 0.15, w: cellW - 0.5, h: 0.4,
      fontSize: 13, fontFace: "Georgia", bold: true, color: C.primary,
    });
    s.addText(g.detail, {
      x: g.x + 0.3, y: g.y + 0.6, w: cellW - 0.5, h: cellH - 0.8,
      fontSize: 10, fontFace: "Calibri", color: C.text, wrap: true,
    });
  });
  footer(s, "Intercom Blog / Shopify公式 / 匿名A社事例, 2025");
}

// ============================
// SLIDE 15: まとめ & Next Steps
// ============================
{
  const s = pptx.addSlide();
  s.background = { fill: C.primaryDark };
  s.addText("まとめと Next Steps", {
    x: L.mx, y: 0.4, w: L.cw, h: 0.6,
    fontSize: 24, fontFace: "Georgia", bold: true, color: C.textLight,
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: L.mx, y: 1.05, w: 2.5, h: 0.04, fill: { color: C.accent },
  });

  s.addText("Key Takeaways", {
    x: L.mx, y: 1.3, w: 4, h: 0.35,
    fontSize: 13, fontFace: "Georgia", bold: true, color: C.accent,
  });
  const takeaways = [
    "Claude Codeはコード補完ではなく自律型エージェント。200Kトークンで開発タスク全体を完遂する新カテゴリ",
    "Intercom 10倍高速化、Shopify 92%浸透を実証。ROI回収は3-6ヶ月でSaaS平均の1/3",
    "3段階導入で成功率80%。セキュリティ・品質・コストの3大リスクは全て管理可能",
  ];
  takeaways.forEach((t, i) => {
    const ty = 1.8 + i * 0.6;
    s.addShape(pptx.shapes.OVAL, {
      x: L.mx + 0.05, y: ty + 0.05, w: 0.3, h: 0.3,
      fill: { color: C.accent },
    });
    s.addText(String(i + 1), {
      x: L.mx + 0.05, y: ty + 0.05, w: 0.3, h: 0.3,
      fontSize: 11, fontFace: "Calibri", bold: true, color: C.textLight, align: "center", valign: "middle",
    });
    s.addText(t, {
      x: L.mx + 0.5, y: ty, w: L.cw - 0.7, h: 0.5,
      fontSize: 10, fontFace: "Calibri", color: "CCDDEE", valign: "middle", wrap: true,
    });
  });

  s.addText("Next Steps", {
    x: L.mx, y: 3.85, w: 4, h: 0.35,
    fontSize: 13, fontFace: "Georgia", bold: true, color: C.accent,
  });
  const steps2 = [
    "今週中: セキュリティポリシー初期検討とチャンピオン候補3-5名リストアップ",
    "2週間以内: CLAUDE.md初版作成とMax Plan契約でPoC環境セットアップ",
    "1ヶ月後: チャンピオンPoC開始、速度向上率のベースラインデータ収集",
    "四半期末: 定量効果レポート、経営会議でPhase 2移行判断",
  ];
  steps2.forEach((t, i) => {
    const ty = 4.35 + i * 0.55;
    s.addText("\u2192", {
      x: L.mx + 0.05, y: ty, w: 0.35, h: 0.4,
      fontSize: 14, color: C.accent, align: "center", valign: "middle",
    });
    s.addText(t, {
      x: L.mx + 0.45, y: ty, w: L.cw - 0.7, h: 0.4,
      fontSize: 10, fontFace: "Calibri", color: "CCDDEE", valign: "middle", wrap: true,
    });
  });

  footer(s, "本資料全体のまとめ", { dark: true });
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
