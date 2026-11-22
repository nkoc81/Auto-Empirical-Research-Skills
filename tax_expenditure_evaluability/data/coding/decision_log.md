# Coding decision log

Single coder. Dates refer to coding sessions. Each entry states a rule clarification; overrides that implement
it are listed in data/coding/overrides.csv (with the decision id).

| Id | Date | Decision |
|---|---|---|
| D1 | 2026-11-22 | Unit of narrative coding is the numbered section of the provisions chapter. Section codes are attributed to every annex item mapped to the section. For multi-provision sections (e.g. GVK 23, 89; KVK 5, 10; KDV 13, 17; ÖTV 7) a code of 2 can rest on a purpose stated for only one sub-provision; item-level narrative codes are therefore upper bounds. |
| D2 | 2026-11-22 | Purpose words inside law/decree titles (e.g. '... Faaliyetlerinin Desteklenmesi Hakkında Kanun'), customs-tariff descriptions, definitions of entities by their own aims ('... amacıyla faaliyette bulunan'), and the report's general definition of a tax expenditure ('Vergi harcamasının hangi durumlarda ...') are not purpose statements. Implemented as the NOISE filter; residual cases overridden. |
| D3 | 2026-11-22 | C6/C7/B require non-cost information on use or effects. Counterfactual phrasing inside a cost computation ('bu istisna olmasaydı ... götürü gider') and section headings are not evidence. |
| D4 | 2026-11-22 | C8: 'etkin/etkinliği' in purpose statements (efficient use of resources) is not a cost-effectiveness assessment and is excluded; only explicit cost-effectiveness language or a comparison with direct spending/other instruments counts. The AGİ sections (2016-2021) state that the measure supports wage earners 'instead of direct public spending' and are coded C8 = 1. |
| D5 | 2026-11-22 | C9 = 2 requires a stated review/evaluation of the provision; the verb 'değerlendirilecek' in the sense of 'is treated as' does not count. Time limits in the quoted statute or narrative give C9 = 1. |
| D6 | 2026-11-22 | A purpose stated for an amendment that narrows or repeals the tax expenditure is not the purpose of the tax expenditure. |
| D7 | 2026-11-22 | C1 = 1 when the narrative describes the measure as an incentive/support or states a rationale only implicitly (e.g. neutrality between domestic supplies and imports) without saying what it is meant to achieve. |
| D8 | 2026-11-22 | Cue matching uses the part of each sentence outside quoted statute text (“...”); narrative purpose statements that precede a quotation are therefore retained. The quoted statute is used only for C2 (eligibility) and C9 (time limits). |
| D9 | 2026-11-22 | C5: simplification or lower compliance costs is an administrative rationale (C5 = 0); higher voluntary compliance, employment, investment, exports, R&D, savings, financial-market depth, current-account or energy-dependence reduction are policy outcomes (C5 = 1 if named in general terms). 'Encourage X' without a named result variable is C1 evidence only. |
| D10 | 2026-11-22 | Overrides decided on one report are applied to the same-title section of other reports only when the rule fired on the identical evidence sentence there (scripts/08_finalize_section_codes.py). Differences between consecutive reports that remain after this step were listed and checked (data/coding/consecutive_report_differences.csv). |
