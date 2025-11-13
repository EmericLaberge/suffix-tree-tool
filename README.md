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

```bash
generate-suffix-tree agacagg ggacaga acacac --annotate-internal --unique-terminal
```

Key options:

- `--include-terminal`: keep the suffix that contains only the terminator.
- `--unique-terminal`: assign a distinct terminator to each sequence.
- `--annotate-internal`: display depth and sequence indices on internal nodes.

The renderer writes two files in the current directory:

- `suffix_tree.dot`
- `suffix_tree.pdf` (when Graphviz is available)

## Python API

```python
from suffix_tree_tool import process_sequences, build_suffix_tree, render_suffix_tree
```

## License

Distributed under the MIT License (see `LICENSE` for details). For questions or contributions, email `emeric.laberge@umontreal.ca`.
