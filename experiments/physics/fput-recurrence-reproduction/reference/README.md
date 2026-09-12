# LA-1940 Fig. 1 reference extraction

These are digitized values read from Fig. 1 of E. Fermi, J. Pasta, S. Ulam
(with M. Tsingou), *Studies of Nonlinear Problems, I*, LA-1940, report page
12 / PDF page 14. They are calibration evidence for comparison, never the
original numerical dataset.

## Source and credit

Source: [OSTI public copy](https://www.osti.gov/servlets/purl/4376203), DOI
[10.2172/4376203](https://doi.org/10.2172/4376203). The report is a US
Government work and the scan is public domain. Credit for the reproduced crop:
E. Fermi, J. Pasta, S. Ulam (with M. Tsingou), LANL/OSTI, LA-1940 (1955),
Fig. 1; crop prepared for this observatory experiment.

## Extraction method and uncertainty

The source PDF was fetched to a temporary path and verified against the data
manifest (1,570,076 bytes and the listed SHA-256). Ghostscript rendered PDF
page 14 at 150 dpi to a 1,272 × 1,659 RGBA PNG. The checked-in helper
[`extract_figure.sh`](extract_figure.sh) uses the same render settings and the
stdlib-only [`crop_png.py`](crop_png.py) helper to crop the plot and its axis
labels; the source PDF is never written into this repository.

For the full-page raster, the plot rectangle was calibrated at approximately
`left=306`, `right=1111`, `top=333`, `bottom=1219` pixels. The mappings were

```text
t_cycles   = (x - 306) / (1111 - 306) * 30,000
energy     = (1219 - y) / (1219 - 333) * 300
```

Curve centerlines were traced by eye on the high-contrast raster, using the
printed mode labels and following each line through overlaps. Grid and line
thickness give a stated digitization uncertainty of ±250 cycles and ±5 energy
units for individual points. The caption-level higher-mode statement is
recorded as a statement rather than treated as a trace. The values in
`fig1-digitized.csv` therefore remain approximate digitized features, not
measurements exported by the MANIAC calculation.

The crop is `la-1940-fig1.png` and is below the 400 kB repository limit.
