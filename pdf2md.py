#!/usr/bin/env python3
import argparse

import pymupdf4llm

DEFAULT_OUTPUT = "output.md"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a PDF file into Markdown using pymupdf4llm."
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Path to the source PDF file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT,
        help="Path to write the converted Markdown output.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    markdown_text = pymupdf4llm.to_markdown(args.input, header=False, footer=False, page_numbers=False, force_ocr=False)

    with open(args.output, "w", encoding="utf-8") as output_file:
        output_file.write(markdown_text)