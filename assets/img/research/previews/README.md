# Compact website previews

These single-panel graphics use retained numerical data from the
[computed examples](../computed/README.md). They are previews for small cards;
the full multi-panel figures and their checks remain in that directory.

```shell
uv run --python 3.12 assets/img/research/previews/card_previews.py
uv run --python 3.12 assets/img/research/previews/card_previews.py --check
```

Plotting dependencies are pinned in the script. The manifest records hashes
of the source, numerical data and four SVG exports. The production build also
verifies that these bytes survive publication.

The layouts adapt the author's compact panel and explicit-reference conventions
from `structural_scores/illustrations/figure_style.py` and VBPCApy plotting
scripts. All plotted values come from the public synthetic examples. The
stochastic band shows pointwise variation across replicates. Costs are assumed;
nondominance uses the declared objectives. Reconstruction uses a supplied
component count. These are not additional application results.
