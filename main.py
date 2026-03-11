"""vCompany 自動資料作成ツール - エントリーポイント"""

import argparse
import sys

from src.pipeline import DocumentPipeline
from src.design.builder import DesignConfig


def main():
    parser = argparse.ArgumentParser(
        description="vCompany 自動資料作成ツール - テーマから自動で資料を生成"
    )
    parser.add_argument(
        "theme",
        help="資料のテーマ",
    )
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=["markdown", "html", "pdf", "pptx"],
        default=["pptx"],
        help="出力形式（複数指定可、デフォルト: pptx）",
    )
    parser.add_argument(
        "--context",
        default="",
        help="追加のコンテキスト情報",
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

    if args.all_formats:
        formats = ["markdown", "html", "pdf", "pptx"]
    else:
        formats = args.formats

    design = DesignConfig()
    pipeline = DocumentPipeline(output_dir=args.output_dir, design=design)

    print("=" * 60)
    print("vCompany 自動資料作成ツール")
    print("=" * 60)
    print(f"テーマ: {args.theme}")
    print(f"出力形式: {', '.join(formats)}")
    print(f"出力先: {args.output_dir}")
    print("=" * 60)

    result = pipeline.run(
        theme=args.theme,
        output_formats=formats,
        additional_context=args.context,
    )

    # 結果の表示
    print("\n" + "=" * 60)
    print("生成完了")
    print("=" * 60)

    print("\n出力ファイル:")
    for fmt, path in result["outputs"].items():
        print(f"  [{fmt}] {path}")

    if result["auto_fixes"]:
        print(f"\n自動修正: {len(result['auto_fixes'])} 件")
        for fix in result["auto_fixes"]:
            print(f"  - {fix.get('item', '')}")

    if result["manual_review_items"]:
        print(f"\n{result['manual_review']}")
    else:
        print("\nOwner確認が必要な項目はありません。")


if __name__ == "__main__":
    main()
