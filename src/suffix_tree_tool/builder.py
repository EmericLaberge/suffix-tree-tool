"""Functions to build and render a generalized suffix tree."""
from __future__ import annotations

from typing import List, Sequence, Tuple
import os
import shutil
import subprocess

import networkx as nx

DEFAULT_TERMINATOR = "#"
UNIQUE_TERMINATORS = ["#", "$", "%", "&", "!"]
SEQUENCE_COLORS = {
    1: "black",
    2: "red",
    3: "blue",
    4: "green",
    5: "orange",
}


def process_sequences(
    raw_sequences: Sequence[str], unique_terminal: bool = False
) -> List[Tuple[str, str]]:
    """Sanitize sequences and assign terminators.

    Parameters
    ----------
    raw_sequences
        Sequences provided by the user.
    unique_terminal
        When ``True``, each sequence receives a distinct terminator
        (following the ``UNIQUE_TERMINATORS`` order). Otherwise, all share
        ``DEFAULT_TERMINATOR``.

    Returns
    -------
    list of tuple
        List of ``(sequence, terminator)`` tuples ready for construction.
    """

    if not raw_sequences:
        raise ValueError("At least one sequence is required.")

    if unique_terminal and len(raw_sequences) > len(UNIQUE_TERMINATORS):
        raise ValueError(
            f"At most {len(UNIQUE_TERMINATORS)} sequences are supported in 'unique_terminal' mode."
        )

    processed: List[Tuple[str, str]] = []
    for idx, raw in enumerate(raw_sequences):
        seq = raw.strip()
        terminator = (
            UNIQUE_TERMINATORS[idx] if unique_terminal else DEFAULT_TERMINATOR
        )
        if terminator in seq:
            raise ValueError(
                f"Sequence {idx + 1} already contains the terminator '{terminator}'."
            )
        processed.append((seq, terminator))
    return processed


def build_suffix_tree(
    sequences: Sequence[Tuple[str, str]], include_terminal_suffix: bool = False
) -> nx.DiGraph:
    """Build a NetworkX `DiGraph` representing the suffix tree."""

    tree = nx.DiGraph()
    tree.add_node(0, depth=0, seqs=set())  # root

    for seq_index, (seq, terminator) in enumerate(sequences):
        seq_with_term = seq + terminator
        seq_number = seq_index + 1
        color = SEQUENCE_COLORS.get(seq_number)
        tree.nodes[0].setdefault("seqs", set()).add(seq_number)

        for i in range(len(seq_with_term)):
            suffix = seq_with_term[i:]
            if not include_terminal_suffix and len(suffix) == 1:
                continue

            current = 0
            parent_depth = tree.nodes[current].get("depth", 0)
            for char in suffix:
                next_node = None
                for neighbor in tree.successors(current):
                    if tree.edges[current, neighbor]["label"] == char:
                        next_node = neighbor
                        break
                if next_node is None:
                    next_node = len(tree.nodes)
                    new_depth = parent_depth + 1
                    tree.add_node(next_node, depth=new_depth, seqs={seq_number})
                    edge_attrs = {"label": char}
                    if color:
                        edge_attrs.update({"color": color, "fontcolor": color})
                    tree.add_edge(current, next_node, **edge_attrs)
                else:
                    new_depth = tree.nodes[current].get("depth", 0) + 1
                    node_attrs = tree.nodes[next_node]
                    node_attrs.setdefault("seqs", set()).add(seq_number)
                    node_attrs.setdefault("depth", new_depth)
                    if color:
                        edge_attrs = tree.edges[current, next_node]
                        edge_attrs.setdefault("color", color)
                        edge_attrs.setdefault("fontcolor", color)

                current = next_node
                parent_depth = tree.nodes[current].get("depth", parent_depth + 1)
                tree.nodes[current].setdefault("seqs", set()).add(seq_number)

            ends = tree.nodes[current].get("ends", [])
            ends.append((seq_number, i + 1))
            tree.nodes[current]["ends"] = ends

    return tree


def render_suffix_tree(
    tree: nx.DiGraph,
    out_path: str = "suffix_tree.dot",
    annotate_internal: bool = False,
    total_sequences: int = 1,
) -> str:
    """Write the graph in DOT format and return the resulting path."""

    lines: List[str] = []
    lines.append("digraph SuffixTree {")
    lines.append('  graph [rankdir=LR];')
    lines.append('  node [shape=point, label="", width=0.01, height=0.01, style=invis, penwidth=0];')
    lines.append('  edge [arrowhead=none];')

    edge_annotations: dict[tuple[int, int], List[str]] = {}
    node_xlabels: dict[int, str] = {}
    if annotate_internal:
        only_one_sequence = total_sequences == 1
        for node, attrs in tree.nodes(data=True):
            if tree.out_degree(node) < 2:
                continue
            seqs = sorted(set(attrs.get("seqs", set())))
            depth = attrs.get("depth")
            rows: List[str] = []
            if depth is not None:
                rows.append(
                    f'<TR><TD ALIGN="left"><FONT COLOR="purple">{depth}</FONT></TD></TR>'
                )
            if seqs and not only_one_sequence:
                if len(seqs) == 1:
                    seq = seqs[0]
                    color = SEQUENCE_COLORS.get(seq, "black")
                    rows.append(
                        f'<TR><TD ALIGN="left">'
                        f'<FONT COLOR="{color}">(</FONT>'
                        f'<FONT COLOR="{color}">{seq}</FONT>'
                        f'<FONT COLOR="{color}">)</FONT>'
                        f"</TD></TR>"
                    )
                else:
                    colorized_parts = [
                        f'<FONT COLOR="{SEQUENCE_COLORS.get(seq, "black")}">{seq}</FONT>'
                        for seq in seqs
                    ]
                    colorized = ",".join(colorized_parts)
                    rows.append(
                        f'<TR><TD ALIGN="left"><FONT COLOR="black">(</FONT>'
                        f"{colorized}"
                        f'<FONT COLOR="black">)</FONT></TD></TR>'
                    )
            if not rows:
                continue
            label_html = (
                "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\">"
                + "".join(rows)
                + "</TABLE>>"
            )
            preds = list(tree.predecessors(node))
            if preds:
                parent = preds[0]
                edge_annotations[(parent, node)] = [
                    f"headlabel={label_html}",
                    'labeldistance=0.2',
                    'labelangle=135',
                    'labelfontsize=10',
                ]
            else:
                node_xlabels[node] = label_html

    for u, v, data in tree.edges(data=True):
        label = data.get("label", "")
        color = data.get("color")
        fontcolor = data.get("fontcolor")
        safe_label = str(label).replace('"', '\\"')
        attrs = [f'label="{safe_label}"']
        if color:
            attrs.append(f'color="{color}"')
        if fontcolor:
            attrs.append(f'fontcolor="{fontcolor}"')
        extra = edge_annotations.get((u, v))
        if extra:
            attrs.extend(extra)
        lines.append(f'  {u} -> {v} [{", ".join(attrs)}];')

    for node, attrs in tree.nodes(data=True):
        ends = attrs.get("ends")
        if not ends:
            continue
        unique_ends = sorted(set(ends))
        rows_html: List[str] = []
        for seq_num, pos in unique_ends:
            color = SEQUENCE_COLORS.get(seq_num, "black")
            if total_sequences == 1:
                rows_html.append(
                    f'<TR><TD ALIGN="left"><FONT COLOR="{color}">{pos}</FONT></TD></TR>'
                )
            else:
                rows_html.append(
                    f'<TR><TD ALIGN="left"><FONT COLOR="{color}">{seq_num},{pos}</FONT></TD></TR>'
                )
        table_html = (
            "<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\">"
            + "".join(rows_html)
            + "</TABLE>>"
        )
        lines.append(
            f'  {node} [shape=plaintext, style="", label={table_html}, margin=0];'
        )

    for node, xlabel in node_xlabels.items():
        lines.append(f"  {node} [xlabel={xlabel}];")

    lines.append("}")
    with open(out_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    return os.path.abspath(out_path)


def dot_to_pdf(dot_path: str, pdf_path: str = "suffix_tree.pdf", open_viewer: bool = True) -> str:
    """Convert a DOT file to a PDF using Graphviz."""

    if shutil.which("dot") is None:
        raise RuntimeError("Graphviz 'dot' executable not found. Install Graphviz to produce the PDF.")

    subprocess.run(["dot", "-Tpdf", dot_path, "-o", pdf_path], check=True)
    if open_viewer:
        opener = shutil.which("xdg-open") or shutil.which("gio") or shutil.which("open")
        if opener:
            subprocess.Popen([opener, pdf_path])
    return os.path.abspath(pdf_path)


__all__ = [
    "DEFAULT_TERMINATOR",
    "UNIQUE_TERMINATORS",
    "SEQUENCE_COLORS",
    "process_sequences",
    "build_suffix_tree",
    "render_suffix_tree",
    "dot_to_pdf",
]
