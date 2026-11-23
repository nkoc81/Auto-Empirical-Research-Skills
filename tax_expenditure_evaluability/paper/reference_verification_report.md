# Kaynakça ve Atıf Doğrulama Raporu

**Makale:** *Evaluability of Tax Expenditures in Türkiye: An Assessment of Official Reporting Against the IMF Evaluation Framework*
**Tarih:** 23 Kasım 2026
**Dosyalar:** `paper/manuscript.md`, `paper/references.bib`, `paper/csl/apa.csl`

Kontroller şu betiklerle yeniden çalıştırılabilir:

- `scripts/13_check_citations.py`: atıf anahtarı ve kaynakça karşılaştırması
- `scripts/12_number_trace.py`: metindeki sayıların izlenmesi
- `scripts/14_build_submission.py`: gönderim dosyalarının üretimi

## 1. Başlangıç durumu ve dış değerlendirmeye yanıt

`paper/references.bib` dosyası depoda mevcuttu. Dış değerlendirmede "dosya yok" denmesinin nedeni, dosyanın değerlendiriciye iletilmemiş olmasıdır. Aynı durum kaynak PDF'ler, betikler ve çıktı tabloları için de geçerlidir:

- `data/raw/`: 22 kaynak dosya
- `scripts/`, `outputs/tables/`
- `outputs/tables/manuscript_number_trace.csv`

Bununla birlikte değerlendirmede haklı olan beş nokta vardı ve hepsi düzeltildi:

| Sorun | Düzeltme |
|---|---|
| Önceki Word çıktısı kaynakçasızdı. Pandoc `--citeproc` kullanılmadan dışa aktarılmıştı. | Yeni çıktı citeproc ve APA 7 CSL dosyasıyla üretildi; kaynakça dahil. |
| Resmî belgeler (raporlar, bütçe kanunları, 5018) bib'de değildi. Metinde "(VHR2025, PDF p. 23)" biçiminde düz metinle anılıyorlardı. | 12 resmî kayıt eklendi. Bu anılar Pandoc atıfına çevrildi. |
| Ek cetvel iddiası için 5018 sayılı Kanun'un 18. maddesi yoktu. | 15. madde (bütçe kanununda vazgeçilen vergi gelirlerinin gösterilmesi) ve 18/2-c (vazgeçilen kamu gelirleri cetvelinin kanun tasarısına eklenmesi) metinden doğrulandı ve makaleye eklendi. |
| Veri ve kod paragrafında bağlantı, sürüm ve dosya listesi yoktu. | Anonim makaleye dosya listesi eklendi. Depo adresi ayrı başlık sayfasına konuldu (kör hakemlik için). DOI henüz yok; uydurulmadı. |
| `scripts/11_verify_references.py`, her çalıştırmada `references.bib` dosyasının üzerine yazıyordu. | Betik artık ham Crossref çıktısını `data/literature/references_crossref_raw.bib` dosyasına yazıyor. Elle doğrulanmış `references.bib` korunuyor. |

## 2. Atıf stili

Proje dosyalarında hedef dergi belirtilmemiştir. Bu nedenle **APA 7** kullanıldı. Kullanılan stil dosyası, CSL deposundaki *APA Style 7th edition* sürümüdür (2026-02-07); `paper/csl/apa.csl` olarak kaydedildi.

Hedef dergi belirlendiğinde yalnızca `csl:` satırı değiştirilerek o derginin stiline geçilebilir. Örneğin Elsevier, Springer veya Taylor & Francis dergilerinin CSL dosyaları kullanılabilir.

Uygulanan APA ayrıntıları:

- Türkçe başlıklardan sonra köşeli parantez içinde İngilizce çeviri verildi (APA 7, 9.38). Çeviriler yazara aittir.
- Kurum hem yazar hem yayıncı olduğunda yayıncı tekrar edilmedi.
- Alt birim yazar olarak, bağlı olduğu bakanlık yayıncı olarak yazıldı. Örnek: Gelir Düzenlemeleri Genel Müdürlüğü / Hazine ve Maliye Bakanlığı.
- Resmî raporlarda sayfa gösterimleri PDF sayfasına göredir. Bu durum yöntem bölümünde açıkça belirtildi.

## 3. Anahtar envanteri

| | Sayı |
|---|---|
| Önceki metindeki literatür anahtarları | 24 |
| Önceki bib kayıtları | 26. Bunların ikisi (`toder2000`, `burman2008`) metinde hiç kullanılmıyordu. Önceki notta "26 kaydın tamamı atıflı" yazıyordu; bu ifade yanlıştı. |
| Çıkarılan kayıtlar | 2 (`toder2000`, `burman2008`; kullanılmıyordu) |
| İçeriği değişen kayıt | 1 (`barsimantov2018`; bkz. 4.2) |
| Eklenen resmî kayıtlar | 12. Dokuz vergi harcamaları raporu (`vhr2016`–`vhr2018`, `vhr2020`–`vhr2025`), iki bütçe kanunu (`law7156`, `law7197`) ve `law5018`. |
| **Son durum** | **36 anahtar metinde, 36 kayıt bib'de** |
| Metinde olup bib'de olmayan | 0 |
| Bib'de olup metinde olmayan | 0 |
| Metin içi atıf örneği | 73 |

## 4. Kayıt bazında doğrulama

### 4.1. Akademik kaynaklar

Akademik kaynakların yazar, yıl, başlık, dergi, cilt, sayı, sayfa ve DOI bilgileri Crossref kayıtlarından alındı (`data/literature/crossref/*.json`). Gerektiğinde OpenAlex ile karşılaştırıldı.

| Anahtar | Durum | Not |
|---|---|---|
| beer2022 | Tam doğrulandı | Künye PDF kapağından alındı: "NOTE 22/05", dört yazar, Kasım 2022. DOI Crossref'te. **Sayfa atıfları PDF metniyle tek tek kontrol edildi** (basılı sayfa = PDF sayfası − 5). Bir hata düzeltildi: "pp. 4, 12" → "pp. 3, 10, 12" (bkz. 4.3). |
| altshuler2011, burman2003, heald2003, klemm2012, leviton2010, trevisan2007, vanparys2010, zee2002, isikman2024 | Tam doğrulandı | Klemm ve Van Parys: çevrim içi 2011, baskı 2012 19(3). APA'ya göre 2012 kullanıldı. |
| surrey1973, surrey1985, howard1999, mettler2011, burton2013, brixi2003, oecd2010 | Doğrulandı | Crossref'teki alt başlıklar eklendi. |
| haldenwang2021 | **Kısmen doğrulandı** | Editörler (Hakelberg ve Seelkopf) RePEc/IDEAS ve yayıncı kaydından doğrulandı. Sayfa aralığında kaynaklar çelişiyor (128–145 ve 129–…). Bu nedenle sayfa yazılmadı. |
| redonda2019 | Doğrulandı | *Economics* 13(1). Makale numarası Crossref'te ayrı bir alan olarak yok; eklenmedi. |
| ericok2019, yoruldu2021 | Doğrulandı | Yoruldu (2021) için Crossref cilt değeri "0"; yalnız sayı (65) yazıldı. |
| doganalp2020 | **Kısmen doğrulandı** | Crossref ve OpenAlex'te cilt ve sayı yok; yalnız sayfa (201–205) var. |
| dziemianowicz2017 | **Kısmen doğrulandı** | Crossref'te yalnız ilk sayfa (79) var. Yıl konusunda belirsizlik var: sayı yılı ve DOI 2017'yi, Crossref "issued" tarihi 2018-01-12'yi gösteriyor. Sayı yılı (2017) kullanıldı. |

### 4.2. Değiştirilen kayıt: Bar-Siman-Tov (2018)

Önceki kayıt (*American Journal of Comparative Law* 66(2), 453–457, doi:10.1093/ajcl/avy011) bir **kitap incelemesidir**. OpenAlex türü "book-review"; özet, Kouroutakis'in kitabını değerlendiriyor. Bu kayıt metindeki genel iddiayı desteklemek için zayıftı.

Yerine aynı yazarın ampirik makalesi konuldu: *Regulation & Governance* 12(2), 192–219, doi:10.1111/rego.12148. Künye Crossref'ten, özet OpenAlex'ten doğrulandı.

Metindeki cümle özete uygun biçimde yeniden yazıldı. Yeni cümle, geçici (sunset) yasaların daha iyi düzenleme ve gözden geçirme aracı olarak sunulduğunu ve kullanımına ilişkin ampirik kanıtın sınırlı olduğunu söylüyor.

### 4.3. IMF notu sayfa atıflarının kontrolü

Her sayfa atfı, PDF metninde ilgili ifadeyle karşılaştırıldı:

| Metindeki iddia | Sayfa | Sonuç |
|---|---|---|
| 102 ülke; "does not by itself ensure ... well spent" | p. 1 | Doğru |
| Tanım ("deviations from a benchmark tax system") | p. 1, Box 1 p. 2 | Doğru; önceki "Box 1, p. 2" gösterimi kesinleştirildi |
| Tahminler sıklıkla kapsamlı değil | p. 1, dipnot 1 | Doğru. Önceki cümle dipnotta olmayan bir neden ("verisi olmayan hükümler hesaplanmaz") ekliyordu; çıkarıldı. |
| Türkiye 2017: 222 vergi harcaması / 183 tahmin / değerlendirmeye atıf yok | Tablo 1, p. 3 | Doğru |
| "to understand how a TE works, whom it benefits, and its intended purpose"; ex ante göstergeler; dipnot 10 (yaklaşık %70) | p. 5 | Doğru |
| Değişim kuramı | p. 6 | Doğru |
| Karşı-olgusal değerlendirme, ikame (displacement) | pp. 5, 7 | Doğru |
| Box 2: "How large and how reliable are the cost estimates" | p. 7 | Doğru |
| Doğrudan harcamayla karşılaştırma | p. 6 | Doğru |
| Çok yıllı değerlendirme döngüsü | pp. 3–4 | Doğru |
| Değerlendirme raporlarının yayımı; yararlanıcılar | p. 11 | Doğru |
| Pragmatik yaklaşım, öncelikle en önemli vergi harcamaları, nitel değerlendirme | **pp. 4, 12 → pp. 3, 10, 12** | **Düzeltildi.** "Most important TEs" ifadesi p. 12'de, "pragmatic" pp. 3 ve 10'da geçiyor; p. 4'te bu ifadeler yok. |
| Değerlendirme olmadan anlatıyı çıkar sahiplerinin belirlemesi riski | p. 1 | Doğru |

### 4.4. Resmî belgeler

Resmî belgelerin künye alanları belgelerin kendisinden alındı. Kaynaklar şunlardır: rapor kapakları, Resmî Gazete sayfa başlıkları ve kanun metinleri (`data/raw/`).

| Anahtar | Kaynak | Doğrulanan alanlar | Not |
|---|---|---|---|
| vhr2016 | `data/raw/hmb/Vergi-Harcamalar_-Raporu-2016-.pdf` | Yazar: Maliye Bakanlığı. Yıl: 2016. URL | PDF'de kapak sayfası yok. Yayıncı Bakan sunuşundan ("Maliye Bakanı"), yıl metinden ("2016 yılında yayınladığımız bu raporda") alındı. |
| vhr2017 | kapak: "T.C. Maliye Bakanlığı Gelir Politikaları Genel Müdürlüğü … Ankara, 2017" | Yazar, yayıncı, yıl, URL | PDF oluşturma tarihi 2018-03-08; künyede kapaktaki baskı yılı kullanıldı. |
| vhr2018 | kapak: "T.C. Hazine ve Maliye Bakanlığı Gelir Düzenlemeleri Genel Müdürlüğü … Ankara, 2018" | Yazar, yayıncı, yıl, URL | Kaynak envanterindeki birim adı ("Gelir Politikaları") kapakla uyuşmuyordu; kapaktaki ad kullanıldı. |
| vhr2020–vhr2025 | kapak: "Gelir İdaresi Başkanlığı, <yıl> Yılı Vergi Harcamaları Raporu, Gelir Bütçesi Daire Başkanlığı, Ankara, <yıl>" | Yazar, yıl, URL | Kapaktaki baskı yılı başlıktaki yılla aynı. PDF oluşturma tarihleri bazı yıllarda sonraki yıla düşüyor (ör. 2025 raporu: 2026-02-26). |
| law5018 | Hazine ve Maliye Bakanlığı'nın konsolide metni (`data/raw/law/`) | Kanun No. 5018; kabul 10/12/2003; R.G. 24/12/2003, Sayı 25326; md. 15/2 (PDF s. 10); md. 18/2-c (PDF s. 12) | Konsolide metin 6562 sayılı Kanun'a (2014) kadarki değişiklikleri içeriyor. **mevzuat.gov.tr erişime kapalıydı** (proxy 403). 2014 sonrası değişiklikler resmî güncel metinle karşılaştırılamadı; bu durum makalede dipnotla belirtildi. |
| law7156 | `20181231M1-1.htm`, `20181231M1-B221.pdf` | Kanun No. 7156; kabul 22/12/2018; R.G. 31/12/2018, Sayı 30642 (Mükerrer); cetveller s. 1929–2077; vergi harcaması tablosu s. 1973 | Sayfa numaraları PDF başlıklarından okundu. |
| law7197 | `20191231M1-1.htm`, `20191231-B226.pdf` | Kanun No. 7197; kabul 21/12/2019; R.G. 31/12/2019, Sayı 30995 (Mükerrer); cetveller s. 1930–2079; vergi harcaması tablosu s. 1973 | Aynı |

Raporlara verilen tüm PDF sayfa atıfları, alıntılanan Türkçe ifadelerin o sayfada geçip geçmediğine bakılarak kontrol edildi. 2016, 2018, 2020 ve 2025 raporlarına verilen 14 farklı sayfa atfı kontrol edildi. **Hepsi doğru çıktı.** Kontrol edilen ifadelerden bazıları:

- 2025 raporu: "gerçekleşme tutarları" (s. 14); "çok iyi / iyi / yaklaşık" (s. 15); "31/12/2028 tarihine kadar" (s. 104); "uygulanabilir en iyi hesaplama yönteminin kullanılması benimsenmiştir" (s. 303)
- 2016 raporu: "doğrudan kamu harcamaları yapılması yerine" (s. 71); "yeni belirleme" ve %1,34 / %4,08 (ss. 284–290)
- 2018 raporu: 178.696 milyon TL (ss. 296, 298)

## 5. Doğrulanamayan veya kısmen doğrulanan kayıtlar

| Kayıt | Eksik veya belirsiz bilgi | Yapılan |
|---|---|---|
| haldenwang2021 | Bölüm sayfa aralığı (kaynaklar çelişiyor) | Sayfa yazılmadı |
| doganalp2020 | Cilt ve sayı | Yazılmadı |
| dziemianowicz2017 | Son sayfa; 2017/2018 yıl belirsizliği | Yalnız ilk sayfa yazıldı; sayı yılı kullanıldı |
| law5018 | 2014 sonrası değişiklikler (resmî güncel metne erişilemedi) | Makalede dipnotla belirtildi |
| vhr2016 | Kapak sayfası yok | Yayıncı ve yıl metinden alındı |
| Vergi Harcamaları Raporu 2019 | Bulunamadı | Kaynakçada yok; makalede açıkça belirtildi |
| İçerik düzeyi | Surrey, Burman, Altshuler ve Dietz, Howard, Mettler, Zee vd., Van Parys ve James, Klemm ve Van Parys tam metinden okunmadı. Bu kaynaklar yalnız genel ve bilinen argümanları için anılıyor. Türk çalışmaları (Eriçok, Yoruldu, Doğanalp, Işıkman ve Doğan) özetlerine dayanılarak aktarıldı; bu durum metinde belirtildi. | Değişiklik yapılmadı |

## 6. Metin düzenlemeleri (gönderim sürümü)

- Resmî belgelere yapılan tüm düz metin anılar APA atıflarına çevrildi. Örnek: "(VHR2025, PDF p. 23)" → (Gelir İdaresi Başkanlığı, 2025, PDF p. 23).
- 5018 sayılı Kanun'un 15. ve 18/2-c maddeleri Bölüm 3'te açıkça yazıldı. Girişteki madde 15 atfı genel bir kanun atfına dönüştürüldü.
- Metin içindeki dosya yolları (`scripts/...`, `data/...`) çıkarıldı ve "replication package" ifadesiyle değiştirildi. Dosya listesi "Data and code availability" bölümünde.
- Kaynakça APA sırasına göre ekten önce yerleştirildi.
- Tablolar ve şekiller makalenin sonuna eklendi. Tablo ve şekil bölümü yatay sayfalarda. Biçimlendirme yalnızca baskı içindir; hiçbir değer yeniden hesaplanmadı (`nan` → "–", binlik ayırıcı).
- "Draft" tarihi kaldırıldı. Yazar bilgisi ve depo adresi ayrı başlık sayfasında. Finansman, çıkar çatışması ve yapay zekâ beyanı alanları yazarın doldurması için boş bırakıldı.
- `scripts/12_number_trace.py` düzenlemelerden sonra yeniden çalıştırıldı: **75/75 PASS**.

## 7. Çıktılar

| Dosya | İçerik |
|---|---|
| `paper/submission/manuscript_anonymised.docx` (ve `.md`) | Kör hakemlik için makale: metin, APA 7 kaynakça, 16 tablo (1–13 ile 3b, 10b, 11b), 4 şekil, Ek A1 |
| `paper/submission/title_page.docx` (ve `.md`) | Başlık sayfası, depo bağlantısı, beyanlar |
| `paper/references.bib` | 36 doğrulanmış kayıt |
| `paper/csl/apa.csl` | APA 7 stil dosyası |
