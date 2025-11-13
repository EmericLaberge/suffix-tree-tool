"""Command-line interface for suffix-tree-tool."""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .builder import (
    DEFAULT_TERMINATOR,
    build_suffix_tree,
    dot_to_pdf,
    process_sequences,
    render_suffix_tree,
)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and render a generalized suffix tree for 1 to 5 sequences.",
    )
    parser.add_argument(
        "sequences",
        metavar="SEQ",
        nargs="+",
        help="Sequence(s) (1 to 5). Example: SEQ1 [SEQ2 ... SEQ5]",
    )
    parser.add_argument(
        "--include-terminal",
        action="store_true",
        help="Include the suffix that contains only the terminator (e.g. '#').",
    )
    parser.add_argument(
        "--unique-terminal",
        action="store_true",
        help="Assign a distinct terminator to each sequence.",
    )
    parser.add_argument(
        "--annotate-internal",
        action="store_true",
        help="Display depth (purple) and sequence indices (colors) on internal nodes.",
    )
    parser.add_argument(
        "--dot",
        default="suffix_tree.dot",
        help="Path to the output DOT file (default: %(default)s).",
    )
    parser.add_argument(
        "--pdf",
        default="suffix_tree.pdf",
        help="Path to the output PDF file (default: %(default)s).",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not attempt to automatically open the generated PDF.",
    )

    args = parser.parse_args(argv)

    if not (1 <= len(args.sequences) <= 5):
        parser.error("You must provide between 1 and 5 sequences.")

    return args


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    try:
        sequences = process_sequences(
            args.sequences, unique_terminal=args.unique_terminal
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    mode = "are distinct" if args.unique_terminal else f"all use '{DEFAULT_TERMINATOR}'"
    print(f"Normalized sequences (terminators {mode}):")
    for idx, (seq, terminator) in enumerate(sequences, start=1):
        print(f"  {idx}: {seq}{terminator}")

    suffix_tree = build_suffix_tree(
        sequences, include_terminal_suffix=args.include_terminal
    )
    print("Suffix Tree Nodes:", suffix_tree.nodes(data=True))
    print("Suffix Tree Edges:", suffix_tree.edges(data=True))

    dot_file = render_suffix_tree(
        suffix_tree,
        out_path=args.dot,
        annotate_internal=args.annotate_internal,
        total_sequences=len(sequences),
    )
    print("DOT written ->", dot_file)

    try:
        pdf_file = dot_to_pdf(
            dot_file, pdf_path=args.pdf, open_viewer=not args.no_open
        )
        print("PDF written ->", pdf_file)
    except Exception as exc:  # pylint: disable=broad-except
        print("Could not generate/open the PDF automatically:", exc)
        print("Manual command: dot -Tpdf", args.dot, "-o", args.pdf)


if __name__ == "__main__":  # pragma: no cover
    main()
