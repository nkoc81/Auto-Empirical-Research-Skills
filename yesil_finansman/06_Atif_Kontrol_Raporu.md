# 06 — Atıf Kontrol Raporu

**Kontrol edilen dosya:** `calisma/metin_gelistirilmis.md` (Word sürümü: `04_Yerel_Yesil_Finansman_Gelistirilmis.docx`)
**Kontrol betiği:** `scripts/atif_kontrol.py`. Betik yeniden çalıştırılabilir:

```bash
python3 scripts/atif_kontrol.py calisma/metin_gelistirilmis.md
```

## 1. Özet sonuç

| Kontrol | Sonuç |
|---|---|
| Metin içi atıf örneği | 126 |
| Kaynakçada karşılığı olmayan atıf | **0** |
| Metinde atıf almayan kaynak | **0** |
| "ve" / "vd." biçim hatası (1, 2, 3+ yazar kuralı) | **0** |
| Kaynakça girdisi | 68 (64 DOI'li + 4 kitap) |
| Mükerrer DOI | 0 |
| DOI'si Crossref'te doğrulanmayan girdi | 0 |
| Kaynakça ve Crossref arasında yıl/cilt/sayfa uyumsuzluğu | 0 (otomatik karşılaştırma; ayrıntı Bölüm 3'te) |
| Öz | 195 kelime |
| Ana metin (Giriş → Sonuç, tablo dahil) | ~6.740 kelime (≥ 2.000 koşulu sağlandı) |
| Ortalama cümle uzunluğu | ~15 kelime |
| 40 kelimeyi aşan cümle | 1 (yöntem bölümündeki konu listesi) |
| Dosya bütünlüğü | Word dosyası python-docx ile açılıyor ve LibreOffice ile PDF'e dönüştürülebiliyor (20 sayfa). Tablo 1'in 10 satır × 7 sütun yapısı doğru |
| Özgün dosya | Değiştirilmedi. MD5 `7e782728…d015`, yüklenen dosyayla aynı |

## 2. Kaynak başına atıf sayısı (betik çıktısı)

```
   1x  ahmad 2026
   2x  anguelovski 2022
   4x  ayaydın hacıömeroğlu 2026
   1x  bachelet 2019
   2x  baggio 2025
   3x  baker 2022
   1x  berry-stölzle 2026
   1x  biasin 2024
   1x  bigger 2020
   2x  brown 2025
   2x  bunch 2025
   3x  busch 2021
   1x  campi 2024
   2x  compagnoni 2026
   1x  connolly 2026
   2x  davey 2026
   4x  de mello 2023
   1x  de mello 2024
   1x  deslatte 2023
   1x  diezmartínez 2024
   1x  diezmartínez 2025
   2x  droste 2017
   1x  ermasova 2026
   1x  fatica 2021
   1x  flammer 2021
   1x  funder 2022
   2x  garcía-lamarca 2022
   2x  gilmore 2022
   2x  goldsmith-pinkham 2023
   3x  gorelick 2020
   3x  jeon 2026
   1x  karpf 2018
   3x  keenan 2019
   1x  ko 2022
   4x  kupper 2026
   4x  larcker 2020
   1x  mazzucato 2013
   3x  moser 2019
   1x  moser-plautz 2025
   2x  oates 1972
   5x  oecd 2022
   1x  oecd 2023
   4x  oecd 2024
   3x  op de beeck 2024
   2x  painter 2020
   1x  papari 2024
   2x  partridge 2020
   1x  pigou 1920
   1x  pindiriri 2024
   1x  rashidi 2019
   1x  rogers 2025
   2x  romano 2023
   2x  sax 2022
   1x  shi 2020
   2x  shtob 2024
   2x  smull 2023
   3x  suchodolski 2022
   1x  sun 2023
   2x  taghizadeh-hesary 2019
   1x  thompson 2023
   2x  toxopeus 2021
   1x  tran 2024
   1x  wced 1987
   4x  white 2019
   1x  whittaker 2022
   1x  wu 2025
   2x  yazar 2020
   1x  zerbib 2019
```

İsimler betiğin eşleştirme anahtarlarıdır (küçük harfe çevrilmiş ilk yazar soyadı ve yıl). "de mello 2023" K. de Mello vd. (2023), "de mello 2024" L. de Mello ve Ter-Minassian (2024), "wced 1987" ise World Commission on Environment and Development (1987) karşılığıdır.

## 3. Kaynakça–Crossref karşılaştırması

Her kaynakça girdisindeki yıl, cilt ve ilk sayfa ya da makale numarası, `dogrulama/meta_*.json` dosyalarındaki Crossref kaydıyla otomatik karşılaştırılmıştır. Uyumsuzluk çıkmamıştır.

Yıl kararlarında APA 7 ilkesi uygulanmıştır: sayıya atanmış makalede baskı yılı kullanılır. Bu ilkenin uygulandığı kaynaklar:

| Kaynak | Çevrim içi yayın | Kullanılan yıl |
|---|---|---|
| Ahmad ve Du | 2025 | 2026 |
| Bigger ve Millington | 2019 | 2020 |
| Connolly ve Kythreotis | 2025 | 2026 |
| Baggio ve Tozer | 2024 | 2025 |
| Rogers vd. | 2024 | 2025 |
| Berry-Stölzle ve Hao | 2025 | 2026 |
| Yazar vd. | 2019 | 2020 |
| Suchodolski vd. | 2021 | 2022 |
| Ayaydın Hacıömeroğlu vd. | — | 2026 (cilt 109) |
| Papari vd. | DOI'de 2023 | 2024 (cilt 151) |

Davey (2026) henüz bir sayıya atanmamıştır ve "Advance online publication" olarak gösterilmiştir.

DOI'si olmayan dört kitap Crossref'te bulunmaz; künyeleri standart bibliyografik bilgiyle tutarlıdır.

## 4. Elle yapılan içerik kontrolleri

| Kontrol | Sonuç |
|---|---|
| Şirket veya uluslarüstü kuruluş bulgusunun belediyelere genellenmesi | Zerbib (2019), Fatica vd. (2021), Bachelet vd. (2019) ve Flammer (2021) için açık uyarı var |
| Ulusal bulgunun yerel yaygınlık gibi sunulması | OECD (2023, 2024), Ermasova vd. (2026) ve Pindiriri ve Kwaramba (2024) için "merkezî/ulusal düzey" uyarısı var |
| İlişkisel bulgunun nedensel dille aktarılması | Droste vd. (2017) ve Pindiriri ve Kwaramba (2024) ilişkisel dille yazıldı |
| Yazar yorumunun literatür bulgusundan ayrılması | 2.2, 4.2, 4.3 ve 5.4'te açıkça işaretlendi |
| Sayısal bulguların özetle uyumu | Tüm sayılar (bp, %, örneklem büyüklükleri, ülke ve kent sayıları) kaynak özetinde yer alıyor. Kaynak bazında liste `02_Literatur_Matrisi.xlsx` dosyasındadır |
| Sistematik derleme veya WoS izlenimi | Yöntem bölümünde açıkça reddedildi; atıf sayısı ve indeks ifadesi yok |

## 5. Bilinen sınırlılıklar

- Betik Türkçe ek almış atıfları ("Mazzucato'nun (2013)") ve çoklu yılları ("OECD (2022, 2024)") tanır. Ancak her olası Türkçe çekim ekini kapsadığı garanti edilemez. Bu nedenle sonuç ayrıca elle de gözden geçirilmiştir.
- Tablo 1'deki atıflar da sayıma dahildir.
