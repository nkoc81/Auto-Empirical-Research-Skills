# Literature log

All DOIs were resolved at CrossRef on 22 Nov 2026 (scripts/11_verify_references.py; raw records in
data/literature/crossref/). Bibliographic fields in paper/references.bib are taken from those records.
"Basis" states what the manuscript's use of each source rests on. No source was read in full text during this
project except the IMF How-To Note and the official reports. Claims attributed to other sources are kept at the
level of their well-known central argument, their CrossRef abstract, or their title/abstract as indicated.

| Key | Type | Peer reviewed | Basis for use in the manuscript | Used for |
|---|---|---|---|---|
| beer2022 | IMF How-To Note 22/05 (BibTeX @techreport; CrossRef files the series as a journal) | No (institutional guidance) | Full text read (data/raw/imf); every quotation and page checked against the PDF on 23 Nov 2026 | Evaluation framework; criteria mapping; Türkiye in Table 1 of the note |
| surrey1973, surrey1985 | Books | Academic press (Harvard UP) | General knowledge of the works' central argument; CrossRef metadata | Origin of the TE concept and spending-equivalence |
| burman2003 | Journal article (NTJ) | Yes | General knowledge of central argument; metadata | Relevance of TE concept; benchmark controversies |
| altshuler2011 | Journal article (NTJ) | Yes | General knowledge; metadata | Estimation methods (revenue forgone vs other approaches) |
| toder2000 | Journal article (NTJ) | Yes | General knowledge; cited also in beer2022 fn. 12 | TEs vs direct spending |
| burman2008 | Journal article (AER P&P) | Yes | General knowledge; metadata | Size and distribution of TEs |
| burton2013 | Monograph (CUP) | Academic press | CrossRef abstract | TE management, reporting controversies |
| brixi2003 | World Bank book | No (institutional) | Metadata | Early international TE reporting practice |
| oecd2010 | OECD book | No (institutional) | Metadata | Cross-country reporting practice |
| howard1999 | Monograph (Princeton UP) | Academic press | General knowledge | 'Hidden' spending through the tax code; accountability |
| mettler2011 | Monograph (U Chicago Press) | Academic press | General knowledge | Visibility of tax-based policy |
| heald2003 | Journal article (Public Administration) | Yes | CrossRef abstract | Transparency–accountability link |
| leviton2010 | Journal article (Annu Rev Public Health) | Yes | CrossRef abstract | Evaluability assessment concept |
| trevisan2007 | Journal article (Am J Evaluation) | Yes | CrossRef abstract | Evaluability assessment practice, document review as method |
| redonda2019 | Journal article (Economics) | Yes | CrossRef abstract | Opacity of TEs, transparency proposals |
| haldenwang2021 | Book chapter (Edward Elgar handbook) | Edited volume | Title/metadata | Politics of TEs |
| klemm2012 | Journal article (ITPF) | Yes | General knowledge | Evidence on tax incentives' effects (context only) |
| vanparys2010 | Journal article (ITPF) | Yes | General knowledge | Same |
| zee2002 | Journal article (World Development) | Yes | General knowledge | Design and evaluation of investment incentives |
| barsimantov2018 | Journal article (AJCL) | Yes | Title/metadata, general knowledge | Sunset clauses / temporary legislation |
| dziemianowicz2017 (print 2017 vol. 51; CrossRef issued 2018) | Journal article | Yes (university journal) | Title/metadata only | TEs and fiscal transparency (mentioned only as existing work) |
| ericok2019 | Journal article (İstanbul İktisat Dergisi) | Yes | Abstract (via DergiPark/RePEc listing, paraphrased search result) | Turkish literature: size/development of TEs 2015-2021 |
| yoruldu2021 | Journal article (Maliye Çalışmaları Dergisi) | Yes | Abstract (search result; document analysis of 2019-2023 TEs by functions of taxation) | Turkish literature |
| doganalp2020 | Journal article (EJOSAT) | Yes | Partial abstract only | Turkish literature: call to weigh fiscal cost against benefits |
| isikman2024 | Journal article (USSMAD) | Yes | CrossRef abstract | Turkish literature: deviations between realised and projected TEs |

Sources found but not used: ozturk2016, bayhanay2026, cicek2018 (verified, but their content is not needed
for the argument). The GTED flagship report (von Haldenwang et al. 2021) is cited only indirectly, as reported in
beer2022 (footnote 10); it was not retrieved.


## Audit note (23 Nov 2026)

The manuscript was revised so that sources not read in full are cited only for their central, widely known argument
(Surrey; Burman 2003; Altshuler & Dietz 2011; Howard; Mettler; Zee et al.; Van Parys & James; Klemm & Van Parys;
Bar-Siman-Tov) or for statements contained in their CrossRef abstract (Heald; Leviton et al.; Trevisan; Redonda et al.;
Burton & Sadiq). Statements about Turkish studies are explicitly marked in the text as based on abstracts.
oecd2026 was removed (not cited). All 26 entries in paper/references.bib are cited in the manuscript and vice versa.

## Bibliography audit (23 Nov 2026, second pass)

- Correction to the note above: toder2000 and burman2008 were in references.bib but not cited; both removed.
- barsimantov2018 previously pointed to a book review (AJCL 66(2), 453–457; OpenAlex type book-review). Replaced
  by Bar-Siman-Tov (2018), Regulation & Governance 12(2), 192–219, doi:10.1111/rego.12148 (Crossref + abstract);
  the sentence in Section 2.3 was rewritten to match that abstract.
- Twelve official sources added to references.bib (nine reports, Laws 7156 and 7197, Law 5018); fields taken from
  the documents in data/raw/. Law 5018 Arts. 15 and 18(2)(c) read in data/raw/law/.
- references.bib is now curated by hand; scripts/11_verify_references.py writes the raw Crossref version to
  data/literature/references_crossref_raw.bib instead of overwriting it.
- Full record: paper/reference_verification_report.md.
