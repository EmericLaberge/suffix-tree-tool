# suffix-tree-tool

Command-line tool and Python library for building, annotating, and rendering generalized suffix trees. The project accepts up to five sequences, colors edges per sequence, and produces DOT/PDF output that is ready to embed in documents.

## Installation

From PyPI:

```bash
pip install suffix-tree-tool
```

From a cloned repository:

```bash
pip install .
```

Or directly from Git (once the repository is public):

```bash
pip install git+https://github.com/EmericLaberge/suffix-tree-tool.git
```

## Usage

Single-sequence example:

```bash
generate-suffix-tree gatgaatgg
```

![Suffix tree rendering for a single sequence](examples/single_seq_tree.png)

Multi-sequence example with internal annotations:

```bash
generate-suffix-tree gatgaatgg ggtaagtag --annotate-internal
```

![Suffix tree rendering for multiple sequences](examples/multi_seq_tree.png)

Key options:

- `--include-terminal`: keep the suffix that contains only the terminator.
- `--unique-terminal`: assign a distinct terminator to each sequence.
- `--annotate-internal`: display depth and sequence indices on internal nodes.

The renderer writes two files in the current directory:

- `suffix_tree.dot`
- `suffix_tree.pdf` (when Graphviz is available)

Rendered screenshots are available under `examples/`.

## Python API

```python
from suffix_tree_tool import process_sequences, build_suffix_tree, render_suffix_tree
```

## License

Distributed under the MIT License (see `LICENSE` for details). For questions or contributions, email `emeric.laberge@umontreal.ca`.
