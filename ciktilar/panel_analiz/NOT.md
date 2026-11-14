# Notlar
- `results/regresyonlar.csv` içindeki `kirilma_*` satırlarının küme standart hataları hatalıdır (koşul sayısı ~1e17 olan dummy matrisinde sayısal kararsızlık). Doğrulanmış değerler: `results/varyans_dogrulama.csv` (pyfixest, linearmodels, QR ile indirgenmiş statsmodels).
- `lfsa_ergaed` ve `lfst_hheredty` 2014 (ISCED) ve 2021 (IESS) kırılmalarını içerir. `lfsi_educ_a` 2021 kırılması için düzeltilmiştir (2009–); ISCED 2014 değişikliği düzeltilmemiştir.
