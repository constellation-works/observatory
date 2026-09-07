# ROGII Wellbore Geology Prediction — data dictionary

This directory contains the files supplied for the
[ROGII — Wellbore Geology Prediction](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/data)
competition. The definitions below combine Kaggle's data description, the
organizer-provided `AI_wellbore_geology_prediction_task_en.pptx`, and checks of
the downloaded CSV files.

## What one example represents

The unit of modeling is a **horizontal well**, identified by an 8-character
hash such as `000d7d20`. The hash is stored in the filenames, not in a CSV
column. Each well has two related sequences:

1. The **horizontal-well sequence** follows the drilled path in 1-foot steps of
   measured depth (`MD`). It contains the trajectory, its gamma-ray log, known
   `TVT` values before the prediction start, and a suffix whose `TVT` must be
   predicted.
2. The **typewell sequence** is the vertical reference log assigned to that
   horizontal well. It supplies a complete gamma-ray signature indexed by
   known `TVT`, so the horizontal log can be correlated to a geological
   vertical position.

The modeling goal is to infer the horizontal well's `TVT` after the prediction
start by combining its path and gamma-ray sequence with the typewell reference.
Along increasing `MD`, `TVT` may increase, decrease, or remain nearly constant,
depending on the well path and the dip or structure of the rock layers.

## Directory and file layout

| Path or pattern | Contents |
| --- | --- |
| `train/{WELLNAME}__horizontal_well.csv` | Complete horizontal-well target plus the partially masked input target. |
| `train/{WELLNAME}__typewell.csv` | The corresponding vertical reference log and training-only geology labels. |
| `train/{WELLNAME}.png` | Organizer visualization of the well path and geological cross-section; it has no tabular columns. |
| `test/{WELLNAME}__horizontal_well.csv` | Authoring-test trajectory, gamma ray, and partially observed `TVT_input`; ground-truth `TVT` is omitted. |
| `test/{WELLNAME}__typewell.csv` | Authoring-test vertical reference; `Geology` is omitted. |
| `sample_submission.csv` | One output row for every masked authoring-test row. |
| `AI_wellbore_geology_prediction_task_en.pptx` | Organizer explanation and diagrams. |

The three visible test wells are examples copied from the training set. Kaggle
replaces them with roughly 200 hidden wells when it reruns a submitted
notebook. They are useful for testing inference and submission generation, but
they are not an independent validation set.

## Three coordinates that should not be confused

All distance and coordinate columns are in **feet**.

| Column | Coordinate meaning |
| --- | --- |
| `MD` | Measured depth: distance traveled along the wellbore from the surface. It is path length, not vertical depth. |
| `Z` | The vertical coordinate of the physical well path relative to sea level. Values in this release are negative, so a more negative value is deeper in the dataset's coordinate convention. |
| `TVT` | True Vertical Thickness, used here as a geological vertical coordinate. It locates the rock encountered by the horizontal well on the typewell's geological/depth axis; it is the prediction target, not another copy of `Z`. |

The typewell's `TVT` is ordered down the vertical reference log. The horizontal
well's `TVT` is a mapping from each path sample to that reference axis and does
not have to be monotonic as `MD` increases.

## Horizontal-well columns

### `MD`

- **Meaning:** Measured Depth, the cumulative distance along the drilled
  wellbore from the surface to the sample point.
- **Type/unit:** Floating point, feet.
- **Availability:** Train and test.
- **Observed behavior:** Consecutive rows are spaced exactly 1 foot apart in
  all downloaded training wells. CSV row order therefore follows drilling/path
  order.
- **Modeling note:** Differences and rolling windows along `MD` describe local
  path/log behavior. Do not interpret `MD` as vertical depth.

### `X`

- **Meaning:** Easting, the first horizontal spatial coordinate of the sampled
  point on the well path.
- **Type/unit:** Floating point, feet.
- **Availability:** Train and test.
- **Modeling note:** Together with `Y`, it defines map position, well azimuth,
  distance traveled horizontally, and proximity to offset wells. The
  competition does not publish a coordinate reference system or datum, so use
  these as projected/local coordinates rather than converting them to
  latitude/longitude.

### `Y`

- **Meaning:** Northing, the second horizontal spatial coordinate of the
  sampled point on the well path.
- **Type/unit:** Floating point, feet.
- **Availability:** Train and test.
- **Modeling note:** Use with `X` to derive direction, curvature, relative
  location, and neighboring-well features. Geological dip can behave similarly
  in spatially nearby wells, and drilling azimuth affects how that dip is
  encountered.

### `Z`

- **Meaning:** True vertical depth/elevation coordinate of the physical
  wellbore point relative to sea level.
- **Type/unit:** Floating point, feet.
- **Availability:** Train and test.
- **Observed convention:** Values are negative in the downloaded data
  (`-11,027.65` to `-7,174.22` in training). More-negative `Z` is deeper.
- **Modeling note:** `Z` describes the borehole trajectory. `TVT` describes the
  geological position assigned to that trajectory point; their difference and
  slopes need not be constant.

### `ANCC`, `ASTNU`, `ASTNL`, `EGFDU`, `EGFDL`, `BUDA`

- **Meaning:** Predicted `Z`/depth of six geological formation tops at the
  horizontal location of each trajectory sample. These columns describe
  geological surfaces, not the well path itself.
- **Type/unit:** Floating point, feet, using the same negative-depth convention
  as `Z`.
- **Availability:** **Training only. They do not appear in test horizontal-well
  files, including the visible authoring examples.**
- **Ordering:** Wherever all six values are present, every downloaded training
  row has the shallow-to-deep order
  `ANCC > ASTNU > ASTNL > EGFDU > EGFDL > BUDA`; “greater” means shallower here
  because the depths are negative.
- **Missingness:** `ANCC` is missing in 45,634 rows (0.90%, seven wells), and
  `EGFDL` is missing in 6,067 rows (0.12%, one well). The other four are
  complete in the downloaded training data.
- **Naming caution:** The official materials use these marker codes but do not
  provide authoritative long-form expansions. Keep the codes as supplied
  instead of assigning guessed formation names.
- **Modeling note:** A production inference model cannot require these columns.
  They may still be useful as training-only auxiliary targets, for analysis,
  or for designing features that can also be constructed without them at
  inference time.

### `TVT`

- **Meaning:** Manually interpreted True Vertical Thickness/geological
  position of the rock encountered at the horizontal-well row.
- **Type/unit:** Floating point, feet.
- **Availability:** **Training horizontal-well files only.** It is present for
  every training row and omitted from test horizontal-well files.
- **Role:** Ground-truth regression target. Kaggle computes RMSE between this
  value and submitted `tvt` values for the hidden evaluation rows.
- **Modeling note:** Although the typewell also has a `TVT` column, the two
  columns play different roles: the typewell column is the known reference
  axis; the horizontal-well column is the unknown mapping onto that axis.

### `GR`

- **Meaning:** Gamma-ray log measured at the horizontal-well sample. It records
  natural radioactivity and acts as a rock-character signature. Matching the
  shape of horizontal and typewell `GR` sequences is central to geological
  correlation.
- **Type/unit:** Floating point, API gamma-ray units.
- **Availability:** Train and test.
- **Missingness:** Missing in 1,507,972 of 5,092,255 training rows (29.61%) and
  3,784 of 19,221 visible test rows (19.69%). Every downloaded training well
  contains at least one missing horizontal `GR` value.
- **Modeling note:** Missing spans require an explicit strategy. Preserve a
  missingness indicator and avoid allowing interpolation or rolling features
  to see across a validation mask in a way that would be unavailable at
  inference time. A high or low `GR` value is a signal, not by itself a
  definitive geology label.

### `TVT_input`

- **Meaning:** The observed portion of the horizontal well's target. It is an
  exact copy of `TVT` from the first row through the row immediately before the
  Prediction Start (`PS`), then `NaN` from `PS` through the end of the well.
- **Type/unit:** Floating point, feet.
- **Availability:** Train and test.
- **Observed behavior:** All 773 training wells have exactly one known-to-missing
  transition, and the missing interval always continues to the final row.
  Every non-missing training value matches `TVT` exactly. The masked suffix is
  3,783,989 rows, or 74.31% of training horizontal-well rows.
- **Modeling note:** This is legitimate inference-time context: the final known
  value, local trend, and pre-PS horizontal `GR`/`TVT` correlation can anchor
  the prediction. It is also the main leakage risk. During validation, create
  a synthetic PS boundary and mask `TVT_input` for the full validation suffix
  before deriving any feature.

## Typewell columns

Each horizontal well has one assigned typewell. The typewell is a vertical
reference sequence; its `TVT` and `GR` remain known through the full depth
range.

### `TVT` (typewell)

- **Meaning:** Known vertical depth/geological index of the typewell gamma-ray
  sample. It is the reference axis onto which the horizontal-well `GR` must be
  correlated.
- **Type/unit:** Floating point, feet.
- **Availability:** Train and test typewell files; no missing values were found.
- **Sampling:** The grid is not globally uniform. Common adjacent increments
  are 0.5, 0.25, 0.1, and 1.0 feet, so code should read the actual values rather
  than assume a fixed typewell step.

### `GR` (typewell)

- **Meaning:** Gamma-ray measurement along the vertical reference log at the
  corresponding typewell `TVT`.
- **Type/unit:** Floating point, API gamma-ray units.
- **Availability:** Train and test typewell files; no missing values were found
  in the downloaded data.
- **Modeling note:** Compare patterns or learned representations of this series
  with the horizontal-well `GR` series. Alignment generally needs to tolerate
  different sampling grids, noise, missing horizontal measurements, and
  stretches where the horizontal `TVT` reverses or remains flat.

### `Geology`

- **Meaning:** Categorical geological-unit/interval label assigned along the
  training typewell.
- **Type:** String/category.
- **Availability:** **Training typewell files only; the column is absent from
  test typewell files.**
- **Missingness:** Missing in 523,474 of 1,567,045 training typewell rows
  (33.41%). A missing value means no label is supplied for that depth; it should
  not be silently treated as a new physical formation without testing that
  choice.
- **Observed labels:** There are 43 non-null strings in this release. Frequent
  labels include `ANCC`, `EGFDL`, `ASTNL`, `BUDA`, `ASTNU`, and `EGFDU`; the
  full set also includes interval/marker codes such as `OLMOS`, `MNSS`,
  `EGFD300`, `UEGFD TGT`, and `Clay Rich Interval`.
- **Modeling note:** Like the six formation-surface columns, `Geology` cannot be
  used as a required test-time feature. It can support training-only analysis,
  auxiliary supervision, or interpretation of gamma-ray signatures.

## Submission columns

### `id`

- **Meaning:** Unique prediction-point identifier formatted as
  `{WELLNAME}_{row_index}`.
- **Type:** String.
- **Row index convention:** `row_index` is the zero-based data-row position in
  that well's horizontal CSV (the header is not counted). In the visible test
  data, the IDs exactly match the rows where `TVT_input` is `NaN`.
- **Requirement:** Preserve the sample submission's IDs and order unless the
  submission generator explicitly validates an equivalent ordering.

### `tvt`

- **Meaning:** Predicted horizontal-well `TVT` for the corresponding `id`.
- **Type/unit:** Floating point, feet.
- **Requirement:** The header is lower-case `tvt`, even though source CSVs use
  upper-case `TVT`. Kaggle requires the output filename `submission.csv`.

## Local data snapshot

These counts describe the downloaded authoring package, not Kaggle's hidden
rerun data:

| Partition | Files/wells | Rows | Notable missingness |
| --- | ---: | ---: | --- |
| Train horizontal wells | 773 wells | 5,092,255 | `GR` 29.61%; `TVT_input` 74.31%; `ANCC` 0.90%; `EGFDL` 0.12% |
| Train typewells | 773 wells | 1,567,045 | `Geology` 33.41%; `TVT` and `GR` complete |
| Visible test horizontal wells | 3 wells | 19,221 | `GR` 19.69%; `TVT_input` 73.62% |
| Visible test typewells | 3 wells | 5,798 | `TVT` and `GR` complete |
| Sample submission | 3 wells | 14,151 | One row per missing visible-test `TVT_input` |

## Leakage and validation checklist

- Split validation by `WELLNAME`; adjacent one-foot samples from the same well
  are strongly dependent.
- Reproduce the test setup by choosing a Prediction Start within each
  validation well and masking `TVT_input` from that row to the end.
- Compute RMSE only on the synthetic masked suffix.
- Fit imputers, scalers, spatial-neighbor searches, templates, and learned
  gamma-ray correlations without exposing the validation well's hidden `TVT`.
- Do not require `TVT`, the six formation surfaces, or typewell `Geology` at
  inference time: they are absent from hidden test inputs.
- Do not treat the three visible test wells as an independent holdout; Kaggle
  identifies them as training examples supplied for authoring submissions.
