# Limitations and data gaps

## Data availability
1. **Missing 2019 report.** No official copy of a 2019 Tax Expenditure Report was found (HMB archive lists 2007,
   2016–2018; the Revenue Administration lists 2020–2025; the 2019 file name returns HTTP 400). The 2018 realisation
   year is therefore missing, and the 2018→2020 comparisons span two report vintages.
2. **Budget-law annexes not retrieved separately.** Budget-law tax expenditure totals are taken from the tables the
   reports reprint; they are recorded as a separate series and never added to report totals. The 2008–2015 budget-law
   series rests on the 2007 methodology and is not comparable with the post-2016 series (the 2016 report prints both:
   1.34% vs 4.08% of GDP for 2015).
3. **Ministry of Industry and Technology statistics not used.** The ministry's website refused automated access; the
   restriction was not circumvented. These statistics report planned investment and employment on incentive
   certificates and would not measure tax expenditure costs or effects in any case.
4. **Ratios.** TE/GDP and TE/tax-revenue ratios are those published by the reports. The 2017 report publishes none.
   Nominal TL values are not compared across years.

## Extraction
5. Annex tables were extracted from PDFs with rotated pages (2020–2023), broken character encodings (2017) and fonts
   without Unicode maps (2018, decoded by a learned glyph map). Item rows reconcile with the printed sub-table totals in
   395 of 402 comparisons (±5 thousand TL) and with body totals within ±0.5 million TL; remaining differences are
   traced to the documents themselves (outputs/tables/official_document_inconsistencies.csv).
6. Five 2016 rows (MTV, ÖİV) were transcribed by hand; the 2016 MTV amount is printed on the first sub-item only.
7. Annex descriptions on some rotated pages of the 2021–2022 reports are word-scrambled; they are not used for coding
   (narratives are used), but they weaken cross-report item linking for BSMV/MTV rows.
8. **Item linking across reports** (338 linked identities) is a research construct based on legal reference and
   description similarity. Weak links were audited by sample; item-level time comparisons use only links based on
   both legal reference and description.

## Coding
9. **Single coder; no inter-coder reliability.** Codes come from explicit rules with recorded evidence sentences, followed
   by the author's review and logged overrides. This makes the coding reproducible and auditable but is not a
   substitute for an independent second coder. No re-coding by the same person is presented as independent coding.
10. **Section-to-item attribution.** Narrative codes are assigned at section level and attributed to every item mapped to
    the section; for sections covering many sub-provisions (e.g. GVK 23, 89; KVK 5, 10; KDV 13, 17; ÖTV 7) the item-level
    code is an upper bound. 16–26% of annex items (2020–2025; 92% in the 2017 report) map to no narrative section, including all BSMV, MTV
    and ÖİV items; these are coded "not reported".
11. **"Absent from the document" ≠ "absent from policy".** The coding concerns the official reports only. Objectives,
    data or reviews may exist in legislative preambles, ministry statistics or audit reports not covered here.
12. **C9 time limits** are mostly read from quoted statute; a time limit is not evidence that any review takes place.
13. The cue rules may miss unusual wording; the review targeted all sections coded 0 on C1 in 2016 and 2025, all rule
    hits on C6–C8 and B, and all changes between consecutive reports, but not every sentence of every report.

## Interpretation
14. All amounts are static revenue-forgone estimates under a no-behavioural-response assumption. They are not the
    revenue that repeal would raise and not measures of policy effects. Nothing in this study measures whether any tax
    expenditure is effective or ineffective; "not evaluable from the report" does not mean "ineffective".
15. Differences between projections, budget-law figures and later realisation estimates combine macro forecast errors,
    legal changes, inflation and data/method updates; they are not decomposed.
16. The IMF How-To Note is institutional guidance, not a peer-reviewed standard or a scored checklist; the nine criteria
    are the author's operationalisation of it.
