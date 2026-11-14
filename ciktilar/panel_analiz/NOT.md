# Proje notları

## Nihai analiz (makalede kullanılan)
- Veri: `data/clean/panel_nihai.csv` (30 ülke, 2009–2025, senaryo başına 492 gözlem)
- Kod sırası: `code/01_indir.sh` → `code/05_nihai_tahmin.py` → `code/07_ek_uret.py` → `code/06_makale_derle.py`
- Sonuçlar: `results/nihai_*.csv`, `results/Ek_tablolar.xlsx`
- Makale: `makale/Makale_asgari_gelir_istihdam.docx`, ek: `makale/Ek_tablolar.docx`
- Kaynak doğrulama: `kaynakca/` (CrossRef sorguları, `kaynak_meta.json`, `kaynakca.md`)

## Kullanılmayan / hatalı önceki çıktılar
- `results/regresyonlar.csv`, `results/kirilma_*.csv`, `results/hata_yapisi.csv`: önceki tasarım (lfst_hheredty). `kirilma_*` satırlarındaki küme SE'leri sayısal olarak hatalıdır; doğrulanmış değerler `results/varyans_dogrulama.csv`.
- `code/02`–`04`: önceki tasarımın kodları; makalede kullanılmaz.
- Kendi yazdığımız wild bootstrap fonksiyonu, wildboottest paketinden farklı sonuç verdiği için kaldırıldı; makaledeki bootstrap p-değerleri pakete aittir.
