"""vCompany 自動資料作成ツール - エントリーポイント

Claude Code方式: Claude Codeが各フェーズを実行し、
本スクリプトはファイル出力を担当する。

使い方:
    Claude Codeが生成したJSONデータを引数で渡してファイル出力する。

    python main.py --input content.json --formats pptx markdown
    python main.py --input content.json --all-formats
"""

import argparse
import json
import sys

from src.pipeline import generate_document
from src.design.builder import DesignConfig


def main():
    parser = argparse.ArgumentParser(
        description="vCompany 自動資料作成ツール - コンテンツデータからファイルを生成"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="コンテンツデータのJSONファイルパス",
    )
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=["markdown", "html", "pdf", "pptx"],
        default=["pptx"],
        help="出力形式（複数指定可、デフォルト: pptx）",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="出力先ディレクトリ（デフォルト: output）",
    )
    parser.add_argument(
        "--all-formats",
        action="store_true",
        help="全形式（Markdown, HTML, PDF, PPTX）で出力",
    )

    args = parser.parse_args()

    # コンテンツデータの読み込み
    with open(args.input, "r", encoding="utf-8") as f:
        content = json.load(f)

    if args.all_formats:
        formats = ["markdown", "html", "pdf", "pptx"]
    else:
        formats = args.formats

    print("=" * 60)
    print("vCompany 自動資料作成ツール")
    print("=" * 60)
    print(f"タイトル: {content.get('title', '無題')}")
    print(f"セクション数: {len(content.get('sections', []))}")
    print(f"出力形式: {', '.join(formats)}")
    print(f"出力先: {args.output_dir}")
    print("=" * 60)

    result = generate_document(
        content=content,
        output_formats=formats,
        output_dir=args.output_dir,
    )

    print("\n生成完了:")
    for fmt, path in result["outputs"].items():
        print(f"  [{fmt}] {path}")


if __name__ == "__main__":
    main()
