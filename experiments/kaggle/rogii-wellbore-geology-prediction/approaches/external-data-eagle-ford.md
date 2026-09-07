# External data scouting — Eagle Ford / ROGII Wellbore Geology Prediction

Scouting report, 2026-07-16. Competition rules allow freely & publicly available external
data (incl. pre-trained models) mounted as offline Kaggle datasets. Key constraint driving
every verdict: **competition X,Y are de-identified/local**, so geo-registration to real-world
maps is almost certainly impossible — *regional statistics and pretraining transfer; exact
surfaces don't.*

## Summary verdict

- **Best bet: pretrain a GR/log encoder on large public LAS corpora** — FORCE 2020 (Zenodo,
  NOLD 2.0, already mirrored on Kaggle) + Kansas Geological Survey LAS (free bulk, tens of
  thousands of wells, GR nearly universal). Volve/NLOG/Australia as optional volume.
- **Second: distill regional *statistics* as priors, not surfaces** — EIA Eagle Ford
  structure/isopach shapefiles and the USGS 2018 assessment give defensible priors for
  regional dip (~gentle SE dip, tens of ft/mi), Eagle Ford thickness (~50–400 ft), and
  layer-ordering/thickness ratios (Buda → EGFD L/U → Austin Chalk → Anacacho).
- **Texas RRC is a dead end for logs at scale**: logs are per-well scanned TIFF/PDF images
  behind query UIs; bulk downloads cover production/permits/GIS only, no LAS corpus.
- **No pre-existing "Eagle Ford LAS" Kaggle dataset exists**; the useful Kaggle-hosted items
  are FORCE 2020 mirrors and small Volve extracts. Plan on building and uploading our own
  curated external dataset(s).
- **Public geosteering datasets: essentially none besides this competition itself** — the
  ROGII data *is* the public benchmark; community toolkit repos exist on GitHub.

---

## 1. Texas Railroad Commission (RRC) — verdict: **skip** (marginal at best)

What exists:

- **Imaged well records 1981–present** (completion packets W-2/G-1, drilling permits W-1,
  plugging reports, directional surveys as attachments) via the
  [Oil and Gas Imaged Records Query](https://www.rrc.texas.gov/oil-and-gas/research-and-statistics/obtaining-commission-records/oil-and-gas-well-records-online/).
  Delivered as **per-lease PDF bundles**; "oversized" documents — which is where **electric
  logs** live — come as **scanned TIFF images**.
- **Well Log (WL) profile**: images of all well logs received since **July 2004**, searchable
  by API/county/field via the
  [well records pages](https://www.rrc.texas.gov/oil-and-gas/research-and-statistics/obtaining-commission-records/oil-and-gas-well-records/)
  and the Public GIS Viewer / Wellbore Query
  ([GIS well logs page](https://www.rrc.texas.gov/oil-and-gas/research-and-statistics/obtaining-commission-records/oil-gas-well-records-gis-well-logs/)).
  Since a 2018 notice
  ([Notice to Operators — digital well logs](https://www.rrc.texas.gov/media/dkihm5zh/notice-to-operators-digital-well-logs.pdf))
  operators *file* both .LAS and .TIFF, but **public delivery is TIFF images**, per-well.
- **[Bulk "Data Sets Available for Download"](https://www.rrc.texas.gov/resource-center/research/data-sets-available-for-download/)**:
  drilling permits, production, field data, injection, GIS well/survey layers (statewide API
  lists, surface/bottomhole locations). **No log curves, no LAS, no digital tops.**

Mechanics: per-well/per-lease manual queries (or scripted scraping of the query apps);
TIFF rasters would need log digitization (e.g., raster-to-LAS) at scale — a project in
itself, and the RRC terms around scraping are untested.

Use-case fit: thousands of real Eagle Ford GR logs *do* sit here, but as raster scans behind
per-well queries. For a Kaggle timeline the extraction cost dwarfs the benefit, and
de-identified coordinates kill the location-matching upside. **Skip.**

## 2. USGS sources — verdict: **marginal** (one narrow win: assessment stats)

- **[Core Research Center well catalog](https://my.usgs.gov/crcwc/)**
  ([overview](https://www.usgs.gov/core-research-center/wells)): searchable catalog of cores
  and cuttings with some **downloadable LAS** per well ("download all" zips per category).
  Holdings are Denver-repository, Rocky-Mountain-heavy; Texas/Eagle Ford coverage sparse.
  Free/public domain. *Marginal* — a minor top-up for a pretraining corpus, not a pillar.
- **NGGDPP well log data** ([program page](https://www.usgs.gov/programs/national-geological-and-geophysical-data-preservation-program/well-log-data),
  [LAS format notes](https://www.usgs.gov/programs/national-geological-and-geophysical-data-preservation-program/las-format)):
  pointers to state-survey digitization efforts; useful as a directory, not a dataset.
- **Eagle Ford 2018 assessment** —
  [Fact Sheet 2018-3033](https://pubs.usgs.gov/publication/fs20183033),
  [AU boundaries + input-data forms (ScienceBase)](https://www.sciencebase.gov/catalog/item/5d1246c2e4b0941bde56e84f),
  [EUR data release](https://www.usgs.gov/data/estimated-ultimate-recoveries-oil-wells-eagle-ford-group-and-associated-cenomanian-turonian),
  and the digested [AAPG Wiki write-up](https://wiki.aapg.org/Eagle_Ford_Group_in_southwest_Texas_(USGS)).
  Small (MBs), public domain, shapefiles/CSV/PDF. **Win**: numeric priors on thickness,
  depth ranges, and stratigraphic framework of BUDA/EGFD/ASTN per assessment unit.
- **[National Produced Waters Geochemical Database](https://www.sciencebase.gov/catalog/item/59d25d63e4b05fe04cc235f9)**
  (v2.3; superseded by v3.0, doi:10.5066/P9DSRCZJ): ~115k samples, CSV/XLSX, 190 variables
  incl. **formation name + depth + lat/lon**. Public domain, one-click download (~tens of MB).
  Could yield coarse formation-depth statistics for Eagle Ford/Austin Chalk/Buda, but no GR.
  *Marginal.*
- No USGS COSUNA-style public formation-tops-per-well database for the Texas Gulf Coast was
  found; tops compilations behind USGS/EIA maps derive from commercial data (Enverus) and are
  released only as contoured products.

## 3. Texas state / academic sources — verdict: **marginal / mostly skip**

- **TWDB BRACS** ([well logs page](https://www.twdb.texas.gov/groundwater/bracs/WellLogs.asp),
  [GIS data](https://www.twdb.texas.gov/groundwater/bracs/GISdata.asp),
  [studies](https://www.twdb.texas.gov/groundwater/bracs/studies.asp)): large digitized
  geophysical-log holdings organized by county, but distribution is **by email request /
  shipped drive** for logs (some direct weblinks); the downloadable GIS packages carry
  **formation tops for aquifer units** (Carrizo-Wilcox, Queen City, etc.) — i.e., the
  *shallow* section, generally above the Buda/Eagle Ford interval of interest. Access model
  is awkward for Kaggle and the stratigraphic window is wrong. **Skip** (revisit only if we
  want extra Texas GR for pretraining and the county weblinks pan out).
- **BEG / TexNet-CISR**: the BEG built a 13,000-well 3D structural framework of the Eagle
  Ford for induced-seismicity work ([Eagle Ford fault maps page](https://www.beg.utexas.edu/texnet-cisr/fault-maps/eagle-ford)),
  but only the **fault shapefiles** are public —
  [McKeighan et al. 2022, Texas Data Repository, CC0](https://dataverse.tdl.org/dataset.xhtml?persistentId=doi:10.18738/T8/TOPKV4)
  (280 KB zip; fault traces + slip-potential attributes; no horizons/tops). STARR has no
  public tops database. TexNet earthquake catalog is public but irrelevant here. **Marginal**
  — fault-density/orientation stats could inform how often laterals cross faults, nothing more.
- **TNRIS/TxGIO** outcrop/elevation data (used in EIA maps) — only relevant for
  geo-registered work. **Skip.**

## 4. Large public LAS / well-log corpora (pretraining) — verdict: **worth pursuing (primary)**

| Corpus | Size / format | GR? | License / access |
|---|---|---|---|
| **[FORCE 2020 lithofacies](https://zenodo.org/records/4351156)** ([GitHub](https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition)) | 118 wells, Norwegian shelf; CSV (+LAS), ~1–2 GB total | Yes + full log suites + **lithofacies labels** + formation tops | **NOLD 2.0** (open, attribution); direct Zenodo download |
| **[Kansas Geological Survey LAS](https://www.kgs.ku.edu/Magellan/Logs/)** | Tens of thousands of wells; LAS 2.0/3.0; **pre-built bulk ZIP index** + per-well HTTP | GR nearly universal; many with tops in KGS DB | Free public data, no registration; scripted bulk download is straightforward |
| **[Equinor Volve](https://www.equinor.com/energy/volve-data-sharing)** | ~40,000 files (~5 GB relevant logs; full set much larger); LAS/DLIS | Yes (24 wells, full petrophysics + drilling/LWD) | Equinor Open Data Licence (CC-BY-style, some resale restrictions) |
| **[SPWLA PDDA ML contests](https://github.com/pddasig/Machine-Learning-Competition-2020)** ([2021](https://github.com/pddasig/Machine-Learning-Competition-2021)) | Small (a few wells, CSV) — Volve-derived | Yes | Open on GitHub; tiny, useful as sanity benchmarks only |
| **[NLOG (Netherlands)](https://www.nlog.nl/en)** | Thousands of released wells; LAS + petrophysical reports, bulk-ish | Yes | Free government open data |
| **[Geoscience Australia / WAPIMS](https://www.andymcdonald.scot/data/geoscience-australia)** | Very large (onshore+offshore Australia); LAS | Yes | Free, per-well portal downloads |
| **[Utah FORGE / DOE GDR](https://www.andymcdonald.scot/data/gdr-openei)** | Geothermal wells, LAS + full suites | Yes | Public domain (DOE) |
| North Dakota DMR | Large LAS holdings | Yes | **Subscription ($) — skip** |

(Good living directory of all of the above: [Andy McDonald's Open Well Data Sources](https://www.andymcdonald.scot/data/).)

Use-case fit: this is the highest-leverage external data. A self-supervised GR-sequence
encoder (masked reconstruction / contrastive on depth windows) pretrained on KGS + FORCE +
Volve transfers to the competition's GR correlation task regardless of basin; FORCE also
supports supervised facies/formation-boundary pretext tasks. All licenses are compatible
with an offline Kaggle dataset upload with attribution. **Practical plan:** curate to
GR + MD/TVD + tops, resample, and package as one 1–5 GB Kaggle dataset.

## 5. Existing Kaggle datasets — verdict: **marginal (convenient mirrors only)**

Searched kaggle.com/datasets; **no Eagle Ford well-log/LAS dataset exists**. What's there:

- [Well logs dataset for machine learning (faresazzam)](https://www.kaggle.com/datasets/faresazzam/well-logs-dataset-for-machine-learning/data) — a **FORCE 2020 mirror** (easiest one-click attach).
- [Volve production data](https://www.kaggle.com/datasets/lamyalbert/volve-production-data),
  [Volve well F-9A drilling data](https://www.kaggle.com/datasets/imranulhaquenoor/volve-dataset-well-f-9-a),
  [wells from Volve oil field](https://www.kaggle.com/datasets/youcefziat/wells-from-volve-oil-field) — partial Volve extracts.
- Generic small sets: [well log facies](https://www.kaggle.com/datasets/imeintanis/well-log-facies-dataset),
  [well logs (sahasourav17)](https://www.kaggle.com/datasets/sahasourav17/well-logs),
  [well log data (prateekvyas)](https://www.kaggle.com/datasets/prateekvyas/well-log-data).

Use-case fit: attach the FORCE mirror for zero-effort experiments; for anything serious,
upload our own curated corpus (also avoids provenance/version doubts in mirrors). Related
find (code, not data): [mycarta/rogii-geosteering-toolkit](https://github.com/mycarta/rogii-geosteering-toolkit),
a community toolkit for this exact competition.

## 6. Published Eagle Ford structure / isopach maps — verdict: **marginal (extract scalar priors, don't digitize surfaces)**

- **EIA Eagle Ford play maps** — [play report PDF (2014)](https://www.eia.gov/maps/pdf/eagleford122914.pdf)
  and, crucially, **"Eagle Ford play boundaries, structure and isopachs (3/11/2016) —
  Shapefile"** on the [EIA maps page](https://www.eia.gov/maps/maps.htm); the isopach layer is
  also on the [US Energy Atlas](https://atlas.eia.gov/datasets/8209a93a3e9b4d09b14702e5986ad5d9_0/about)
  with shapefile/GeoJSON/CSV export. Public domain, small (MBs). Contours of top-of-Eagle-Ford
  elevation and thickness (built from commercial well data + USGS/BEG/TNRIS sources).
- **USGS FS 2018-3033** figures and the [AAPG Wiki version](https://wiki.aapg.org/Eagle_Ford_Group_in_southwest_Texas_(USGS))
  (cross sections, AU maps, thickness ranges).
- BEG publications (Eagle Ford geology reports, Geologic Atlas of Texas sheets) are
  scanned-PDF products behind the BEG store/publication pages — digitizable but low value here.

Use-case fit: with de-identified competition coordinates the surfaces can't be registered, so
converting contours into a usable *prior* means reducing them to **distributions**: regional
dip magnitude/azimuth statistics over the play (structure contour spacing), EGFD gross
thickness (~50–400 ft) and its spatial variance, Austin Chalk/Buda relative spacing. That's a
few numbers/histograms, not a digitization project. Do the cheap version; skip full-map
digitization.

---

## Recommended actions (priority order)

1. Build one curated Kaggle dataset: **KGS bulk LAS (GR+tops subset) + FORCE 2020 + Volve
   petrophysical LAS**, standardized to a common schema; pretrain a GR sequence encoder.
2. Attach the existing **FORCE 2020 Kaggle mirror** immediately for cheap ablations.
3. Pull the **EIA structure/isopach shapefiles + USGS FS 2018-3033** and distill dip/thickness
   priors (scalars + histograms) into the modeling notes; also grab per-formation GR character
   descriptions from the AAPG/USGS write-ups (Austin Chalk low-GR carbonate, Eagle Ford hot
   shale GR peak at base/EGFDL, Buda clean limestone) to sanity-check typewell labeling.
4. Skip RRC, BRACS, and CRC unless a specific gap emerges that only real Texas GR can fill.
