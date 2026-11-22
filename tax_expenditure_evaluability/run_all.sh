#!/usr/bin/env bash
# Re-runs the whole pipeline from the raw PDFs (data/raw) and text files (data/text) to tables and figures.
# Requires: python3 with pandas, numpy, matplotlib, pymupdf (fitz), fonttools, tabulate; network only for step 11.
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/00_decode_2018_glyphs.py
python3 scripts/01_extract_annex_tables.py
python3 scripts/02_build_panel.py
python3 scripts/03_extract_summary_tables.py
python3 scripts/04_reconcile.py > outputs/tables/reconciliation_log.txt
python3 scripts/05_extract_narratives.py
python3 scripts/06_candidate_sentences.py
python3 scripts/07_code_sections.py
python3 scripts/08_finalize_section_codes.py
python3 scripts/09_item_codes.py
python3 scripts/10_analysis.py > /dev/null
python3 scripts/11_verify_references.py   # uses cached CrossRef records in data/literature/crossref when present
echo "done"
