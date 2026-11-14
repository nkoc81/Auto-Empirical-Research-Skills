"""Nihai panel ve tahminler: lfsi_educ_a (IESS 2021 kırılması düzeltilmiş) ana sonuç.

Ana sonuç  : 20-64 yaş (lfsi_educ_a'da 2009-2025 düzeltilmiş seri yalnızca bu yaş grubunda var), ISCED 0-2 istihdam oranı (% nüfus), lfsi_educ_a
Göstergeler: TaxBEN asgari gelir yeterliliği (% medyan gelir) ve PTR (%, %67 AW ile işe geçiş), t-1
Senaryolar : S_C0 bekâr çocuksuz, S_C2 tek ebeveyn 2 çocuk, C_C2 tek kazançlı çift 2 çocuk
Model      : ülke ve yıl sabit etkileri + reel GSYH büyümesi; ülke düzeyinde kümelenmiş SE (CRV1)
             + wild cluster bootstrap p-değeri (wildboottest paketi; Rademacher, 9999, null kısıtlı)
2014 kontrolü: Eurostat edat1 metaverisi (15.2) ISCED 2011 geçişinde toplulaştırılmış eğitim
             düzeylerinin karşılaştırılamadığı ülkeleri AT ve EE olarak belirtir -> ülke x 2014+ göstergesi.
Çıktılar: data/clean/panel_nihai.csv, results/nihai_*.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd
import pyfixest as pf
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
RAW, CLEAN, RES = ROOT / "data/raw", ROOT / "data/clean", ROOT / "results"
ISO = {'AUT':'AT','BEL':'BE','BGR':'BG','HRV':'HR','CYP':'CY','CZE':'CZ','DNK':'DK','EST':'EE','FIN':'FI',
       'FRA':'FR','DEU':'DE','GRC':'EL','HUN':'HU','ISL':'IS','IRL':'IE','ITA':'IT','LVA':'LV','LTU':'LT',
       'LUX':'LU','MLT':'MT','NLD':'NL','NOR':'NO','POL':'PL','PRT':'PT','ROU':'RO','SVK':'SK','SVN':'SI',
       'ESP':'ES','SWE':'SE','CHE':'CH'}
TIPLER = {'S_C0': ('A1_NCH', '_Z'), 'S_C2': ('A1_CH', '_Z'), 'C_C2': ('A_CPL_CH', 'NOEARN')}
ISCED_KIRILMA = ['AT', 'EE']
B = 9999

def k(s):
    return s.astype(str).str.split(':').str[0]

ia = pd.read_csv(RAW / "DF_IA.csv.gz"); ia.columns = [c.split(':')[0] for c in ia.columns]
for c in ['REF_AREA', 'UNIT_MEASURE', 'HOUSEHOLD_TYPE', 'HOUSE_BENEFIT']: ia[c] = k(ia[c])
ia = ia[(ia.UNIT_MEASURE == 'PT_INC_DISP_HH_MEDIAN') & (ia.HOUSE_BENEFIT == 'NO')]
pt = pd.read_csv(RAW / "DF_PTRSA.csv.gz", low_memory=False); pt.columns = [c.split(':')[0] for c in pt.columns]
for c in ['REF_AREA', 'INCOME_CURR', 'HOUSEHOLD_TYPE', 'INCOME_PART', 'HOUSE_BENEFIT', 'TEMP_INTOWORK_BENEFIT']: pt[c] = k(pt[c])
pt = pt[(pt.INCOME_CURR == 'AW67') & (pt.HOUSE_BENEFIT == 'NO') & (pt.TEMP_INTOWORK_BENEFIT == 'NO')]

le = pd.read_csv(RAW / "lfsi_educ_a.csv")
le = le[(le.age == 'Y20-64') & (le.unit == 'PC_POP') & (le.sex == 'T')]
y = le[le.isced11 == 'ED0-2'][['geo', 'TIME_PERIOD', 'OBS_VALUE', 'OBS_FLAG']].rename(
    columns={'TIME_PERIOD': 'yil', 'OBS_VALUE': 'istihdam', 'OBS_FLAG': 'bayrak'})
hi = le[le.isced11 == 'ED5-8'][['geo', 'TIME_PERIOD', 'OBS_VALUE']].rename(columns={'TIME_PERIOD': 'yil', 'OBS_VALUE': 'istihdam_yuksek'})
gdp = pd.read_csv(RAW / "nama_10_gdp.csv")[['geo', 'TIME_PERIOD', 'OBS_VALUE']].rename(columns={'TIME_PERIOD': 'yil', 'OBS_VALUE': 'gsyh_buyume'})
hh = pd.read_csv(RAW / "lfst_hheredty.csv")[['geo', 'TIME_PERIOD', 'phhcomp', 'OBS_VALUE', 'OBS_FLAG']].rename(
    columns={'TIME_PERIOD': 'yil', 'OBS_VALUE': 'istihdam_hane', 'OBS_FLAG': 'bayrak_hane'})

parca = []
for tip, (hhc, es) in TIPLER.items():
    a = ia[ia.HOUSEHOLD_TYPE == tip][['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']].rename(columns={'OBS_VALUE': 'yeterlilik'})
    b = pt[(pt.HOUSEHOLD_TYPE == tip) & pt.INCOME_PART.str.startswith(es)][['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']].rename(columns={'OBS_VALUE': 'ptr'})
    g = a.merge(b, on=['REF_AREA', 'TIME_PERIOD'], how='outer')
    g['geo'] = g.REF_AREA.map(ISO)
    g = g.dropna(subset=['geo']).rename(columns={'TIME_PERIOD': 'yil'}).drop(columns='REF_AREA').sort_values(['geo', 'yil'])
    g['yeterlilik_l1'] = g.groupby('geo').yeterlilik.shift(1)
    g['ptr_l1'] = g.groupby('geo').ptr.shift(1)
    g['yil'] = g.yil.astype(int)
    m = (y.merge(g, on=['geo', 'yil']).merge(gdp, on=['geo', 'yil'], how='left').merge(hi, on=['geo', 'yil'], how='left')
          .merge(hh[hh.phhcomp == hhc].drop(columns='phhcomp'), on=['geo', 'yil'], how='left'))
    m['tip'] = tip
    parca.append(m)

p = pd.concat(parca, ignore_index=True)
p['bayrak'] = p.bayrak.fillna(''); p['bayrak_hane'] = p.bayrak_hane.fillna('')
p['egitim_farki'] = p.istihdam_yuksek - p.istihdam
p['isced_kirilma'] = (p.geo.isin(ISCED_KIRILMA) & (p.yil >= 2014)).astype(int)
p['isced_AT'] = ((p.geo == 'AT') & (p.yil >= 2014)).astype(int)
p['isced_EE'] = ((p.geo == 'EE') & (p.yil >= 2014)).astype(int)
p['sifir_yardim'] = p.yeterlilik_l1 == 0
p['ortak'] = p[['istihdam', 'yeterlilik_l1', 'ptr_l1', 'gsyh_buyume']].notna().all(axis=1)
p = p[p.ortak].reset_index(drop=True)
CLEAN.mkdir(exist_ok=True)
p.to_csv(CLEAN / "panel_nihai.csv", index=False)

# --- Kapsam ve betimsel istatistikler
kap = p.groupby('tip').agg(ulke=('geo', 'nunique'), gozlem=('geo', 'size'), ilk=('yil', 'min'), son=('yil', 'max'),
        bayrakli=('bayrak', lambda s: (s != '').sum()), sifir_yardim=('sifir_yardim', 'sum'))
kap['ulkeler'] = p.groupby('tip').geo.apply(lambda s: ' '.join(sorted(s.unique())))
kap['eksik_yillar'] = p.groupby('tip').apply(lambda d: '; '.join(f"{g}:{d[d.geo==g].yil.min()}-{d[d.geo==g].yil.max()} ({len(d[d.geo==g])})"
                                    for g in sorted(d.geo.unique()) if len(d[d.geo == g]) < d.yil.nunique()), include_groups=False)
kap.to_csv(RES / "nihai_kapsam.csv")
bet = []
for tip in TIPLER:
    d = p[p.tip == tip]
    for v in ['istihdam', 'yeterlilik_l1', 'ptr_l1', 'gsyh_buyume', 'egitim_farki']:
        w = d[v] - d.groupby('geo')[v].transform('mean')
        bet.append(dict(tip=tip, degisken=v, N=d[v].notna().sum(), ort=d[v].mean(), ss=d[v].std(), ulke_ici_ss=w.std(),
                        min=d[v].min(), maks=d[v].max()))
pd.DataFrame(bet).to_csv(RES / "nihai_betimsel.csv", index=False)
# ülke içi korelasyon (ülke ve yıl etkilerinden arındırılmış)
kor = []
for tip in TIPLER:
    d = p[p.tip == tip]
    r = [smf.ols(f"{v} ~ C(geo) + C(yil)", d).fit().resid for v in ('yeterlilik_l1', 'ptr_l1')]
    kor.append(dict(tip=tip, ham=d.yeterlilik_l1.corr(d.ptr_l1), ulke_yil_ici=np.corrcoef(r[0], r[1])[0, 1]))
pd.DataFrame(kor).to_csv(RES / "nihai_korelasyon.csv", index=False)

# --- Tahmin
satir = []
def tahmin(d, y_, xs, etiket, tip, kontrol='', boot=True):
    rhs = ' + '.join(xs + ['gsyh_buyume'] + ([kontrol] if kontrol else []))
    f = f"{y_} ~ {rhs} | geo + yil"
    fit = pf.feols(f, data=d, vcov={'CRV1': 'geo'})
    ci = fit.confint()
    for x in xs:
        r = dict(tip=tip, sonuc=y_, model='+'.join(xs), ornek=etiket, isced_kontrol=bool(kontrol), degisken=x,
                 N=fit._N, ulke=d.geo.nunique(), b=fit.coef()[x], se=fit.se()[x], p=fit.pvalue()[x],
                 ga_alt=ci.loc[x].iloc[0], ga_ust=ci.loc[x].iloc[1])
        if boot:
            # wildboottest paketi (fwildclusterboot portu): WCR, Rademacher, null kısıtlı; küme kimliği tamsayı olmalı
            fb = pf.feols(f, data=d.assign(gid=pd.factorize(d.geo)[0].astype(np.int64)), vcov={'CRV1': 'gid'})
            wb = fb.wildboottest(param=x, reps=B, seed=20261114, cluster='gid')
            r['p_wild'] = float(wb['Pr(>|t|)'])
        satir.append(r)
    return fit

for tip in TIPLER:
    d = p[p.tip == tip].copy()
    for kontrol in ('', 'isced_AT + isced_EE'):
        for xs in (['yeterlilik_l1'], ['ptr_l1'], ['yeterlilik_l1', 'ptr_l1']):
            tahmin(d, 'istihdam', xs, 'ana', tip, kontrol)
    for xs in (['yeterlilik_l1'], ['ptr_l1']):
        tahmin(d[d.bayrak == ''], 'istihdam', xs, 'bayrakli_haric', tip, 'isced_AT + isced_EE', boot=False)
        tahmin(d[~d.sifir_yardim], 'istihdam', xs, 'sifir_yardim_haric', tip, 'isced_AT + isced_EE', boot=False)
        tahmin(d[~d.geo.isin(ISCED_KIRILMA)], 'istihdam', xs, 'AT_EE_haric', tip, boot=False)
        tahmin(d[(d.yil < 2020) | (d.yil > 2021)], 'istihdam', xs, 'covid_2020_2021_haric', tip, 'isced_AT + isced_EE', boot=False)
        tahmin(d.dropna(subset=['egitim_farki']), 'egitim_farki', xs, 'egitim_farki', tip, 'isced_AT + isced_EE', boot=False)
        dh = d.dropna(subset=['istihdam_hane'])
        tahmin(dh, 'istihdam_hane', xs, 'hane_tipi_serisi(lfst_hheredty)', tip, 'isced_AT + isced_EE', boot=False)
        # Driscoll-Kraay (statsmodels; tam ranklı model)
        for L in (2, 4):
            f = f"istihdam ~ {xs[0]} + gsyh_buyume + isced_AT + isced_EE + C(geo) + C(yil)"
            dk = smf.ols(f, d).fit(cov_type='hac-groupsum', cov_kwds={'time': pd.factorize(d.yil)[0], 'maxlags': L})
            satir.append(dict(tip=tip, sonuc='istihdam', model=xs[0], ornek=f'driscoll_kraay_L{L}', isced_kontrol=True,
                degisken=xs[0], N=int(dk.nobs), ulke=d.geo.nunique(), b=dk.params[xs[0]], se=dk.bse[xs[0]],
                p=dk.pvalues[xs[0]], ga_alt=dk.conf_int().loc[xs[0], 0], ga_ust=dk.conf_int().loc[xs[0], 1]))

out = pd.DataFrame(satir)
out.to_csv(RES / "nihai_regresyonlar.csv", index=False)
pd.set_option('display.width', 250)
print(kap.drop(columns='eksik_yillar').to_string()); print(kap.eksik_yillar.to_string())
print(pd.DataFrame(bet).round(2).to_string()); print(pd.DataFrame(kor).round(2).to_string())
print(out.drop(columns=['sonuc']).round(3).to_string())
