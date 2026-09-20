"""Order-book microstructure research: capture, reconstruction, features, horizon analysis.

The modules here test one falsifiable claim: that the visible level-2 book carries information
about short-horizon mid-price returns that survives realistic execution cost. Nothing in this
package places orders.
"""

from __future__ import annotations

__all__ = [
    "book",
    "features",
    "horizon",
    "labels",
    "pipeline",
    "record",
]
