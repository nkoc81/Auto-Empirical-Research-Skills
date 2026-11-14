"""Panel kurulumu ve temel iki yönlü sabit etkili tahminler.

Çıktılar: data/clean/panel.csv, results/kapsam.csv, results/sifirlar.csv, results/regresyonlar.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
RAW, CLEAN, RES = ROOT / "data/raw", ROOT / "data/clean", ROOT / "results"
rng = np.random.default_rng(20261114)

ISO = {'AUT':'AT','BEL':'BE','BGR':'BG','HRV':'HR','CYP':'CY','CZE':'CZ','DNK':'DK','EST':'EE','FIN':'FI',
       'FRA':'FR','DEU':'DE','GRC':'EL','HUN':'HU','ISL':'IS','IRL':'IE','ITA':'IT','LVA':'LV','LTU':'LT',
       'LUX':'LU','MLT':'MT','NLD':'NL','NOR':'NO','POL':'PL','PRT':'PT','ROU':'RO','SVK':'SK','SVN':'SI',
       'ESP':'ES','SWE':'SE','CHE':'CH','GBR':'UK'}
# OECD aile tipi -> Eurostat hane tipi; çiftte eş kazancı yok (tek kazançlı aile)
TIPLER = {'S_C0': ('A1_NCH', '_Z'), 'S_C2': ('A1_CH', '_Z'), 'C_C2': ('A_CPL_CH', 'NOEARN')}

def code(s):
    return s.astype(str).str.split(':').str[0]

# --- OECD göstergeleri
ia = pd.read_csv(RAW / "DF_IA.csv.gz")
ia.columns = [c.split(':')[0] for c in ia.columns]
for c in ['REF_AREA', 'UNIT_MEASURE', 'HOUSEHOLD_TYPE', 'HOUSE_BENEFIT']:
    ia[c] = code(ia[c])
ia = ia[(ia.UNIT_MEASURE == 'PT_INC_DISP_HH_MEDIAN') & (ia.HOUSE_BENEFIT == 'NO')]

pt = pd.read_csv(RAW / "DF_PTRSA.csv.gz", low_memory=False)
pt.columns = [c.split(':')[0] for c in pt.columns]
for c in ['REF_AREA', 'INCOME_CURR', 'HOUSEHOLD_TYPE', 'INCOME_PART', 'HOUSE_BENEFIT', 'TEMP_INTOWORK_BENEFIT']:
    pt[c] = code(pt[c])
pt = pt[(pt.INCOME_CURR == 'AW67') & (pt.HOUSE_BENEFIT == 'NO') & (pt.TEMP_INTOWORK_BENEFIT == 'NO')]

# --- Eurostat
hh = pd.read_csv(RAW / "lfst_hheredty.csv")
ed = pd.read_csv(RAW / "lfsa_ergaed.csv")
gdp = pd.read_csv(RAW / "nama_10_gdp.csv")[['geo', 'TIME_PERIOD', 'OBS_VALUE']].rename(
    columns={'TIME_PERIOD': 'yil', 'OBS_VALUE': 'gsyh_buyume'})
gap = ed.pivot_table(index=['geo', 'TIME_PERIOD'], columns='isced11', values='OBS_VALUE').reset_index()
gap['egitim_farki'] = gap['ED5-8'] - gap['ED0-2']
gap = gap.rename(columns={'TIME_PERIOD': 'yil'})[['geo', 'yil', 'egitim_farki']]

parcalar, sifirlar = [], []
for tip, (hhc, es) in TIPLER.items():
    a = ia[ia.HOUSEHOLD_TYPE == tip][['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']].rename(columns={'OBS_VALUE': 'yeterlilik'})
    b = pt[(pt.HOUSEHOLD_TYPE == tip) & pt.INCOME_PART.str.startswith(es)][['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']].rename(columns={'OBS_VALUE': 'ptr'})
    g = a.merge(b, on=['REF_AREA', 'TIME_PERIOD'], how='outer')
    g['geo'] = g.REF_AREA.map(ISO)
    g = g.dropna(subset=['geo']).rename(columns={'TIME_PERIOD': 'yil'}).drop(columns='REF_AREA')
    sifirlar.append(g[g.yeterlilik == 0].assign(tip=tip))
    g = g.sort_values(['geo', 'yil'])
    g['yeterlilik_l1'] = g.groupby('geo').yeterlilik.shift(1)
    g['ptr_l1'] = g.groupby('geo').ptr.shift(1)
    y = hh[hh.phhcomp == hhc][['geo', 'TIME_PERIOD', 'OBS_VALUE', 'OBS_FLAG']].rename(
        columns={'TIME_PERIOD': 'yil', 'OBS_VALUE': 'istihdam', 'OBS_FLAG': 'bayrak'})
    m = y.merge(g, on=['geo', 'yil'], how='inner').merge(gdp, on=['geo', 'yil'], how='left').merge(gap, on=['geo', 'yil'], how='left')
    m['tip'] = tip
    parcalar.append(m)

panel = pd.concat(parcalar, ignore_index=True)
panel['bayrak'] = panel.bayrak.fillna('')
panel['dusuk_guv'] = panel.bayrak.str.contains('u')
panel['kirilma'] = panel.bayrak.str.contains('b')
# Ülkeye özgü seri kırılması: kırılma yılından sonraki dönem göstergesi (ülke içinde kümülatif sayaç)
panel = panel.sort_values(['tip', 'geo', 'yil'])
panel['kirilma_sayaci'] = panel.groupby(['tip', 'geo']).kirilma.cumsum()
panel['sifir_yardim_l1'] = panel.yeterlilik_l1 == 0
VARS = ['istihdam', 'yeterlilik_l1', 'ptr_l1', 'gsyh_buyume']
panel['ortak'] = panel[VARS].notna().all(axis=1)
CLEAN.mkdir(exist_ok=True); RES.mkdir(exist_ok=True)
panel.to_csv(CLEAN / "panel.csv", index=False)
pd.concat(sifirlar).to_csv(RES / "sifirlar.csv", index=False)

# --- Kapsam tablosu
k = panel[panel.ortak].groupby('tip').agg(ulke=('geo', 'nunique'), gozlem=('geo', 'size'), ilk=('yil', 'min'),
    son=('yil', 'max'), dusuk_guv=('dusuk_guv', 'sum'), kirilma=('kirilma', 'sum'), sifir_yardim=('sifir_yardim_l1', 'sum'))
k['ulkeler'] = panel[panel.ortak].groupby('tip').geo.apply(lambda s: ' '.join(sorted(s.unique())))
k['eksik_istihdam'] = panel.groupby('tip').istihdam.apply(lambda s: s.isna().sum())
k.to_csv(RES / "kapsam.csv")
print(k.to_string())

# --- Tahmin
def wild_p(df, f, var, B=999):
    """Rademacher wild cluster bootstrap-t (null kısıtlı), ülke kümeleri."""
    fit = smf.ols(f, df).fit(cov_type='cluster', cov_kwds={'groups': df.geo})
    t0 = fit.tvalues[var]
    r = smf.ols(f.replace(var + ' +', '').replace('+ ' + var, ''), df).fit()
    g = df.geo.values; ug = np.unique(g); idx = np.searchsorted(ug, g)
    ts = []
    for _ in range(B):
        w = rng.choice([-1, 1], len(ug))[idx]
        d = df.copy(); d[f.split('~')[0].strip()] = r.fittedvalues + r.resid * w
        fb = smf.ols(f, d).fit(cov_type='cluster', cov_kwds={'groups': d.geo})
        ts.append(fb.tvalues[var])
    return np.mean(np.abs(ts) >= abs(t0))

satirlar = []
def tahmin(df, y, xs, ornek, tip, boot=False):
    f = f"{y} ~ {' + '.join(xs)} + gsyh_buyume + C(geo) + C(yil)"
    cl = smf.ols(f, df).fit(cov_type='cluster', cov_kwds={'groups': df.geo})
    dk = smf.ols(f, df).fit(cov_type='hac-groupsum', cov_kwds={'time': pd.factorize(df.yil)[0], 'maxlags': 2})
    for x in xs:
        satirlar.append(dict(tip=tip, sonuc=y, model='+'.join(xs), ornek=ornek, degisken=x, N=int(cl.nobs),
            ulke=df.geo.nunique(), b=cl.params[x], se_kume=cl.bse[x], p_kume=cl.pvalues[x],
            ki_alt=cl.conf_int().loc[x, 0], ki_ust=cl.conf_int().loc[x, 1], se_dk=dk.bse[x], p_dk=dk.pvalues[x],
            p_wild=wild_p(df, f, x) if boot else np.nan))

for tip in TIPLER:
    d = panel[(panel.tip == tip) & panel.ortak].copy()
    for xs in (['yeterlilik_l1'], ['ptr_l1'], ['yeterlilik_l1', 'ptr_l1']):
        tahmin(d, 'istihdam', xs, 'ortak', tip, boot=True)
        tahmin(d[~d.dusuk_guv], 'istihdam', xs, 'dusuk_guv_haric', tip)
        tahmin(d[~d.sifir_yardim_l1], 'istihdam', xs, 'sifir_yardim_haric', tip)
    # Kırılma kontrolleri. 'b' bayraklarının çoğu tüm ülkelerde ortak 2014 ve 2021 yöntem değişikliklerinde.
    # (i) her bayraklı yıldan sonra ülkeye özgü sabit (en katı; tahmin varyansının çoğunu emer)
    d['kir_grp'] = d.geo + '_' + d.kirilma_sayaci.astype(str)
    # (ii) ülke x 2014 sonrası ve ülke x 2021 sonrası sabitleri
    d['donem'] = d.geo + '_' + np.select([d.yil >= 2021, d.yil >= 2014], ['c', 'b'], 'a')
    for etiket, grp, dd in (('kirilma_tum_bayraklar', 'kir_grp', d), ('ulke_x_2014_2021', 'donem', d),
                            ('2006_2020', 'geo', d[d.yil <= 2020])):
        for x in ('yeterlilik_l1', 'ptr_l1'):
            f = f"istihdam ~ {x} + gsyh_buyume + C({grp}) + C(yil)"
            cl = smf.ols(f, dd).fit(cov_type='cluster', cov_kwds={'groups': dd.geo})
            satirlar.append(dict(tip=tip, sonuc='istihdam', model=x, ornek=etiket, degisken=x, N=int(cl.nobs),
                ulke=dd.geo.nunique(), b=cl.params[x], se_kume=cl.bse[x], p_kume=cl.pvalues[x],
                ki_alt=cl.conf_int().loc[x, 0], ki_ust=cl.conf_int().loc[x, 1]))
    # tamamlayıcı: eğitim grupları arası istihdam farkı (yüksek - düşük), aynı örneklem
    dg = d.dropna(subset=['egitim_farki'])
    for xs in (['yeterlilik_l1'], ['ptr_l1']):
        tahmin(dg, 'egitim_farki', xs, 'ortak', tip)

out = pd.DataFrame(satirlar)
out.to_csv(RES / "regresyonlar.csv", index=False)
pd.set_option('display.width', 250)
print(out.round(3).to_string())
