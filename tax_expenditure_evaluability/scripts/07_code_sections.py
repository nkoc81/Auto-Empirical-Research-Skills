"""Rule-based first-pass codes for the narrative criteria (C1, C2, C5-C9, M, B, TE_status) per report-section.

Every code carries the evidence sentence (first matching sentence), its PDF page and the rule that fired.
The coder then reviews the evidence (data/coding/review_*.csv) and records overrides in
data/coding/overrides.csv, which scripts/08_apply_overrides.py applies. Nothing here infers effects.
Output: data/coding/section_codes_auto.csv
"""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "coding"
OUT.mkdir(parents=True, exist_ok=True)

GENERIC = re.compile(r"(sosyal|ekonomik|mali)(\s*(ve|,|ile)\s*(sosyal|ekonomik|mali|kültürel|çevresel))*\s*(amaç|amaçlı|amacı)", re.I)
PURPOSE = re.compile(r"amacıyla|amacı ile|amacına|amaçlanm|amaçlamakta|amaçla(?!nan bu)|hedeflenm|hedeflemekte|maksadıyla|"
                     r"teşvik etmek|teşvik edilmesi|teşvik edilerek|desteklenmesi|desteklemek|özendirilmesi|korumak|korunması|"
                     r"kolaylaştırmak|kolaylık sağlanması|sağlanması amac|yaygınlaştırılması|geliştirilmesi|sağlamak (için|üzere)|"
                     r"sağlanması için|teşvik amacıyla|için (getirilmiş|düzenlenmiş)|(esas|temel|asıl) amac|"
                     r"(istisnanın|düzenlemenin|indirimin|muafiyetin|maddenin|uygulamanın) amacı|teşvik edilmektedir|"
                     r"teşvik edilmiştir|katkıda bulunul|katkı sağlan", re.I)
REFERENTIAL = re.compile(r"\b(bu|aynı|söz konusu) amaçla\b", re.I)
# spans that contain purpose words but are not purpose statements (decision log D2): law and decree titles,
# customs-tariff descriptions, definitions of entities by their own aims
NOISE = re.compile(r"\d+ (sayılı|Sayılı) [^.;]{0,160}?(Kanun|Karar|Kararname)[a-zıüğş]*|“[^”]*”|“[^”]*$|"
                   r"amacıyla (faaliyette bulunan|kurulan|kurulmuş|kullanan|kullanılan|teminat|ve sözleşme)|"
                   r"(Yatırımların Proje Bazında Desteklenmesi|Faaliyetlerinin Desteklenmesi|Desteklenmesine Dair|"
                   r"İyileştirilmesi Amacıyla)[^.]{0,80}|[^.]{0,120}Desteklenmesi Hakkında (Karar|Kanun)|"
                   r"Vergi harcamasının hangi durumlarda[^.]*", re.I)


def clean(s):
    return NOISE.sub(" ", s)
OUTCOME = re.compile(r"artır|istihdam|yatırım|ihracat|rekabet|büyüme|kalkınma|tasarruf|derinleş|ar-?ge|araştırma|inovasyon|gelişme|geliştirmek|"
                     r"yenilik|üretim|kayıt ?dışı|verimlilik|azaltıl|geliştiril|yaygınlaştır|cazip|finansman|konut", re.I)
TARGET = re.compile(r"hedef(lenen)?\s+[^.]{0,40}\d|%\s?\d+[^.]{0,30}(artış|azalış|hedef)", re.I)
COUNT = re.compile(r"\b\d{1,3}(?:\.\d{3})*\s+(adet|kişi|mükellef|firma|şirket|belge|işletme|proje|çalışan|personel)\b|"
                   r"(mükellef|kişi|firma|yararlanan|faydalanan|belge|işletme)\s+sayısı", re.I)
ADDIT = re.compile(r"olmasaydı|kendiliğinden|zaten (yapıl|gerçekleş)|karşı.?olgusal|ek katkı|etki analiz|net etki|"
                   r"ilave (yatırım|istihdam)[^.]{0,30}(sağla|yarat|oluş)", re.I)
COSTEFF = re.compile(r"maliyet.?etkin|fayda.?maliyet|maliyet.?fayda|doğrudan (kamu )?harcama|alternatif (araç|politika|destek)|"
                     r"\bhibe\b|nakdi destek", re.I)   # 'etkin/etkinliği' (efficient use) excluded: decision log D4
SUNSET = re.compile(r"tarihine kadar|yıl süreyle|vergilendirme dönemi (süreyle|boyunca)|süreyle uygulan|yılı sonuna kadar|"
                    r"sona er|uygulanmak üzere|geçici olarak|süresi uzat|uzatılmış|uzatmaya[^.]{0,40}yetkili|"
                    r"\d{4} yılı sonuna kadar|dönemlerinde uygulan|tarihleri arasında", re.I)
REVIEW = re.compile(r"(etki|sonuç|uygulama)[^.]{0,40}(değerlendirilecek|incelenecek|gözden geçirilecek)|gözden geçirilecek|"
                    r"yeniden değerlendirilecek|izlenecek|etki analizi", re.I)   # decision log D5
METHOD = re.compile(r"vergi harcaması (olacaktır|olarak (kabul|hesap|değerlendiril))|vergi harcaması tutarı|hesaplanacak|hesaplanmış|"
                    r"hesaplanmakta|hesaplanır|tespit edil", re.I)
DATA = re.compile(r"beyanname|bildirim|veri|kayıtlar|tahakkuk|gümrük|sgk|kurumdan|bakanlığından|bankalar|"
                  r"tutarlar[ıi]n[ıa]|tutarı(na)? |istatistik", re.I)
NOT_TE = re.compile(r"vergi harcaması (mahiyetinde|niteliğinde) değil|vergi harcaması (olarak )?"
                    r"(kabul edilme(z|mekte|mektedir|yecek|yecektir|miş|miştir)|değerlendirilme(z|mekte|mektedir|yecek|yecektir|miş|miştir))|"
                    r"vergi harcaması sayılma(z|makta|yacak)", re.I)
IS_TE = re.compile(r"vergi harcaması (niteliğinde(dir| olup| olmakta| bulunmakta)|olacaktır|mahiyetindedir)", re.I)


def first(idx, sents, pages, pat=None, extra=None):
    for i in idx:
        s = re.sub(r"“[^”]*”|“[^”]*$", " ", sents[i]) if pat is not SUNSET else sents[i]
        if (pat is None or pat.search(s)) and (extra is None or extra(s)):
            return i
    return None


def code_section(o):
    S, L, P = o["sentences"], o["legal"], o["pages"]
    # narrative = the part of a sentence outside quoted statute text (decision log D8)
    nonlegal = [i for i in range(len(S)) if len(re.sub(r"“[^”]*”|“[^”]*$", "", S[i]).strip()) > 30]
    rec = dict(report_id=o["report_id"], sec_no=o["sec_no"], title=o["title"], group=o["group"],
               page_start=o["page_start"], page_end=o["page_end"], n_sent=len(S))

    def ev(key, i, rule):
        rec[key + "_evidence"] = S[i][:300] if i is not None else ""
        rec[key + "_page"] = P[i] if i is not None else ""
        rec[key + "_rule"] = rule

    # TE status
    Q = [re.sub(r"“[^”]*”|“[^”]*$", " ", x) for x in S]
    nt = [i for i in nonlegal if NOT_TE.search(Q[i])]
    it = [i for i in nonlegal if IS_TE.search(Q[i]) and not NOT_TE.search(Q[i])]
    rec["TE_status"] = "not_te" if nt and not it else ("mixed" if nt and it else "te")
    ev("TE", nt[0] if nt else (it[0] if it else None), "NOT_TE/IS_TE")

    # C1 objective
    spec = first(nonlegal, S, P, None, lambda s: not REFERENTIAL.search(s) and PURPOSE.search(GENERIC.sub("", clean(s))))
    gen = first(nonlegal, S, P, GENERIC)
    if spec is not None:
        rec["C1"] = 2; ev("C1", spec, "specific purpose cue")
    elif gen is not None:
        rec["C1"] = 1; ev("C1", gen, "generic 'social/economic purpose' formula only")
    else:
        rec["C1"] = 0; ev("C1", None, "no purpose cue")

    # C2 beneficiaries: quoted statute defines eligibility, or narrative names the group
    ben = first(nonlegal, S, P, re.compile(r"yararlan|faydalan|mükellefler|kişiler|işletmeler|kurum ve kuruluş|sektör|çiftçi|esnaf|engelli|personel|hizmet erbabı", re.I))
    has_statute = any(L) or "Madde metni" in " ".join(S[:3])
    if ben is not None or has_statute:
        rec["C2"] = 2; ev("C2", ben if ben is not None else next(i for i in range(len(S)) if L[i]) if any(L) else 0,
                          "beneficiary cue in narrative" if ben is not None else "eligibility defined in quoted statute")
    else:
        rec["C2"] = 1 if len(S) else 0; ev("C2", None, "no explicit group")

    # C5 expected outcome (inside a purpose sentence)
    outc = first(nonlegal, S, P, None, lambda s: PURPOSE.search(clean(s)) and OUTCOME.search(clean(s)) and not REFERENTIAL.search(s))
    if outc is not None and TARGET.search(S[outc]):
        rec["C5"] = 2; ev("C5", outc, "outcome with quantified target")
    elif outc is not None:
        rec["C5"] = 1; ev("C5", outc, "outcome named in general terms")
    else:
        rec["C5"] = 0; ev("C5", None, "no outcome cue in purpose sentence")

    # C6 indicator / outcome data; B beneficiary count (candidates require review)
    cnt = first(nonlegal, S, P, COUNT)
    rec["C6"] = 1 if cnt is not None else 0; ev("C6", cnt, "count/indicator cue (REVIEW)" if cnt is not None else "none")
    rec["B"] = 2 if cnt is not None else 0; ev("B", cnt, "count cue (REVIEW)" if cnt is not None else "none")

    # C7 additionality; C8 cost-effectiveness / alternatives (candidates require review)
    a = first(nonlegal, S, P, ADDIT)
    rec["C7"] = 1 if a is not None else 0; ev("C7", a, "additionality cue (REVIEW)" if a is not None else "none")
    c = first(nonlegal, S, P, COSTEFF)
    rec["C8"] = 1 if c is not None else 0; ev("C8", c, "cost-effectiveness cue (REVIEW)" if c is not None else "none")

    # C9 review: review language (2, REVIEW) > time limit in statute or narrative (1) > none
    rv = first(nonlegal, S, P, REVIEW)
    sn = first(range(len(S)), S, P, SUNSET)
    if rv is not None:
        rec["C9"] = 2; ev("C9", rv, "review language (REVIEW)")
    elif sn is not None:
        rec["C9"] = 1; ev("C9", sn, "time limit / temporary nature (statute or narrative)")
    else:
        rec["C9"] = 0; ev("C9", None, "none")

    # M estimation method
    m2 = first(nonlegal, S, P, METHOD, lambda s: DATA.search(s))
    m1 = first(nonlegal, S, P, METHOD)
    if m2 is not None:
        rec["M"] = 2; ev("M", m2, "computation + data source")
    elif m1 is not None:
        rec["M"] = 1; ev("M", m1, "computation only")
    else:
        rec["M"] = 0; ev("M", None, "none")

    if rec["TE_status"] == "not_te":
        for k in ("C1", "C2", "C5", "C6", "C7", "C8", "C9", "M", "B"):
            rec[k] = "NA"
    return rec


def main():
    C = [json.loads(l) for l in open(ROOT / "data" / "interim" / "coding_candidates.jsonl", encoding="utf-8")]
    D = pd.DataFrame([code_section(o) for o in C])
    D.to_csv(OUT / "section_codes_auto.csv", index=False)
    cols = ["C1", "C2", "C5", "C6", "C7", "C8", "C9", "M", "B"]
    for c in cols:
        print(c, D.groupby("report_id")[c].apply(lambda s: s.astype(str).value_counts().to_dict()).to_dict() if False else
              D[c].astype(str).value_counts().to_dict())
    print(D.TE_status.value_counts().to_dict())


if __name__ == "__main__":
    main()
