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

## High-dpi label check (2026-09-12, repair)

The first digitization (above) traced curves "by eye" at 150 dpi without
reading the printed mode numerals painted on each peak, and assigned three of
them to the wrong mode. The repair re-renders PDF page 14 with Ghostscript at
300 dpi (`gs -q -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -r300
-dFirstPage=14 -dLastPage=14 -sOutputFile=page-14-300.png la-1940.pdf`,
`la-1940.pdf` fetched and SHA-256-verified per the data manifest, never
tracked) and crops the plot with `crop_png.py` using the same rectangle
convention as `extract_figure.sh`, scaled to the new dpi:

```text
scale      = dpi / 150
left, right, top, bottom = 306*scale, 1111*scale, 333*scale, 1219*scale
t_cycles   = (x - left) / (right - left) * 30,000
energy     = (bottom - y) / (bottom - top) * 300
```

At 300 dpi the rectangle is `left=612, right=2222, top=666, bottom=2438`
pixels. Three crops from this render are checked in as review evidence:

- `fig1-hidpi-full.png` — the whole plot, axes included.
- `fig1-hidpi-detail-mode2345.png` — cycles ≈0–10k, showing the printed "2"
  (early bump), "5", "4" and "3" numerals in sequence.
- `fig1-hidpi-detail-mode234.png` — cycles ≈13–23k, showing the printed "2"
  on the tallest non-mode-1 peak and the printed "3" on the peak that follows
  it.

**Rule followed:** each curve's mode number was read from its own printed
numeral wherever one is legible, confirmed by tracing the curve's continuity
back to an unambiguous anchor (t=0, where only mode 1 is nonzero). The
reconstruction's own simulated curves were never consulted to assign a label
— using them would make the check circular. This matches report p. 7's
description of the energy exchange ("mode 2 ... becomes predominant. At one
time, it has more energy than all the others put together! Then mode 3
undertakes this role"), which independently identifies the ≈265-unit peak
near 14k cycles as mode 2 and the ≈193-unit peak near 19k cycles as mode 3.

| feature | printed numeral | approx. (t_cycles, energy_units) |
|---|---|---|
| mode-2 early bump | "2" | (2,500, 40) |
| mode-5 first maximum | "5" | (5,000, 60) |
| mode-4 first maximum | "4" | (6,500, 135) |
| mode-3 first maximum | "3" | (9,400, 210) — unchanged from the first pass |
| mode-2 first maximum | "2" | (14,000, 265) |
| mode-3 second maximum | "3" | (19,000, 193) |
| mode-4 second maximum | "4" | (22,000, 110) |
| mode-1 minimum | none legible; continuity from t=0 along the smoothest, least-cusped curve | (19,000, 30) |
| mode-1 initial value / recurrence | obvious from t=0 continuity | (0, 300) / (28,600, 290) |

The curve that dips to ≈0 near 7.3k cycles in the first digitization is a
different mode's curve crossing near zero, not mode 1's; mode 1 remains well
above zero through the 6k–22k exchange window and only comes down to its own
minimum near 19k–20k cycles, where no numeral is legible and the reading
rests on continuity alone (flagged in the table above and carrying wider
uncertainty, see below).

### Uncertainty (repair)

Rectangle calibration is unchanged from the first pass and is stated there as
"approximately" located; comparing independently-derived pixel positions
against round tick marks across this repair suggests the effective
calibration uncertainty is closer to ±1,000 cycles and ±10 energy units than
the originally stated ±250/±5 for individual major-peak reads, and wider
still (~±1,500 cycles, ~±15 units) for the mode-1 minimum, which has no
printed numeral to anchor it. `fput/compare.py` still reports the tighter
±250 cycles / ±5 units figure for the plotted error bars; treat the values in
this section as the more honest bound for the newly-added and re-measured
rows.

### Changelog

- 2026-09-12 (repair, this task): corrected three mislabeled peaks —
  the 6.5k/135 peak is mode 4, not mode 2; the 14.0k/265 peak is mode 2, not
  mode 4; the 19.0k/193 peak is mode 3's second maximum, not mode 5's first
  maximum. Added previously-missing rows: mode 5's first maximum (5.0k/60),
  mode 2's early bump (2.5k/40), and mode 4's second maximum (22k/110).
  Re-measured the mode-1 minimum: the earlier 7,200-cycle/2-unit dip belonged
  to a different curve; mode 1's own minimum is near 19k–20k cycles and does
  not reach zero. Mode-3's first maximum (9.4k/210) and mode-1's initial and
  recurrence values were re-checked and are unchanged. Superseded by protocol
  `v2` (`../protocol/v2.md`); `v1` stays frozen and describes the pre-repair
  reading.
