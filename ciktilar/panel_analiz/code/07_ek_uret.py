"""Ek tabloları (Word) üretir."""
from pathlib import Path
import pandas as pd
R = Path(__file__).resolve().parents[1]
p = pd.read_csv(R / 'data/clean/panel_nihai.csv'); r = pd.read_csv(R / 'results/nihai_regresyonlar.csv')
v = pd.read_csv(R / 'results/varyans_dogrulama.csv')
TIP = {'S_C0': 'Bekâr', 'S_C2': 'Tek ebeveyn', 'C_C2': 'Tek kazançlı çift'}
f = lambda x, d=3: '' if pd.isna(x) else f"{x:.{d}f}".replace('.', ',').replace('-', '−')
md = ["---\ntitle: \"Ek Tablolar\"\nlang: tr\n---\n"]
k = p[p.tip == 'S_C0'].groupby('geo').agg(ilk=('yil', 'min'), son=('yil', 'max'), N=('yil', 'size'),
      bayrak=('bayrak', lambda s: ', '.join(f"{y} ({b})" for y, b in zip(p.loc[s.index, 'yil'], s) if isinstance(b, str) and b))).reset_index()
md.append("**Ek Tablo A1.** Ülkelere göre kapsam ve Eurostat bayrakları (ana bağımlı değişken; üç senaryoda aynı)\n")
md.append("| Ülke | İlk yıl | Son yıl | N | Bayraklı gözlemler |\n|---|---|---|---|---|")
md += [f"| {a.geo} | {a.ilk} | {a.son} | {a.N} | {a.bayrak} |" for a in k.itertuples()]
md.append("\n*Not:* b = seride kırılma; d = tanım farkı (Eurostat).\n")
md.append("**Ek Tablo A2.** Temel ve ortak modeller, 2014 sınıflandırma kontrolleriyle ve kontrolsüz\n")
md.append("| Senaryo | Model | 2014 kontrolü | Değişken | Katsayı | Std. hata | %95 GA | p (küme) | p (wild) |\n|---|---|---|---|---|---|---|---|---|")
for a in r[r.ornek == 'ana'].itertuples():
    md.append(f"| {TIP[a.tip]} | {'Ortak' if '+' in a.model else 'Ayrı'} | {'Evet' if a.isced_kontrol else 'Hayır'} | {'Yeterlilik' if a.degisken.startswith('yet') else 'PTR'} | {f(a.b)} | {f(a.se)} | [{f(a.ga_alt)}; {f(a.ga_ust)}] | {f(a.p)} | {f(a.p_wild)} |")
md.append("\n*Not:* Wild bootstrap p-değerleri wildboottest paketiyle (Rademacher, 9.999 tekrar, null kısıtlı) hesaplanmıştır. Yazarların kendi bootstrap kodu bir modelde paketten farklı sonuç verdiği için kullanılmamıştır. Paketin raporladığı 0,000 değerleri metinde <0,001 olarak gösterilmiştir.\n")
md.append("**Ek Tablo A3.** Tüm sağlamlık ve tamamlayıcı tahminler\n")
md.append("| Senaryo | Örneklem / sonuç | Değişken | N | Katsayı | Std. hata | %95 GA | p |\n|---|---|---|---|---|---|---|---|")
for a in r[r.ornek != 'ana'].itertuples():
    md.append(f"| {TIP[a.tip]} | {a.ornek} | {'Yeterlilik' if a.degisken.startswith('yet') else 'PTR'} | {a.N} | {f(a.b)} | {f(a.se)} | [{f(a.ga_alt)}; {f(a.ga_ust)}] | {f(a.p)} |")
md.append("\n**Ek Tablo A4.** Önceki (kullanılmayan) hane tipi serisinde kırılma sabitli model için varyans doğrulaması\n")
md.append("Bu tablo, makalede kullanılmayan önceki bir tasarımda (lfst_hheredty, 2006–2025, her kırılma bayrağından sonra ülkeye özgü sabit) standart hataların hatalı hesaplandığını ve bağımsız paketlerle nasıl düzeltildiğini belgelemektedir. Ham dummy matrisinin koşul sayısı yaklaşık 10^17'dir; statsmodels'in genelleştirilmiş ters ile hesapladığı varyans bir modelde negatif çıkmıştır.\n")
md.append("| Senaryo | Gösterge | Model | Rank / sütun | Katsayı | Ham varyans | SE (QR) | SE (pyfixest) | SE (linearmodels) |\n|---|---|---|---|---|---|---|---|---|")
for a in v.itertuples():
    md.append(f"| {TIP[a.tip]} | {'Yeterlilik' if a.gosterge.startswith('yet') else 'PTR'} | {a.model} | {a.rank}/{a.sutun} | {f(a.b_qr)} | {f(a.var_ham,4)} | {f(a.se_qr)} | {f(a.se_pyfixest)} | {f(a.se_linearmodels)} |")
(R / 'makale/ek_tablolar.md').write_text('\n'.join(md), encoding='utf-8')
