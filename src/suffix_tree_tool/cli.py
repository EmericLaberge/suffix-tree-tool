"""Interface en ligne de commande pour suffix-tree-tool."""
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
        description="Construit et rend un arbre des suffixes généralisé pour 1 à 5 séquences.",
    )
    parser.add_argument(
        "sequences",
        metavar="SEQ",
        nargs="+",
        help="Séquence(s) (1 à 5). Exemple: SEQ1 [SEQ2 ... SEQ5]",
    )
    parser.add_argument(
        "--include-terminal",
        action="store_true",
        help="Inclure le suffixe ne contenant que le terminateur (ex: '#').",
    )
    parser.add_argument(
        "--unique-terminal",
        action="store_true",
        help="Attribuer un terminateur distinct à chaque séquence.",
    )
    parser.add_argument(
        "--annotate-internal",
        action="store_true",
        help="Afficher profondeur (violet) et séquences (couleurs) sur les nœuds internes.",
    )
    parser.add_argument(
        "--dot",
        default="suffix_tree.dot",
        help="Chemin du fichier DOT de sortie (défaut: %(default)s).",
    )
    parser.add_argument(
        "--pdf",
        default="suffix_tree.pdf",
        help="Chemin du PDF de sortie (défaut: %(default)s).",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Ne pas tenter d'ouvrir automatiquement le PDF généré.",
    )

    args = parser.parse_args(argv)

    if not (1 <= len(args.sequences) <= 5):
        parser.error("Vous devez fournir entre 1 et 5 séquences.")

    return args


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    try:
        sequences = process_sequences(
            args.sequences, unique_terminal=args.unique_terminal
        )
    except ValueError as exc:
        print(f"Erreur: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    mode = (
        "distincts" if args.unique_terminal else f"identiques '{DEFAULT_TERMINATOR}'"
    )
    print(f"Séquences normalisées (terminateurs {mode}):")
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
    print("DOT écrit ->", dot_file)

    try:
        pdf_file = dot_to_pdf(
            dot_file, pdf_path=args.pdf, open_viewer=not args.no_open
        )
        print("PDF écrit ->", pdf_file)
    except Exception as exc:  # pylint: disable=broad-except
        print("Impossible de générer/ouvrir le PDF automatiquement:", exc)
        print(
            "Commande manuelle: dot -Tpdf",
            args.dot,
            "-o",
            args.pdf,
        )


if __name__ == "__main__":  # pragma: no cover
    main()
