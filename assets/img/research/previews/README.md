# Compact website previews

These single-panel graphics use retained numerical data from the
[computed examples](../computed/README.md) and the imported public op_infer
fixture. They are previews for small cards; the full figures and their checks
remain in the computed directory.

```shell
uv run --python 3.12 assets/img/research/previews/card_previews.py
uv run --python 3.12 assets/img/research/previews/card_previews.py --check
```

Plotting dependencies are pinned in the script. The manifest records hashes
of the source, both numerical inputs and five SVG exports. The production build also
verifies that these bytes survive publication.

The layouts adapt the author's compact panel and explicit-reference conventions
from `structural_scores/illustrations/figure_style.py` and VBPCApy plotting
scripts. All plotted values come from the public synthetic examples. The
stochastic band shows pointwise variation across replicates. Costs are assumed;
nondominance uses the declared objectives. Reconstruction uses a supplied
component count. These are not additional application results.
The op_infer preview shows a 64-replicate SBC histogram; it is deliberately
underpowered and is not evidence that inference is calibrated.
