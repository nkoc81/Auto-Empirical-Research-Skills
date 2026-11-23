# Yerel Yönetimlerde Yeşil Finansman — bildiri geliştirme ve kaynak doğrulama

Teslim dosyaları:

| Dosya | İçerik |
|---|---|
| `01_Kaynak_Dogrulama_Raporu.md` | Kaynak doğrulama raporu |
| `02_Literatur_Matrisi.xlsx` | Literatür matrisi |
| `03_Degisiklik_Raporu.md` | Değişiklik raporu |
| `04_Yerel_Yesil_Finansman_Gelistirilmis.docx` | Geliştirilmiş bildiri |
| `05_Yonetici_Ozeti.md` | Yönetici özeti |
| `06_Atif_Kontrol_Raporu.md` | Atıf kontrol raporu |

Klasörler:

- `kaynak/`: Özgün Word dosyası. Değiştirilmemiştir.
- `calisma/`: Geliştirilmiş metnin Markdown kaynağı ve kontrol çıktıları.
- `dogrulama/`: DOI listeleri, Crossref/OpenAlex üst verileri ve önbellek.
- `scripts/`: Çalışmada kullanılan betikler.

Betikleri çalıştırmak için:

1. Üst verileri çekin:
   ```bash
   python3 scripts/fetch_meta.py dogrulama/yeni.txt
   ```
2. Atıf–kaynakça kontrolünü yapın:
   ```bash
   python3 scripts/atif_kontrol.py calisma/metin_gelistirilmis.md
   ```
3. Word dosyasını üretin:
   ```bash
   python3 scripts/build_docx.py
   ```
