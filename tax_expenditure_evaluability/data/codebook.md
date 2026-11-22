# Codebook: evaluability of tax expenditure reporting (Türkiye, 2016–2025 reports)

Version 1.0 (22 Nov 2026). One coder (the author). **No independent second coder was available.** Codes
were assigned with dictionary-assisted retrieval of candidate sentences (scripts/06_candidate_sentences.py)
followed by the coder's reading of each section. A later re-reading by the same coder (intra-coder check)
is reported as such and is *not* an inter-coder reliability statistic.

## 1. Units of analysis

| Unit | Definition | Used for |
|---|---|---|
| Report-item-year | One annex row (provision) of one report for one fiscal year (5 years per report) | C3, C4 |
| Report-item | One annex row of one report | C3/C4 summaries, link to narratives |
| Report-section | One numbered narrative section of Chapter 2 (2016: Chapter 3), usually one article of a law, sometimes several provisions | C1, C2, C5–C9 and the auxiliary variables M and B |

Narrative codes are attached to annex items through the legal reference (law + article). An annex item
that maps to no narrative section receives code 0 on C1, C2, C5–C9 with the note `no_narrative`
("not reported"), because the annex itself only gives a short label.

## 2. Code values

* **2** – explicit, provision-specific information.
* **1** – partial: general, implicit, shared by several provisions, or given only through the quoted legal text.
* **0** – absent from the document.
* **NA** – not applicable (the report states that the provision is not a tax expenditure, no tax expenditure
  arises, or the cell is a dash whose meaning is not stated), or the document cannot be read for that unit.

"0 = absent from the document" is a statement about the **report**, not about the policy. A provision may have an
objective, data or a review clause elsewhere (legislative preamble, other ministries' statistics) that the report
does not show. These cases are not searched for and not coded.

## 3. Criteria and decision rules

Mapping to the IMF How-To Note 22/05 (Beer et al., 2022) is given in column "IMF note". The note is guidance, not a
scored checklist; the criteria below are our operationalisation for document analysis.

| # | Criterion | 2 | 1 | 0 | IMF note (section / content) |
|---|---|---|---|---|---|
| C1 | Policy objective stated | A purpose statement specific to the provision says what the measure is meant to achieve (e.g. "protect low-income artisans", "support R&D") | Only a generic statement ("social and economic purpose", "has the nature of a tax expenditure"), a purpose stated jointly for a group of provisions, or a purpose that can only be inferred from the legal text/heading | No purpose | Evaluation requires an explicit statement of the policy objective; objectives often missing (von Haldenwang et al., 2021) |
| C2 | Target beneficiary group/sector/activity defined | Provision-specific eligible group, sector or activity identified (in narrative or quoted legal text) | Only a general reference ("certain taxpayers") | Not identified | Intended beneficiaries; distributional analysis |
| C3 | Item-level cost estimate | Numerical estimate for the item and year | Cost included in another item or a combined row; value flagged as uncertain by the extractor | "Veri temin edilememiştir", "Yeni uygulama" (no estimate yet), blank | Direct cost (revenue forgone) per measure |
|  | NA | "Vergi harcaması oluşmamıştır", dash "-", repealed |  |  |  |
| C4 | Estimate quality / uncertainty disclosed | Quality label **with** stated criteria, or a quantitative uncertainty measure (range, error, sensitivity) | Categorical label only ("çok iyi", "iyi", "yaklaşık"), whose criteria are not defined in the report | Estimated item without any label | Reliability of cost estimates |
|  | NA | Item-year without an estimate (C3 ≠ 2) |  |  |  |
| C5 | Expected policy outcome defined | Outcome variable named **and** quantified or linked to a target/indicator | Outcome named in general terms (e.g. "increase employment/investment/exports/savings") | No outcome beyond granting relief to the group, or only an administrative rationale | Theory of change; expected effects defined ex ante |
| C6 | Indicator / realised outcome data published | Provision-specific non-cost data on use or outcomes (number of beneficiaries, investment, jobs, etc.) | Partial non-cost data (aggregate counts, one year, or for a group of provisions) | None | Indicators and data for ex post evaluation |
| C7 | Additionality / counterfactual | Quantitative estimate of the additional activity caused | Qualitative discussion of whether the activity would occur anyway (deadweight, displacement) | None | Effectiveness relative to a counterfactual; redundant expenditure |
| C8 | Cost-effectiveness or alternative instruments | Cost per unit of outcome, or explicit comparison with a direct-spending/other alternative | Qualitative remark on efficiency or alternatives for the provision | None | Efficiency; comparison with direct spending and other instruments |
| C9 | Regular review (sunset, renewal, termination evaluation) | A scheduled review/evaluation of the provision is stated, or the results of a review informing renewal/termination are reported | A time limit, expiry date or temporary nature is visible (usually in the quoted legal text), or an extension/repeal is mentioned without evaluation | None | Periodic evaluation cycle; sunset clauses |

Auxiliary variables (not IMF criteria, recorded because they condition evaluability):

* **M – estimation method described** (2 = provision-specific data source and computation described; 1 = only "calculated
  from declarations" or a generic remark; 0 = none).
* **B – beneficiary count reported** (2 = provision-specific number of beneficiaries/claimants; 0 = none). Kept separate
  from C2 because defining a group is not the same as reporting its size.
* **TE_status** – the narrative's own classification of the provision: `te` (treated as a tax expenditure),
  `not_te` (report says it is not a tax expenditure, e.g. diplomatic exemptions), `mixed`.

## 4. Coding procedure (as implemented)

1. Narrative sections are extracted with page markers (scripts/05_extract_narratives.py): 74 (2016), 22 (2017),
   76 (2018), 82–87 (2020–2025) sections; the section lists match each report's table of contents.
2. Sentences are split; text inside quotation marks “...” (quoted statute) is separated from the report's own narrative
   (scripts/06_candidate_sentences.py; decision D8).
3. **Explicit coding rules** (scripts/07_code_sections.py) are applied to every section of every report. Each code
   carries the evidence sentence, its PDF page and the rule that fired. The rules are written versions of the decision
   rules in section 3 (cue lists for purpose, outcome, counts, additionality, cost-effectiveness, review/time limits,
   method; filters for false cues, decisions D2–D9).
4. **Review by the coder.** (a) For the 2025 and 2016 reports every C1 and C5 evidence sentence was read, and every
   section coded C1 = 0 was re-read for purpose statements the cues might miss; (b) every rule hit on C6, C7, C8,
   B and C9 = 2 in all reports was read (all C6/C7/B hits and all C9 = 2 hits were false positives; decisions D3, D5);
   (c) for all consecutive report pairs (and 2016 vs 2018) every same-title section whose code changed was listed
   (data/coding/consecutive_report_differences.csv) and checked against both texts. Corrections are recorded in
   data/coding/overrides.csv with a decision id and applied by scripts/08_finalize_section_codes.py.
5. C3 and C4 are derived mechanically from annex cell status and quality labels (scripts/09_item_codes.py), which also
   maps annex items to narrative sections by legal reference.

Limits of this procedure: there is no independent second coder and no inter-coder reliability statistic. The rule
layer makes the coding reproducible and auditable, but rules can miss unusual wording; the review step reduces, but
does not eliminate, this risk. Section codes attributed to items are upper bounds for multi-provision sections (D1).

## 5. Decision log

See data/coding/decision_log.md (dated entries for every rule clarification made during coding).
