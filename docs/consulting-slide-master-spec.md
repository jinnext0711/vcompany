# コンサルティングファーム スライドマスタ仕様書
# python-pptx実装用 完全リファレンス

---

## 1. 各社ブランドカラー一覧（Web調査に基づく公開情報）

### 1-1. 戦略コンサル（MBB）

| ファーム | プライマリ | セカンダリ | アクセント | テキスト | フォント |
|---------|-----------|-----------|-----------|---------|---------|
| **McKinsey** | Deep Blue `#051C2C` | Electric Blue `#2251FF` | Light Blue `#A0D2DB` | Dark `#222222` | Georgia（タイトル）/ Arial（本文） |
| **BCG** | BCG Green `#29BA74` | Dark Green `#006341` | Dark Gray `#333333` | Dark `#222222` | Trebuchet MS |
| **Bain** | Bain Red `#EE3224` | Dark Red `#CC0000` | Dark Gray `#333333` | Dark `#222222` | Arial |

### 1-2. 総合コンサル（Big4 + Accenture）

| ファーム | プライマリ | セカンダリ | アクセント | テキスト | フォント |
|---------|-----------|-----------|-----------|---------|---------|
| **Deloitte** | Green `#86BC25` | Black `#000000` | Gray `#75787B` | Dark `#2D2D2D` | Arial |
| **Accenture** | Purple `#A100FF` | Black `#000000` | Gray `#6B6B6B` | Dark `#333333` | Graphik / Arial |
| **PwC** | Dark Orange `#DB4E18` | Light Orange `#E88D14` | Charcoal `#2D2D2D` | Dark `#333333` | Georgia / Arial |
| **EY** | Yellow `#FFE600` | Dark Gray `#2E2E38` | Charcoal `#333333` | Dark `#2E2E38` | Arial |
| **KPMG** | Blue `#00338D` | Persian Blue `#1E49E2` | Light Gray `#D3D3D3` | Dark `#333333` | Arial |

> **出典**: Brandfetch, BrandColorCode.com, color.adobe.com, encycolorpedia.com 等の公開ブランドカラーDB

---

## 2. スライドマスタの構成要素（全社共通パターン）

### 2-1. 共通スライドマスタ一覧（10パターン）

コンサル各社の公開資料を分析した結果、以下のスライドマスタが共通して使われている。

| # | マスタ名 | 用途 | 使用頻度 |
|---|---------|------|---------|
| 1 | **Title Slide** | 表紙 | 必須 |
| 2 | **Agenda / TOC** | 目次・アジェンダ | 必須 |
| 3 | **Section Divider** | セクション区切り | 必須 |
| 4 | **Action Title + Body** | 標準コンテンツ（最多使用） | 必須 |
| 5 | **Action Title + Table** | テーブル・比較一覧 | 必須 |
| 6 | **Action Title + Chart** | グラフ・チャート | 必須 |
| 7 | **Action Title + 2-Column** | 左右比較・並列 | 必須 |
| 8 | **KPI / Big Number** | 数値ハイライト | 推奨 |
| 9 | **Executive Summary** | エグゼクティブサマリー | 必須 |
| 10 | **Summary + Next Steps** | まとめ・次のアクション | 必須 |
| 11 | **Appendix Title** | 付録の表紙 | 推奨 |
| 12 | **Blank with Footer** | 自由配置用 | 推奨 |

---

## 3. スライドレイアウト詳細仕様（python-pptx座標系）

### 3-1. 基本寸法

```
スライドサイズ: 13.333 x 7.5 インチ（ワイドスクリーン 16:9）
python-pptx: Inches(13.333), Inches(7.5)
EMU換算: 12192000 x 6858000
```

### 3-2. 3層構造の座標仕様

```
┌────────────────────────────────────────────────────────────┐
│  LEFT MARGIN    CONTENT AREA                RIGHT MARGIN   │
│  0.5"                                       0.5"           │
│                                                            │
│  ┌──────────────────────────────────────────────────┐      │
│  │ HEADER ZONE (Action Title)                       │ 0.3" │ top margin
│  │ top=0.3", left=0.5", width=12.333", height=0.83"│      │
│  │ (2行分のアクションタイトル)                        │      │
│  ├──────────────────────────────────────────────────┤ 1.13"│
│  │ THIN ACCENT LINE (区切り線)                       │      │
│  │ top=1.15", left=0.5", width=12.333", height=0.02"│      │
│  ├──────────────────────────────────────────────────┤ 1.20"│
│  │                                                  │      │
│  │ BODY ZONE (コンテンツエリア)                      │      │
│  │ top=1.25", left=0.5", width=12.333", height=5.55"│      │
│  │                                                  │      │
│  │ ※ここに図表・テキスト・テーブル等を配置           │      │
│  │                                                  │      │
│  ├──────────────────────────────────────────────────┤ 6.80"│
│  │ FOOTER ZONE                                      │      │
│  │ top=7.05", left=0.5", width=12.333", height=0.30"│      │
│  │ [機密表示]      [出典/フッター]    [ページ番号]    │      │
│  └──────────────────────────────────────────────────┘ 7.35"│
│                                                     0.15"  │ bottom margin
└────────────────────────────────────────────────────────────┘
```

### 3-3. 各ゾーンの詳細座標（インチ）

| ゾーン | top | left | width | height | 備考 |
|--------|-----|------|-------|--------|------|
| **Action Title** | 0.30 | 0.50 | 12.333 | 0.83 | 20-22pt x 2行分 |
| **Accent Line** | 1.15 | 0.50 | 12.333 | 0.017 | 1.2pt線、アクセントカラー |
| **Body Area** | 1.25 | 0.50 | 12.333 | 5.55 | メインコンテンツ |
| **Footer Left** | 7.05 | 0.50 | 4.0 | 0.30 | 機密表示 "CONFIDENTIAL" |
| **Footer Center** | 7.05 | 4.50 | 4.333 | 0.30 | 出典・プロジェクト名 |
| **Footer Right** | 7.05 | 10.833 | 2.0 | 0.30 | ページ番号（右揃え） |

---

## 4. 各スライドマスタの詳細レイアウト仕様

### 4-1. Title Slide（表紙）

```
McKinsey式: 濃紺背景 + 白テキスト、ロゴ右下
BCG式:     白背景 + 濃色テキスト + 左にグリーンのアクセント帯
Bain式:    白背景 + 赤のアクセントライン
```

**python-pptx 座標仕様（McKinsey風統合版）:**

| 要素 | top | left | width | height | フォント | 色 |
|------|-----|------|-------|--------|---------|---|
| 背景 | - | - | 全面 | 全面 | - | Primary色ベタ塗り |
| メインタイトル | 2.0 | 1.0 | 11.333 | 1.5 | 36pt Bold | White `#FFFFFF` |
| サブタイトル | 3.7 | 1.0 | 11.333 | 0.8 | 18pt Regular | White 80% `#CCCCCC` |
| 区切り線 | 3.5 | 1.0 | 3.0 | 0.02 | - | Accent色 |
| 日付 | 5.0 | 1.0 | 5.0 | 0.4 | 14pt Regular | White 60% `#999999` |
| クライアント名 | 5.5 | 1.0 | 5.0 | 0.4 | 14pt Regular | White 60% `#999999` |
| 機密表示 | 6.8 | 1.0 | 5.0 | 0.3 | 10pt Regular | White 40% `#666666` |
| ロゴ | 6.5 | 10.5 | 2.333 | 0.7 | - | 画像 |

### 4-2. Agenda / TOC（目次）

| 要素 | top | left | width | height | フォント | 備考 |
|------|-----|------|-------|--------|---------|------|
| タイトル "Agenda" | 0.30 | 0.50 | 12.333 | 0.83 | 22pt Bold | |
| Accent Line | 1.15 | 0.50 | 12.333 | 0.017 | - | |
| 項目1 | 1.50 | 0.50 | 12.333 | 0.60 | 16pt Bold + 14pt Regular | ハイライト中のセクションはアクセントカラー |
| 項目2 | 2.20 | 0.50 | 12.333 | 0.60 | 同上 | グレーアウト（非アクティブ） |
| 項目3 | 2.90 | 0.50 | 12.333 | 0.60 | 同上 | |
| 項目4 | 3.60 | 0.50 | 12.333 | 0.60 | 同上 | |
| 項目5 | 4.30 | 0.50 | 12.333 | 0.60 | 同上 | |
| Footer | 7.05 | 0.50 | 12.333 | 0.30 | 9pt | 標準フッター |

**アジェンダの特徴（各社共通）:**
- 現在のセクションはPrimary色 + Bold
- 他のセクションはLight Gray `#CCCCCC` でグレーアウト
- 番号付き（01, 02, 03...）で表示

### 4-3. Section Divider（セクション区切り）

```
McKinsey式: 濃紺背景 + 白い大文字テキスト
BCG式:     白背景 + 左端にグリーンの太い帯（幅0.3"）
Bain式:    白背景 + 赤い区切り線
```

| 要素 | top | left | width | height | フォント | 色 |
|------|-----|------|-------|--------|---------|---|
| 背景 | - | - | 全面 | 全面 | - | Primary色 or White |
| セクション番号 | 2.5 | 1.0 | 2.0 | 0.8 | 48pt Bold | Accent or White |
| セクション名 | 3.3 | 1.0 | 10.0 | 1.2 | 32pt Bold | White or Primary |
| サブテキスト | 4.6 | 1.0 | 10.0 | 0.6 | 16pt Regular | White 70% or Gray |
| Footer | 7.05 | 0.50 | 12.333 | 0.30 | 9pt | 標準フッター |

### 4-4. Action Title + Body（標準コンテンツ）- 最頻出

**全コンサルで最も多用されるレイアウト。スライドの60-70%がこのパターン。**

| 要素 | top | left | width | height | フォント |
|------|-----|------|-------|--------|---------|
| Action Title | 0.30 | 0.50 | 12.333 | 0.83 | 20pt Bold |
| Accent Line | 1.15 | 0.50 | 12.333 | 0.017 | - |
| Body Area | 1.25 | 0.50 | 12.333 | 5.55 | 14pt Regular |
| Footer | 7.05 | 0.50 | 12.333 | 0.30 | 9pt |

**ボディエリアのグリッド分割パターン:**

```
[1列 全幅]          12.333" x 5.55"   ← テキスト・テーブル・チャート用
[2列均等]           6.0" + 0.333" gap + 6.0"
[3列均等]           3.889" + 0.333" gap x2 + 3.889"
[1/3 + 2/3]        3.889" + 0.333" gap + 8.111"
[2/3 + 1/3]        8.111" + 0.333" gap + 3.889"
```

### 4-5. Action Title + Table（テーブル）

ボディエリア内にテーブルを配置。

| 要素 | top | left | width | height |
|------|-----|------|-------|--------|
| Action Title | 0.30 | 0.50 | 12.333 | 0.83 |
| Accent Line | 1.15 | 0.50 | 12.333 | 0.017 |
| **Table** | 1.40 | 0.50 | 12.333 | 可変 |
| Footer | 7.05 | 0.50 | 12.333 | 0.30 |

### 4-6. Action Title + Chart（グラフ）

| 要素 | top | left | width | height |
|------|-----|------|-------|--------|
| Action Title | 0.30 | 0.50 | 12.333 | 0.83 |
| Accent Line | 1.15 | 0.50 | 12.333 | 0.017 |
| **Chart Area** | 1.25 | 0.50 | 12.333 | 5.00 |
| **Source/Note** | 6.40 | 0.50 | 12.333 | 0.40 |
| Footer | 7.05 | 0.50 | 12.333 | 0.30 |

### 4-7. Action Title + 2-Column（左右分割）

| 要素 | top | left | width | height |
|------|-----|------|-------|--------|
| Action Title | 0.30 | 0.50 | 12.333 | 0.83 |
| Accent Line | 1.15 | 0.50 | 12.333 | 0.017 |
| **Left Column** | 1.25 | 0.50 | 6.0 | 5.55 |
| **Right Column** | 1.25 | 6.833 | 6.0 | 5.55 |
| Footer | 7.05 | 0.50 | 12.333 | 0.30 |

### 4-8. KPI / Big Number（数値ハイライト）

| 要素 | top | left | width | height | フォント |
|------|-----|------|-------|--------|---------|
| Action Title | 0.30 | 0.50 | 12.333 | 0.83 | 20pt Bold |
| Accent Line | 1.15 | 0.50 | 12.333 | 0.017 | |
| KPI 1 数値 | 2.0 | 0.50 | 3.889 | 1.2 | 48pt Bold, Primary |
| KPI 1 ラベル | 3.2 | 0.50 | 3.889 | 0.5 | 14pt Regular, Gray |
| KPI 2 数値 | 2.0 | 4.722 | 3.889 | 1.2 | 48pt Bold, Primary |
| KPI 2 ラベル | 3.2 | 4.722 | 3.889 | 0.5 | 14pt Regular, Gray |
| KPI 3 数値 | 2.0 | 8.944 | 3.889 | 1.2 | 48pt Bold, Primary |
| KPI 3 ラベル | 3.2 | 8.944 | 3.889 | 0.5 | 14pt Regular, Gray |
| 補足テキスト | 4.5 | 0.50 | 12.333 | 2.0 | 14pt Regular |
| Footer | 7.05 | 0.50 | 12.333 | 0.30 | 9pt |

### 4-9. Executive Summary（エグゼクティブサマリー）

| 要素 | top | left | width | height | フォント |
|------|-----|------|-------|--------|---------|
| Title "Executive Summary" | 0.30 | 0.50 | 12.333 | 0.83 | 22pt Bold |
| Accent Line | 1.15 | 0.50 | 12.333 | 0.017 | |
| メッセージ1 | 1.50 | 0.50 | 12.333 | 1.0 | 16pt Bold（主張）+ 14pt（補足） |
| メッセージ2 | 2.70 | 0.50 | 12.333 | 1.0 | 同上 |
| メッセージ3 | 3.90 | 0.50 | 12.333 | 1.0 | 同上 |
| メッセージ4 | 5.10 | 0.50 | 12.333 | 1.0 | 同上 |
| Footer | 7.05 | 0.50 | 12.333 | 0.30 | 9pt |

**McKinsey/BCG式の特徴:**
- 各メッセージの左端に番号インジケーター（丸数字）
- 太字の1行キーメッセージ + Regular の2-3行補足
- 左側に色付きの縦バー（幅0.04"）を配置してメッセージを区切る

### 4-10. Summary + Next Steps（まとめ）

| 要素 | top | left | width | height |
|------|-----|------|-------|--------|
| Action Title | 0.30 | 0.50 | 12.333 | 0.83 |
| Accent Line | 1.15 | 0.50 | 12.333 | 0.017 |
| **左: Key Takeaways** | 1.25 | 0.50 | 6.0 | 5.55 |
| **右: Next Steps** | 1.25 | 6.833 | 6.0 | 5.55 |
| Footer | 7.05 | 0.50 | 12.333 | 0.30 |

---

## 5. デザイン要素の詳細仕様

### 5-1. アクションタイトルバー

| 属性 | McKinsey | BCG | Bain | 統合仕様 |
|------|---------|-----|------|---------|
| 高さ | 0.83" | 0.83" | 0.75" | **0.83"** |
| フォントサイズ | 20-22pt | 18-20pt | 18-20pt | **20pt** |
| ウェイト | Bold | Bold | Bold | **Bold** |
| 色 | `#051C2C` | `#333333` | `#333333` | **Primary色** |
| 行数 | 最大2行 | 最大2行 | 最大2行 | **最大2行** |
| 配置 | 左揃え | 左揃え | 左揃え | **左揃え** |
| 背景 | なし（白） | なし | なし | **なし** |

**重要**: アクションタイトルはトピック名ではなく「主張文（So What）」を記載する。
- NG: "市場規模分析"
- OK: "国内SaaS市場は2030年までに3倍に拡大し、参入余地は十分にある"

### 5-2. アクセント区切り線

| 属性 | 値 |
|------|-----|
| 太さ | 1.2pt (Pt(12000)) |
| 色 | アクセントカラー（各社異なる） |
| 位置 | タイトル下 0.02" ギャップ |
| 幅 | ボディエリアと同幅 (12.333") |

### 5-3. フッター構成

```
┌──────────────┬──────────────────────────┬──────────────┐
│ 機密表示      │  出典 / プロジェクト名     │   ページ番号  │
│ 左揃え 9pt   │  中央揃え 9pt             │   右揃え 9pt  │
│ `#999999`    │  `#999999`               │   `#999999`  │
└──────────────┴──────────────────────────┴──────────────┘
```

| 要素 | 典型的な内容 | フォント | 色 |
|------|------------|---------|---|
| 機密表示 | "CONFIDENTIAL" / "DRAFT" | 9pt Regular | `#999999` |
| 出典 | "Source: Company analysis" | 9pt Regular | `#999999` |
| ページ番号 | "12" or "12 / 45" | 9pt Regular | `#999999` |

**各社の違い:**
- McKinsey: 右下にページ番号のみ、機密表示は目立たない位置
- BCG: フッター左にロゴ、右にページ番号
- Deloitte: 下部に細いグリーンライン + ページ番号右下

### 5-4. ボディエリアのグリッドシステム

**12列グリッド（推奨）:**

```
コンテンツ幅: 12.333"
列数: 12
列幅: 0.944" (12.333" / 12 = 1.028" - ガター)
ガター: 0.333" (列間の余白)

よく使うグリッド:
  全幅      = 12列 = 12.333"
  1/2       = 6列  = 6.000" (gap 0.333")
  1/3       = 4列  = 3.889" (gap 0.333")
  2/3       = 8列  = 8.111" (gap 0.333")
  1/4       = 3列  = 2.833" (gap 0.333")
  3/4       = 9列  = 9.167" (gap 0.333")
```

---

## 6. 図表デザイン基準

### 6-1. テーブルデザイン

```python
# python-pptx テーブルスタイル仕様
TABLE_STYLE = {
    "header": {
        "bg_color": "PRIMARY",        # 各社のプライマリカラー
        "font_color": "#FFFFFF",       # 白
        "font_size": Pt(11),
        "font_bold": True,
        "alignment": PP_ALIGN.LEFT,
        "cell_height": Inches(0.40),
        "padding_top": Inches(0.05),
        "padding_bottom": Inches(0.05),
        "padding_left": Inches(0.10),
        "padding_right": Inches(0.10),
    },
    "body_odd": {
        "bg_color": "#FFFFFF",
        "font_color": "#333333",
        "font_size": Pt(10),
        "font_bold": False,
        "cell_height": Inches(0.35),
    },
    "body_even": {
        "bg_color": "#F5F5F5",         # ゼブラストライプ
        "font_color": "#333333",
        "font_size": Pt(10),
        "font_bold": False,
        "cell_height": Inches(0.35),
    },
    "borders": {
        "header_bottom": {"color": "PRIMARY", "width": Pt(1.5)},
        "row_bottom": {"color": "#E0E0E0", "width": Pt(0.5)},
        "outer": None,                  # 外枠なし
        "vertical": None,               # 縦罫線なし
    },
    "total_row": {
        "bg_color": "#F0F0F0",
        "font_bold": True,
        "border_top": {"color": "#333333", "width": Pt(1.0)},
    },
}
```

**各社テーブルの特徴:**
- McKinsey: ヘッダーは濃紺背景 + 白テキスト、極力シンプル、縦罫線なし
- BCG: ヘッダーは薄いグリーン背景、セル間のスペースを広めに取る
- Bain: ヘッダーは白背景 + 赤い下線、シンプルで余白重視
- Deloitte: ヘッダーは黒背景 + 白テキスト + グリーンのアクセント

### 6-2. グラフデザイン基準

```python
CHART_STYLE = {
    # 軸の設定
    "axis": {
        "line_color": "#999999",
        "line_width": Pt(0.75),
        "label_font_size": Pt(9),
        "label_font_color": "#666666",
        "title_font_size": Pt(10),
        "title_font_color": "#333333",
        "y_axis_start_at_zero": True,     # Y軸は原則0開始
    },
    # グリッド線
    "gridlines": {
        "major_horizontal": True,          # 横方向の主グリッドのみ表示
        "major_vertical": False,           # 縦方向は非表示
        "minor": False,                    # 副グリッドは非表示
        "color": "#E8E8E8",
        "width": Pt(0.5),
        "dash_style": "dash",              # 破線
    },
    # 凡例
    "legend": {
        "position": "bottom",              # 下部配置（スライド上部を圧迫しない）
        "font_size": Pt(9),
        "font_color": "#666666",
    },
    # データラベル
    "data_labels": {
        "font_size": Pt(9),
        "font_color": "#333333",
        "show_value": True,
        "show_category": False,
        "number_format": "#,##0",
    },
    # カラーパレット（データ系列用、最大6色）
    "series_colors": [
        "PRIMARY",                         # 主要データ
        "ACCENT",                          # 比較データ
        "#999999",                         # 第3データ
        "#CCCCCC",                         # 第4データ
        "#E0E0E0",                         # 第5データ
        "#F5F5F5",                         # 第6データ
    ],
}
```

**各社チャートの原則:**
- 3D効果は絶対禁止
- グリッド線は最小限（横方向の薄いダッシュ線のみ）
- ラベルは直接データポイントに配置（離れた凡例を避ける）
- BCG「10秒ルール」: チャートは10秒で理解できること

### 6-3. フレームワーク図のデザインパターン

#### 2x2 マトリクス

```python
MATRIX_2x2 = {
    "position": {"top": Inches(1.25), "left": Inches(1.5)},
    "size": {"width": Inches(9.333), "height": Inches(5.0)},
    "quadrant_gap": Inches(0.05),
    "quadrant_colors": {
        "top_left": "#E8F4FD",     # 薄いブルー
        "top_right": "#D4EDDA",    # 薄いグリーン
        "bottom_left": "#FFF3CD",  # 薄いイエロー
        "bottom_right": "#F8D7DA", # 薄いレッド
    },
    "axis": {
        "color": "#333333",
        "width": Pt(1.5),
        "arrow": True,
        "label_font_size": Pt(12),
        "label_font_bold": True,
    },
    "bubble": {
        "min_size": Inches(0.3),
        "max_size": Inches(1.0),
        "font_size": Pt(9),
    },
}
```

#### ウォーターフォールチャート

```python
WATERFALL = {
    "bar_width_ratio": 0.6,            # バーの幅（カテゴリ幅の60%）
    "positive_color": "PRIMARY",        # 増加: プライマリカラー
    "negative_color": "#CC3333",        # 減少: レッド
    "total_color": "#666666",           # 合計: グレー
    "connector_line": {
        "color": "#CCCCCC",
        "width": Pt(0.5),
        "dash": "dash",
    },
    "data_label_font_size": Pt(9),
    "category_label_font_size": Pt(10),
}
```

#### プロセスフロー（横方向）

```python
PROCESS_FLOW = {
    "step_shape": "rounded_rectangle",
    "step_width": Inches(2.0),
    "step_height": Inches(1.2),
    "step_gap": Inches(0.4),             # ステップ間の矢印領域
    "step_fill": "PRIMARY",
    "step_text_color": "#FFFFFF",
    "step_font_size": Pt(12),
    "arrow_color": "#999999",
    "arrow_width": Pt(2.0),
    "max_steps": 5,                       # 横方向に最大5ステップ
    "number_indicator": True,             # ステップ番号表示
}
```

---

## 7. python-pptx 実装用 完全数値一覧

### 7-1. 定数定義

```python
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# === スライドサイズ ===
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# === マージン ===
MARGIN_LEFT = Inches(0.5)
MARGIN_RIGHT = Inches(0.5)
MARGIN_TOP = Inches(0.3)
MARGIN_BOTTOM = Inches(0.15)

# === コンテンツ幅 ===
CONTENT_WIDTH = Inches(12.333)        # 13.333 - 0.5 - 0.5

# === ヘッダー（アクションタイトル）===
HEADER_TOP = Inches(0.3)
HEADER_LEFT = Inches(0.5)
HEADER_WIDTH = CONTENT_WIDTH
HEADER_HEIGHT = Inches(0.83)
HEADER_FONT_SIZE = Pt(20)
HEADER_FONT_BOLD = True

# === アクセントライン ===
ACCENT_LINE_TOP = Inches(1.15)
ACCENT_LINE_LEFT = Inches(0.5)
ACCENT_LINE_WIDTH = CONTENT_WIDTH
ACCENT_LINE_HEIGHT = Inches(0.017)

# === ボディエリア ===
BODY_TOP = Inches(1.25)
BODY_LEFT = Inches(0.5)
BODY_WIDTH = CONTENT_WIDTH
BODY_HEIGHT = Inches(5.55)
BODY_FONT_SIZE = Pt(14)

# === フッター ===
FOOTER_TOP = Inches(7.05)
FOOTER_LEFT = Inches(0.5)
FOOTER_HEIGHT = Inches(0.30)
FOOTER_FONT_SIZE = Pt(9)
FOOTER_COLOR = RGBColor(0x99, 0x99, 0x99)

# === 2カラムレイアウト ===
COL2_LEFT_WIDTH = Inches(6.0)
COL2_RIGHT_LEFT = Inches(6.833)
COL2_RIGHT_WIDTH = Inches(6.0)
COL2_GAP = Inches(0.333)

# === 3カラムレイアウト ===
COL3_WIDTH = Inches(3.889)
COL3_COL1_LEFT = Inches(0.5)
COL3_COL2_LEFT = Inches(4.722)
COL3_COL3_LEFT = Inches(8.944)
COL3_GAP = Inches(0.333)
```

### 7-2. ブランドカラー定義

```python
# === McKinsey風カラー ===
MCKINSEY_COLORS = {
    "primary":    RGBColor(0x05, 0x1C, 0x2C),  # #051C2C Deep Blue
    "secondary":  RGBColor(0x22, 0x51, 0xFF),  # #2251FF Electric Blue
    "accent":     RGBColor(0xA0, 0xD2, 0xDB),  # #A0D2DB Light Blue
    "text":       RGBColor(0x22, 0x22, 0x22),  # #222222
    "white":      RGBColor(0xFF, 0xFF, 0xFF),  # #FFFFFF
    "light_gray": RGBColor(0xF5, 0xF5, 0xF5),  # #F5F5F5
    "gray":       RGBColor(0x99, 0x99, 0x99),  # #999999
}

# === BCG風カラー ===
BCG_COLORS = {
    "primary":    RGBColor(0x29, 0xBA, 0x74),  # #29BA74 BCG Green
    "secondary":  RGBColor(0x00, 0x63, 0x41),  # #006341 Dark Green
    "accent":     RGBColor(0x33, 0x33, 0x33),  # #333333
    "text":       RGBColor(0x22, 0x22, 0x22),  # #222222
    "white":      RGBColor(0xFF, 0xFF, 0xFF),
    "light_gray": RGBColor(0xF5, 0xF5, 0xF5),
    "gray":       RGBColor(0x99, 0x99, 0x99),
}

# === Bain風カラー ===
BAIN_COLORS = {
    "primary":    RGBColor(0xEE, 0x32, 0x24),  # #EE3224 Bain Red
    "secondary":  RGBColor(0xCC, 0x00, 0x00),  # #CC0000
    "accent":     RGBColor(0x33, 0x33, 0x33),  # #333333
    "text":       RGBColor(0x22, 0x22, 0x22),  # #222222
    "white":      RGBColor(0xFF, 0xFF, 0xFF),
    "light_gray": RGBColor(0xF5, 0xF5, 0xF5),
    "gray":       RGBColor(0x99, 0x99, 0x99),
}

# === Deloitte風カラー ===
DELOITTE_COLORS = {
    "primary":    RGBColor(0x86, 0xBC, 0x25),  # #86BC25 Deloitte Green
    "secondary":  RGBColor(0x00, 0x00, 0x00),  # #000000
    "accent":     RGBColor(0x75, 0x78, 0x7B),  # #75787B
    "text":       RGBColor(0x2D, 0x2D, 0x2D),  # #2D2D2D
    "white":      RGBColor(0xFF, 0xFF, 0xFF),
    "light_gray": RGBColor(0xF5, 0xF5, 0xF5),
    "gray":       RGBColor(0x99, 0x99, 0x99),
}

# === Accenture風カラー ===
ACCENTURE_COLORS = {
    "primary":    RGBColor(0xA1, 0x00, 0xFF),  # #A100FF Purple
    "secondary":  RGBColor(0x00, 0x00, 0x00),  # #000000
    "accent":     RGBColor(0x6B, 0x6B, 0x6B),  # #6B6B6B
    "text":       RGBColor(0x33, 0x33, 0x33),  # #333333
    "white":      RGBColor(0xFF, 0xFF, 0xFF),
    "light_gray": RGBColor(0xF5, 0xF5, 0xF5),
    "gray":       RGBColor(0x99, 0x99, 0x99),
}

# === PwC風カラー ===
PWC_COLORS = {
    "primary":    RGBColor(0xDB, 0x4E, 0x18),  # #DB4E18 Dark Orange
    "secondary":  RGBColor(0xE8, 0x8D, 0x14),  # #E88D14 Light Orange
    "accent":     RGBColor(0x2D, 0x2D, 0x2D),  # #2D2D2D
    "text":       RGBColor(0x33, 0x33, 0x33),  # #333333
    "white":      RGBColor(0xFF, 0xFF, 0xFF),
    "light_gray": RGBColor(0xF5, 0xF5, 0xF5),
    "gray":       RGBColor(0x99, 0x99, 0x99),
}

# === EY風カラー ===
EY_COLORS = {
    "primary":    RGBColor(0xFF, 0xE6, 0x00),  # #FFE600 Yellow
    "secondary":  RGBColor(0x2E, 0x2E, 0x38),  # #2E2E38 Dark Gray
    "accent":     RGBColor(0x33, 0x33, 0x33),  # #333333
    "text":       RGBColor(0x2E, 0x2E, 0x38),  # #2E2E38
    "white":      RGBColor(0xFF, 0xFF, 0xFF),
    "light_gray": RGBColor(0xF5, 0xF5, 0xF5),
    "gray":       RGBColor(0x99, 0x99, 0x99),
}

# === KPMG風カラー ===
KPMG_COLORS = {
    "primary":    RGBColor(0x00, 0x33, 0x8D),  # #00338D KPMG Blue
    "secondary":  RGBColor(0x1E, 0x49, 0xE2),  # #1E49E2 Persian Blue
    "accent":     RGBColor(0xD3, 0xD3, 0xD3),  # #D3D3D3
    "text":       RGBColor(0x33, 0x33, 0x33),  # #333333
    "white":      RGBColor(0xFF, 0xFF, 0xFF),
    "light_gray": RGBColor(0xF5, 0xF5, 0xF5),
    "gray":       RGBColor(0x99, 0x99, 0x99),
}
```

### 7-3. フォント定義

```python
# === フォント設定 ===
FONTS = {
    "mckinsey": {
        "title": "Georgia",
        "body": "Arial",
    },
    "bcg": {
        "title": "Trebuchet MS",
        "body": "Trebuchet MS",
    },
    "bain": {
        "title": "Arial",
        "body": "Arial",
    },
    "deloitte": {
        "title": "Arial",
        "body": "Arial",
    },
    "accenture": {
        "title": "Arial",          # Graphik は商用フォント、代替として Arial
        "body": "Arial",
    },
    "pwc": {
        "title": "Georgia",
        "body": "Arial",
    },
    "ey": {
        "title": "Arial",
        "body": "Arial",
    },
    "kpmg": {
        "title": "Arial",
        "body": "Arial",
    },
    # 日本語対応の場合
    "japanese": {
        "title": "Noto Sans JP",
        "body": "Noto Sans JP",
    },
}

# === フォントサイズ階層 ===
FONT_SIZES = {
    "slide_title":        Pt(36),   # 表紙タイトル
    "action_title":       Pt(20),   # アクションタイトル（全コンテンツスライド）
    "section_title":      Pt(32),   # セクション区切りタイトル
    "section_number":     Pt(48),   # セクション番号
    "subtitle":           Pt(18),   # サブタイトル
    "heading":            Pt(16),   # セクション見出し（ボディ内）
    "body":               Pt(14),   # 本文
    "body_small":         Pt(12),   # 小さい本文
    "table_header":       Pt(11),   # テーブルヘッダー
    "table_body":         Pt(10),   # テーブル本文
    "data_label":         Pt(9),    # データラベル・グラフラベル
    "caption":            Pt(9),    # キャプション・注釈
    "footer":             Pt(9),    # フッター
    "kpi_number":         Pt(48),   # KPI数値
    "kpi_label":          Pt(14),   # KPIラベル
}
```

---

## 8. 各社スタイル比較サマリー

### 8-1. 全体的なデザイン哲学

| 属性 | McKinsey | BCG | Bain | Deloitte | Accenture |
|------|---------|-----|------|---------|-----------|
| 配色 | 50 shades of blue | Green + Gray | Red + Gray | Green + Black | Purple + Black |
| 密度 | 中（余白重視） | 高（チャート多用） | 中 | 中 | 中-高 |
| タイトル | 2行以内の主張文 | 1-2行の主張文 | 1-2行の主張文 | 見出し + バンパー | 見出し形式 |
| 特徴 | ミニマル、深い青 | データ重視、グリーン | シンプル、赤アクセント | 構造化、グリーンドット | モダン、パープル |
| タイトルフォント | Georgia (Serif) | Trebuchet MS | Arial | Arial | Graphik/Arial |
| 本文フォント | Arial | Trebuchet MS | Arial | Arial | Arial |

### 8-2. 各社共通の鉄則

1. **アクションタイトル必須**: タイトルは「結論・主張」を述べる文であること
2. **1スライド1メッセージ**: 複数のメッセージを1枚に詰め込まない
3. **ピラミッド原則**: トップダウンで結論から入る
4. **MECE**: 漏れなくダブりなく構造化
5. **10秒ルール**: 各スライドは10秒以内に要点が伝わること
6. **3D禁止**: グラフに3D効果は使わない
7. **色は控えめ**: ブランドカラーは5%程度のアクセントとして使う
8. **フォントは1-2種類**: それ以上は使わない
9. **フッターの一貫性**: 全スライドでフッター（出典・ページ番号）を統一

---

## 9. vCompany統合テンプレートへの推奨事項

既存の `design-rules-consulting.md` の仕様を尊重しつつ、本調査結果から以下を推奨する。

### 9-1. 実装すべきスライドマスタ（優先度順）

| 優先度 | マスタ名 | 理由 |
|--------|---------|------|
| P0 | Action Title + Body | 全スライドの60-70%を占める |
| P0 | Title Slide | 必須 |
| P0 | Section Divider | ストーリー構造の区切り |
| P0 | Action Title + Table | データ比較に必須 |
| P0 | Summary + Next Steps | クロージング必須 |
| P1 | Agenda / TOC | 長いデッキに必須 |
| P1 | Executive Summary | 冒頭に必須 |
| P1 | Action Title + Chart | グラフスライド |
| P1 | Action Title + 2-Column | 比較レイアウト |
| P1 | KPI / Big Number | 数値インパクト |
| P2 | Appendix Title | 付録用 |
| P2 | Blank with Footer | 自由配置用 |

### 9-2. vCompanyカラーとの整合

vCompanyの既存カラー（Primary `#1A1A2E`, Highlight `#53868B`）はMcKinsey的な濃紺系と近い。
現行の配色を維持しつつ、本仕様書の座標・レイアウト体系を適用することを推奨する。

---

## Sources

- [Decoding McKinsey's new visual identity and PowerPoint template](https://slideworks.io/resources/decoding-mckinseys-visual-identity-and-powerpoint-template)
- [McKinsey Presentation Structure (A Guide for Consultants)](https://slidemodel.com/mckinsey-presentation-structure/)
- [3 Great Examples Of Slide Structure From McKinsey, Bain, And BCG](https://www.theanalystacademy.com/consulting-slide-structure/)
- [The anatomy of a consulting slide - PowerTools](https://pptpowertools.com/the-anatomy-of-a-consulting-slide/)
- [600+ Real Consulting Presentations](https://www.theanalystacademy.com/consulting-presentations/)
- [How McKinsey Consultants Make Presentations](https://slideworks.io/resources/how-mckinsey-consultants-make-presentations)
- [Mastering the McKinsey/BCG-Style PowerPoint Deck](https://www.linkedin.com/pulse/mastering-mckinseybcg-style-powerpoint-deck-your-niklas-scipio)
- [Deloitte Brand Color Codes](https://www.brandcolorcode.com/deloitte)
- [Accenture Brand Color Codes](https://www.brandcolorcode.com/accenture)
- [PwC Brand Color Codes](https://www.brandcolorcode.com/pricewaterhousecoopers-pwc)
- [EY Brand Color Codes](https://www.brandcolorcode.com/ernst-young)
- [KPMG Brand Color Codes](https://www.brandcolorcode.com/kpmg)
- [Bain & Company Brand Color Codes](https://www.brandcolorcode.com/bain-company)
- [BCG Brand Color Codes](https://www.brandcolorcode.com/boston-consulting-group)
- [McKinsey Brand Colors - Brandfetch](https://brandfetch.com/mckinsey.com)
- [BCG Color Guide - Scribd](https://www.scribd.com/doc/267329899/Bcg-Color-Guide)
- [Consulting Template Slides - MBB Style - SlideShare](https://www.slideshare.net/slideshow/consulting-template-slides-mckinsey-bcg-bain-style-communication/232047945)
- [Design Principles for McKinsey Quantitative Charts](https://umbrex.com/resources/the-busy-consultants-guide-to-quantitative-charts/design-principles-for-mckinsey-quantitative-charts/)
- [BCG Slide Breakdown - Analyst Academy](https://www.theanalystacademy.com/bcg-slide-breakdown/)
- [Deloitte Presentation Structure](https://slidemodel.com/deloitte-presentation-structure/)
- [Bain ADAPT Design System - Colors](https://designsystem.adapt.bain.com/designers/guides/colors/)
- [python-pptx Documentation](https://python-pptx.readthedocs.io/en/latest/)
- [How to Create McKinsey-Style Presentations (2026 Guide)](https://slideuplift.com/blog/mckinsey-style-presentation/)
