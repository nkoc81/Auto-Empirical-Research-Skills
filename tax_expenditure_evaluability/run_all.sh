#!/usr/bin/env bash
# Re-runs the whole pipeline from the raw PDFs (data/raw) and text files (data/text) to tables and figures.
# Requires: python3 with pandas, numpy, matplotlib, pymupdf (fitz), fonttools, tabulate; network only for step 11.
set -euo pipefail
cd "$(dirname "$0")"
# The 2018 glyph map is learned from vocabulary in the 2016, 2017, 2020 and 2021 annexes, so those are extracted first.
python3 scripts/01_extract_annex_tables.py VHR2016 VHR2017 VHR2020 VHR2021 VHR2022 VHR2023 VHR2024 VHR2025
python3 scripts/00_decode_2018_glyphs.py
python3 scripts/01_extract_annex_tables.py VHR2018
python3 scripts/02_build_panel.py
python3 scripts/03_extract_summary_tables.py
python3 scripts/03b_budget_law_annexes.py > outputs/tables/budget_law_annex_log.txt
python3 scripts/04_reconcile.py > outputs/tables/reconciliation_log.txt
python3 scripts/05_extract_narratives.py
python3 scripts/06_candidate_sentences.py
python3 scripts/07_code_sections.py
python3 scripts/08_finalize_section_codes.py
python3 scripts/09_item_codes.py
python3 scripts/10_analysis.py > /dev/null
python3 scripts/11_verify_references.py   # uses cached CrossRef records in data/literature/crossref when present
python3 scripts/12_number_trace.py
python3 scripts/13_check_citations.py > /dev/null   # citation keys vs paper/references.bib
# Submission files (requires pandoc): python3 scripts/14_build_submission.py
echo "done"
