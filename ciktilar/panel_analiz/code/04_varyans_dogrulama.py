"""Kırılma sabitli modelde küme varyansının doğrulanması.

(a) statsmodels, ham dummy matrisi (önceki kod)
(b) statsmodels, QR ile doğrusal bağımlı sütunlar çıkarılmış matris
(c) pyfixest: sabit etkiler absorbe edilir, CRV1 ülke kümesi
(d) linearmodels PanelOLS: entity=kırılma grubu, time=yıl absorbe; ülke kümesi
Çıktı: results/varyans_dogrulama.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pyfixest as pf
from linearmodels.panel import PanelOLS
from patsy import dmatrices

ROOT = Path(__file__).resolve().parents[1]
p = pd.read_csv(ROOT / "data/clean/panel.csv")
p = p[p.ortak].copy()
p['kir_grp'] = p.geo + '_' + p.kirilma_sayaci.astype(str)

def qr_drop(X, tol=1e-9):
    q, r = np.linalg.qr(X)
    keep = np.abs(np.diag(r)) > tol * np.abs(np.diag(r)).max()
    return X[:, keep], keep

rows = []
for tip in ['S_C0', 'S_C2', 'C_C2']:
    d = p[p.tip == tip].reset_index(drop=True)
    for x in ['yeterlilik_l1', 'ptr_l1']:
        for etiket, fe in (('ana', 'geo'), ('kirilma', 'kir_grp')):
            f = f"istihdam ~ {x} + gsyh_buyume + C({fe}) + C(yil)"
            y, X = dmatrices(f, d, return_type='dataframe')
            # (a) ham matris
            a = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': d.geo})
            # (b) doğrusal bağımlı sütunlar çıkarılmış
            Xk, keep = qr_drop(X.values)
            cols = X.columns[keep]
            b = sm.OLS(y, pd.DataFrame(Xk, columns=cols)).fit(cov_type='cluster', cov_kwds={'groups': d.geo})
            # (c) pyfixest
            c = pf.feols(f"istihdam ~ {x} + gsyh_buyume | {fe} + yil", data=d, vcov={'CRV1': 'geo'})
            # (d) linearmodels
            dl = d.set_index([fe, 'yil'])
            e = PanelOLS(dl['istihdam'], dl[[x, 'gsyh_buyume']], entity_effects=True, time_effects=True,
                         drop_absorbed=True).fit(cov_type='clustered', clusters=pd.DataFrame(pd.factorize(d.geo)[0], index=dl.index, columns=['c']))
            rows.append(dict(tip=tip, gosterge=x, model=etiket, N=len(d), sutun=X.shape[1],
                rank=int(np.linalg.matrix_rank(X.values)), cikarilan=int((~keep).sum()),
                kosul_sayisi=np.linalg.cond(X.values),
                b_ham=a.params[x], var_ham=a.cov_params().loc[x, x],
                b_qr=b.params[x], se_qr=b.bse[x],
                b_pyfixest=c.coef()[x], se_pyfixest=c.se()[x], p_pyfixest=c.pvalue()[x],
                b_linearmodels=e.params[x], se_linearmodels=e.std_errors[x]))

out = pd.DataFrame(rows)
out.to_csv(ROOT / "results/varyans_dogrulama.csv", index=False)
pd.set_option('display.width', 250)
print(out.round(4).to_string())
