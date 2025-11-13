"""suffix_tree_tool - generalized suffix tree generation utilities."""

from .builder import (
    DEFAULT_TERMINATOR,
    UNIQUE_TERMINATORS,
    SEQUENCE_COLORS,
    build_suffix_tree,
    dot_to_pdf,
    process_sequences,
    render_suffix_tree,
)

__all__ = [
    "DEFAULT_TERMINATOR",
    "UNIQUE_TERMINATORS",
    "SEQUENCE_COLORS",
    "process_sequences",
    "build_suffix_tree",
    "render_suffix_tree",
    "dot_to_pdf",
]
