"""Seri kırılması kontrolleri ve standart hata seçimi için tanılama.

Çıktılar: results/kirilma_bayraklari.csv, results/kirilma_tanilama.csv, results/hata_yapisi.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
p = pd.read_csv(ROOT / "data/clean/panel.csv")
p['bayrak'] = p.bayrak.fillna('')
d0 = p[p.ortak].copy()

# 1) Kırılma bayraklarının ülke-yıl dağılımı (ana bağımlı değişken, ortak örneklem)
b = d0[d0.kirilma]
tab = b.groupby(['tip', 'yil']).geo.apply(lambda s: ' '.join(sorted(s))).unstack(0)
tab.to_csv(RES / "kirilma_bayraklari.csv")

satir, hata = [], []
for tip in ['S_C0', 'S_C2', 'C_C2']:
    d = d0[d0.tip == tip].copy()
    d['kir_grp'] = d.geo + '_' + d.kirilma_sayaci.astype(str)
    for x in ['yeterlilik_l1', 'ptr_l1']:
        for etiket, fe in (('ana', 'C(geo)'), ('kirilma_sabitleri', 'C(kir_grp)')):
            f = f"istihdam ~ {x} + gsyh_buyume + {fe} + C(yil)"
            m = smf.ols(f, d)
            X = m.exog
            K, rank = X.shape[1], np.linalg.matrix_rank(X)
            fit = m.fit()
            cl = m.fit(cov_type='cluster', cov_kwds={'groups': d.geo})
            # politika göstergesinde sabit etkiler sonrası kalan değişim
            aux = smf.ols(f"{x} ~ gsyh_buyume + {fe} + C(yil)", d).fit()
            j = list(m.exog_names).index(x)
            satir.append(dict(tip=tip, gosterge=x, model=etiket, N=int(fit.nobs), ulke=d.geo.nunique(),
                parametre=K, rank=rank, sabit_etki_grubu=d[fe[2:-1]].nunique(), kalan_sd=fit.df_resid,
                x_kalan_varyans_payi=aux.resid.var() / d[x].var(), x_kalan_sd=aux.resid.std(),
                b=fit.params[x], se_kume=cl.bse[x], kume_var_diag=cl.cov_params().iloc[j, j], se_ols=fit.bse[x]))
        # 4) hata yapısı: ana modelin artıkları
        fit = smf.ols(f"istihdam ~ {x} + gsyh_buyume + C(geo) + C(yil)", d).fit()
        r = d.assign(e=fit.resid).sort_values(['geo', 'yil'])
        r['e_l1'] = r.groupby('geo').e.shift(1)
        rho = r[['e', 'e_l1']].dropna().corr().iloc[0, 1]
        W = r.pivot(index='yil', columns='geo', values='e')
        Cm = W.corr(min_periods=5).values
        iu = np.triu_indices_from(Cm, 1)
        Tij = W.notna().astype(int).T.dot(W.notna().astype(int)).values[iu]
        ok = ~np.isnan(Cm[iu])
        N = W.shape[1]
        cd = np.sqrt(2 / (N * (N - 1))) * np.sum(np.sqrt(Tij[ok]) * Cm[iu][ok])  # Pesaran CD (dengesiz panel)
        hata.append(dict(tip=tip, gosterge=x, ulke=N, yil_sayisi=W.shape[0], ort_T=d.groupby('geo').size().mean(),
            artik_AR1=rho, ort_mutlak_kesit_korelasyon=np.nanmean(np.abs(Cm[iu])), pesaran_CD=cd))

pd.DataFrame(satir).to_csv(RES / "kirilma_tanilama.csv", index=False)
pd.DataFrame(hata).to_csv(RES / "hata_yapisi.csv", index=False)
pd.set_option('display.width', 250)
print(tab.to_string()); print(pd.DataFrame(satir).round(4).to_string()); print(pd.DataFrame(hata).round(3).to_string())
