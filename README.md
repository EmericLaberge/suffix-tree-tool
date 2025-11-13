# suffix-tree-tool

Outil en ligne de commande et bibliothèque Python pour construire, annoter et rendre des arbres des suffixes généralisés. Le projet accepte jusqu'à cinq séquences, colore les arêtes par séquence et génère un rendu DOT/PDF prêt à être inclus dans des documents.

## Installation

Depuis un répertoire cloné :

```bash
pip install .
```

Ou directement depuis Git (une fois le dépôt public) :

```bash
pip install git+https://github.com/EmericLaberge/suffix-tree-tool.git
```

## Utilisation

```bash
generate-suffix-tree agacagg ggacaga --annotate-internal --unique-terminal
```

Options principales :

- ``--include-terminal`` : conserve le suffixe constitué uniquement du terminateur.
- ``--unique-terminal`` : attribue un terminateur distinct à chaque séquence.
- ``--annotate-internal`` : ajoute les profondeurs et indices de séquences sur les nœuds internes.

Le rendu génère deux fichiers dans le répertoire courant :

- ``suffix_tree.dot``
- ``suffix_tree.pdf`` (si Graphviz est disponible)

## API Python

```python
from suffix_tree_tool import process_sequences, build_suffix_tree, render_suffix_tree
```

## Licence

Distribué sous licence MIT (voir ``LICENSE`` pour plus d’informations). Pour toute question ou contribution, écrivez à ``emeric.laberge@umontreal.ca``.
