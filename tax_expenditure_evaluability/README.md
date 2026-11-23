# Evaluability of Tax Expenditures in Türkiye

Replication package for the article *"Evaluability of Tax Expenditures in Türkiye: An Assessment of Official
Reporting Against the IMF Evaluation Framework"* (manuscript: `paper/manuscript.md`).

The study codes the information in nine official Tax Expenditure Reports available for 2016–2018 and 2020–2025 (no 2019 report was found), plus the tax expenditure tables of the 2019 and 2020 budget laws, against nine criteria
derived from the IMF How-To Note 22/05 (Beer, Benedek, Erard & Loeprick, 2022). It measures **evaluability of the
reported information**, not the effects of any tax expenditure.

## Re-running

```bash
./run_all.sh
```

This needs Python 3 with `pandas`, `numpy`, `matplotlib`, `pymupdf`, `fonttools` and `tabulate`. The full run takes
about 40 seconds and is deterministic; a clean run from the raw files reproduces the committed outputs byte for byte (checked 23 Nov 2026). The 2018 glyph map is learned from the other reports' annexes, so `run_all.sh` extracts those first. `data/text/` (pdftotext output) and the hand-checked inputs (`data/interim/manual_rows_VHR2016.csv`, `data/interim/budget_law_annexes.csv`, `data/coding/overrides.csv`) are inputs, not outputs. Step 11 reads cached CrossRef records and goes online only if a record is missing.

## Layout

| Path | Content |
|---|---|
| `PROJECT_STATUS.md` | Feasibility report (Turkish) written before the analysis, plus the completion status |
| `data/source_inventory.csv` | Every source document: institution, title, type, years covered, URL, access date, local file |
| `data/raw/` | Downloaded PDFs (HMB 2007, 2016–2018; GİB 2020–2025; IMF note); `data/raw/budget_law/`: Official Gazette pages and scanned annexes of the 2019 and 2020 budget laws |
| `data/text/` | `pdftotext -layout` output of the PDFs |
| `data/tax_expenditure_panel.csv` | **Main panel**: report × item × year (10,560 rows): amount (thousand TL), cell status, realisation/projection, quality label, legal reference, PDF page, URL |
| `data/interim/` | Extracted annex rows and totals, body summary tables, narrative sections, item links, manual 2016 rows |
| `data/codebook.md` | Criteria, code values, decision rules, IMF mapping, coding procedure |
| `data/coding/` | Section codes with evidence sentences and pages, overrides, decision log, item and item-year codes, consecutive-report difference list |
| `data/literature/` | CrossRef records of all cited DOIs, verification table, literature log (basis of use per source) |
| `scripts/` | Pipeline (00–11), see below |
| `outputs/tables/` | All tables (CSV) and `tables.md`; reconciliation tables; documented inconsistencies in the official documents |
| `outputs/figures/` | Figures 1–4 (PNG, 300 dpi) |
| `paper/` | Manuscript, `references.bib` (generated from CrossRef), limitations and data gaps |

## Pipeline

| Script | Step |
|---|---|
| `00_decode_2018_glyphs.py` | Learns the glyph-to-character map for the 2018 annex fonts, which have no Unicode maps |
| `01_extract_annex_tables.py` | Extracts Annex I item rows and sub-table totals from each report (handles rotated pages and encodings) |
| `02_build_panel.py` | Normalises legal references, links items across reports and builds the long panel |
| `03_extract_summary_tables.py` | Extracts body tables: totals, % of GDP, % of tax revenue, budget-law estimates |
| `03b_budget_law_annexes.py` | Checks the transcribed budget-law annex tables (row sums) and compares them with the reports (same-vintage detection) |
| `04_reconcile.py` | Reconciles item rows with sub-table totals, and annex totals with body tables |
| `05_extract_narratives.py` | Splits the provisions chapter into numbered narrative sections, with page markers |
| `06_candidate_sentences.py` | Splits sentences and separates quoted statute from narrative |
| `07_code_sections.py` | Rule-based first-pass codes with evidence sentence and page |
| `08_finalize_section_codes.py` | Applies the coder's logged overrides and lists differences between consecutive reports |
| `09_item_codes.py` | Maps items to sections and derives C3/C4 for every item-year |
| `10_analysis.py` | Tables and figures |
| `11_verify_references.py` | Verifies DOIs at CrossRef and writes `paper/references.bib` |
| `12_number_trace.py` | Recomputes every number quoted in the manuscript from its table cell and checks it against the text (`outputs/tables/manuscript_number_trace.csv`) |
| `check_totals.py`, `diag_rows.py` | Diagnostic helpers used during extraction |

## Key conventions

* Amounts are thousand TL as printed, from static revenue-forgone estimates that assume no behavioural response. Nominal amounts are not compared across years; ratios are those published by the reports.
* "Realisation" means the report's estimate for the latest year with data (the first annex column). "Projection" means the following four years.
* Codes: 2 = explicit and provision-specific; 1 = partial, generic or implicit; 0 = absent from the document; NA = not applicable. "Absent from the document" does not mean absent from policy.
* There was a single coder and no independent second coding; see `data/codebook.md` §4 and `paper/limitations_and_data_gaps.md`.
* Page references are **PDF page numbers** (1-based) of the files in `data/raw/`, not printed page numbers.
