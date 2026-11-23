# PROJE DURUMU

**Proje:** Evaluability of Tax Expenditures in Türkiye: An Assessment of Official Reporting Against the IMF Evaluation Framework
**Son güncelleme:** 23 Kasım 2026

## 0. Güncel durum (özet)

**Durum:** Kaynak taraması, veri çıkarımı ve mutabakatı, kodlama, analiz, makale taslağı ve iki denetim tamamlandı. Bu dosyanın 1–8. bölümleri, analizden önce yazılmış **analiz öncesi fizibilite notudur** ve tarihsel kayıt olarak korunuyor. Güncel sonuçlar §0, §9 ve §10'dadır. Fizibilite notundaki bir ifade sonradan değiştiyse yanında *[güncellendi]* notu var.

**Belgeler ve kapsam**
- **Vergi Harcamaları Raporları:** 2016, 2017, 2018, 2020, 2021, 2022, 2023, 2024, 2025 (9 rapor) analiz edildi.
- **2019 Vergi Harcamaları Raporu:** bulunamadı. Bu raporun gerçekleşme yılı 2018 olurdu; bu nedenle **2018 gerçekleşme yılı rapor serisinde eksik**. 2019 gerçekleşme yılı eksik değildir: 2020 raporu 2019 verileriyle hesaplanmış "gerçekleşme" tahmini veriyor (Tablo 2, PDF s. 308: 177.601 milyon TL; PDF s. 23, 307).
- **2019 bütçe kanunu eki:** bulundu (7156 sayılı Kanun, RG 31.12.2018/30642 Mükerrer, RG s. 1973 = cetvel PDF s. 45). 2019–2021 bütçe tahminleri, vergi türü toplamları, TL. Bütün satırlar 2018 raporunun Tablo 2 (PDF s. 296) ve Tablo 3 (PDF s. 298) değerleriyle milyon TL'ye yuvarlamayla aynı. 2018 raporu da bu tutarların 2019–2021 bütçe kanununa eklendiğini yazıyor (PDF s. 296). Yani aynı tahmin iki belgede yayımlanmış ve **tek tahmin** sayıldı. Bu bir 2019 tahminidir, 2019 gerçekleşmesi değildir.
- **2020 bütçe kanunu eki:** bulundu (7197 sayılı Kanun, RG 31.12.2019/30995 Mükerrer, RG s. 1973 = cetvel PDF s. 44). 2020–2022 bütçe tahminleri. Bu değerler analiz edilen hiçbir raporda geçmiyor ve hangi rapora dayandıklarını gösteren bir belge yok. Bu nedenle yalnızca "2020 bütçe kanunu ekindeki 2020–2022 tahminleri" olarak kullanılıyor.
- **Panele dahil edilmedi:** Bütçe ekleri kalem bazında tutar vermiyor; yalnızca vergi türü toplamları içeriyor. Bu nedenle `data/tax_expenditure_panel.csv` (rapor-kalem-yıl) paneline eklenmedi. Ayrı bir seri olarak tutuluyor (`data/interim/budget_law_annexes.csv`) ve yalnızca Tablo 3'teki aynı-yıl karşılaştırmalarında kullanılıyor.

**Ana çıktılar:** `paper/manuscript.md`; `outputs/tables/tables.md` (Tablo 1–13); `outputs/figures/fig1–fig4`; `outputs/tables/manuscript_number_trace.csv` (metindeki her sayının kaynağı); `outputs/tables/budget_law_vs_report_estimates_2019_2020.csv`.

**Açık işler:** §10.5'te. **İkinci denetim kaydı:** §10.6.

---

> **Aşağıdaki 1–8. bölümler: ANALİZ ÖNCESİ FİZİBİLİTE NOTU (22 Kasım 2026).** Analizden önce yazılmıştır, tarihsel kayıt olarak korunuyor. Güncel durum için §0, §9 ve §10'a bakın.

## 1. Hangi yılların hangi resmî belgeleri bulundu?

Ayrıntılı envanter: `data/source_inventory.csv` (kurum, başlık, belge türü, yayın yılı, kapsadığı mali yıllar, kalıcı URL, erişim tarihi, yerel dosya yolu, sayfa sayısı, kapsam, durum).

| Belge | Kurum | Yayın (PDF oluşturma tarihi) | Gerçekleşme yılı (ek sütun 1) | Tahmin yılları | Durum |
|---|---|---|---|---|---|
| Vergi Harcamaları Raporu 2007 | Maliye Bakanlığı | 2007-10 | (yöntem temeli) | – | indirildi; yalnızca bağlam |
| VHR 2016 (+ EK I-6, EK I-7 ayrı dosyalar) | Maliye Bakanlığı GPGM | 2016-10-12 | 2015 | 2016–2019 | indirildi |
| VHR 2017 | Maliye Bakanlığı GPGM | 2018-03-08 | 2016 | 2017–2020 | indirildi |
| VHR 2018 | Hazine ve Maliye Bakanlığı GPGM | 2018-10-18 | 2017 | 2018–2021 | indirildi |
| VHR 2019 | – | – | (2018) | – | **bulunamadı** |
| VHR 2020 | HMB Gelir İdaresi Başkanlığı | 2020-11-19 | 2019 | 2020–2023 | indirildi |
| VHR 2021 | GİB | 2022-01-28 | 2020 | 2021–2024 | indirildi |
| VHR 2022 | GİB | 2023-03-23 | 2021 | 2022–2025 | indirildi |
| VHR 2023 | GİB | 2024-02-22 | 2022 | 2023–2026 | indirildi |
| VHR 2024 | GİB | 2025-03-04 | 2023 | 2024–2027 | indirildi |
| VHR 2025 (en güncel) | GİB | 2026-02-26 | 2024 | 2025–2028 | indirildi |
| IMF How-To Note 22/05 (Beer, Benedek, Erard, Loeprick) | IMF FAD | 2022-11 | – | – | indirildi; DOI 10.5089/9798400221507.061 CrossRef ile doğrulandı |

Notlar:
- **2019 raporu bulunamadı.** HMB arşiv sayfası yalnızca 2007, 2016, 2017, 2018 raporlarını; GİB sayfası 2020–2025 raporlarını listeliyor. GİB dosya sunucusunda 2019 ve 2026 adları HTTP 400 döndürüyor. İkincil bir kaynakta 2019 raporundan söz edilmesi, resmî bir kopyaya ulaşılamadığı için kullanılmadı. Sonuç: **2018 gerçekleşme yılı serisi eksiktir.** *[güncellendi: 2019 gerçekleşme tahmini 2020 raporunda var; bkz. §0.]*
- **En güncel rapor 2025 raporudur** (Şubat 2026). 2026 raporu henüz yayımlanmamış görünüyor (dosya adı sunucuda yok, listeleme sayfasında yok).
- Kullanıcının verdiği `teknoloji.gib.gov.tr` adresi 404 döndürdü; aynı belge `cdn.gib.gov.tr` üzerinden alındı (envanterde kalıcı URL olarak bu adres kayıtlı).
- **Bütçe kanunu ekleri** ayrı belge türü olarak envantere girildi ancak ayrıca indirilmedi. Raporlar bütçe kanununa eklenen vergi türü toplamlarını kendi tablolarında yeniden basıyor (2016 Tablo 4.4; 2017 Tablo 2; 2018 Tablo 2; 2020–2025 Tablo 1). Analizde bu rakamlar `budget_law` serisi olarak ayrı tutulacak; rapor tutarlarıyla toplanmayacak (çift sayım yok). 2025 raporundaki bütçe kanunu tutarları raporun kendi tahmin sütunlarıyla birebir aynıdır (2026: 3.597.140 milyon TL). *[güncellendi: 2019 ve 2020 bütçe kanunu ekleri Resmî Gazete'den indirildi ve doğrulandı; 2021–2024 bütçe tahminleri hâlâ raporların yeniden bastığı tablolardan alınıyor; bkz. §0, §10.]*
- **Sanayi ve Teknoloji Bakanlığı** sitesi otomatik erişime “The requested URL was rejected” yanıtı veriyor; erişim kısıtı aşılmaya çalışılmadı. Bu kaynak elle indirilip `data/raw/sanayi/` klasörüne konursa eklenebilir. Ancak teşvik belgesi istatistikleri **öngörülen (planlanan)** yatırım ve istihdamı gösterir; ne vergi harcaması maliyeti ne de nedensel etki ölçüsüdür. Bu nedenle çalışmanın ana sorusu için zorunlu değildir; yalnızca “raporlarda çıktı/gösterge bilgisi yok, ama başka kurumlarda kısmi bilgi var” tespitini desteklemek için kullanılabilir.
- **GTED, OECD, TÜİK:** Oranlar için raporların kendi resmî tabloları (GSYH’ye ve vergi gelirlerine oranlar) yeterli olduğundan ayrıca payda verisi gerekmiyor. GTED yalnızca uluslararası bağlam için (Türkiye’nin GTED’deki kaydı) isteğe bağlıdır.

## 2. Veri çıkarımı ve mutabakat (yapılanlar)

- Ek I-1…I-5 tabloları (madde, açıklama, 5 yıl tutar, tahmin kalitesi, hücre durumu) 9 rapordan çıkarıldı: toplam **2.112 rapor-kalem satırı**, panelde **10.560 rapor-kalem-yıl gözlemi** (`data/tax_expenditure_panel.csv`). Her satırda kaynak PDF sayfası, URL ve yerel dosya yolu var.
- Teknik sorunlar ve çözümler: 2020–2023 eklerinde tablolar 90° döndürülmüş; 2017’de bozuk karakter kodlaması; 2018 ekinde fontlarda Unicode eşlemesi yok (glif eşlemesi öğrenilerek çözüldü, `scripts/00_decode_2018_glyphs.py`); 2016’da MTV ve ÖİV sayfaları otomatik çıkarıcıdan kaçtı ve 5 satır elle aktarıldı (`data/interim/manual_rows_VHR2016.csv`, sayfa notlu).
- **Mutabakat 1 (kalem toplamı ↔ alt tablo GENEL TOPLAM):** basılı GENEL TOPLAM satırı olan 402 alt tablo-yıl karşılaştırmasının 395’i ±5 bin TL içinde (yuvarlama); 93 alt tablo-yılda (çoğu tek satırlık alt tablolar) basılı toplam yok. Kalan farkların hepsi kaynağına kadar izlendi (`outputs/tables/official_document_inconsistencies.csv`).
- **Mutabakat 2 (ek toplamları ↔ rapor gövdesindeki toplam tablosu):** 2016, 2018, 2020–2025’te genel toplamlar ±0,5 milyon TL içinde uyuşuyor. 2017 raporunda gövdede toplam tutar tablosu yok (yalnızca bütçe kanunu tahmini).
- **Resmî belgelerin kendi iç tutarsızlıkları** (çıkarım hatası değil; belgede doğrulandı):
  - VHR2020 Tablo 2: GV 2020 = 78.110 milyon TL; ekin alt toplamları 77.910 milyon TL (200 milyonluk fark, büyük olasılıkla dizgi hatası).
  - VHR2022 Ek I-3 sıra 48 (KDV Geç. Md. 39): 2025 sütununda “-” basılı, ama alt tablo toplamı bu kalem için 1.167 milyon TL içeriyor.
  - VHR2023 Ek I-1 sıra 49 (GVK 89/3): kalem basılı, ancak alt tablo toplamı ve gövde tablosu bu kalemi içermiyor (2,2–9,4 milyon TL).
  - VHR2023: 6111 s. K. Geç. Md. 16 kalemi 2026 için “-”; gövde KDV 2026 rakamı ise 1.292 milyon TL fazladan içeriyor.
  - VHR2017 GV ana tablo 2016: 60 bin TL’lik açıklanamayan fark.

## 3. Hangi kalemler yıllar arasında karşılaştırılabilir?

- Kalemler raporlar arasında **vergi türü + alt tablo (ana kanun/diğer kanunlar) + normalize edilmiş yasal dayanak + açıklama benzerliği** ile eşleştirildi (`scripts/02_build_panel.py`). Sonuç: **338 benzersiz kalem kimliği**. Eşleşme yöntemi her satırda kayıtlı (`link_method`): 2020–2025’te kalemlerin %85–97’si “yasal dayanak + açıklama” ile eşleşiyor; zayıf eşleşmeler (yalnızca açıklama / yalnızca madde) elle örneklem denetiminden geçirildi, büyük çoğunluğu doğru; yasa numarası çelişen eşleşmeler engellendi. Kalem eşleştirmesi bir araştırma kurgusudur; kalem düzeyinde zaman serisi analizleri yalnızca güçlü eşleşmelerle yapılacak.
- **En karşılaştırılabilir dönem: 2020–2025 raporları (GİB, gerçekleşme yılları 2019–2024).** Aynı kurum, aynı ek yapısı (Ek I-1…I-5, II, III, IV), aynı vergi türü kapsamı (GV, KV, KDV, ÖTV, BSMV, MTV, ÖİV) ve aynı gövde tabloları.
- **2016–2018 raporları** aynı yöntem ailesinde (“yeni belirleme”) ve aynı yedi vergiyi kapsıyor; karşılaştırılabilir ama aşağıdaki kırılmalar dikkate alınmalı.
- Rapor başına kalem sayısı: 2016: 193; 2017: 223; 2018: 233; 2020: 252; 2021: 252; 2022: 256; 2023: 236; 2024: 236; 2025: 231. Bu değişim, kapsam değişikliği ile yeni/kaldırılan düzenlemeleri birlikte yansıtır; ayrıştırma analiz aşamasında yapılacak.

## 4. Adlar, kapsam, sınıflandırma ve yöntemde değişiklikler

1. **2016’da seri kırılması:** 2016 raporu iki seri basıyor: (a) 2007 yöntemine dayanıp nominal büyüklüklerle büyütülen eski bütçe eki serisi (2015: 26.113 milyon TL, GSYH’nin %1,34’ü; Tablo 4.4–4.8) ve (b) “yeni belirlemeye göre” seri (2015: 79.582 milyon TL, GSYH’nin %4,08’i; Tablo 4.10–4.12). İkisi birleştirilemez. 2008–2015 bütçe eki tutarları bu yüzden kapsam dışı.
2. **Vergi türü gruplaması:** 2016 gövde tablosu BSMV, MTV, ÖİV’yi ayrı satırlarda ve “diğer kanunlar” kalemlerini ana vergilerin içinde veriyor; 2018’den itibaren BSMV+MTV+ÖİV “Diğer Kanunlar” satırında toplanıyor. Analizde vergi türleri ek tablolardan yeniden kurulduğu için karşılaştırılabilirlik sağlanabiliyor.
3. **Kapsam:** Yalnızca 2016 raporunun eki damga vergisi (32), harçlar (99), veraset ve intikal (19), emlak (47), belediye gelirleri (34) hükümlerini **tutar vermeden** listeliyor; sonraki raporlar bu vergileri hiç listelemiyor. Savunma/askerî amaçlı istisnalar ve uluslararası anlaşmalara bağlı uygulamalar (ör. diplomat muaflığı) tüm raporlarda kapsam dışı.
4. **Anlatı (Bölüm 2) kapsamı:** 2016, 2018, 2020–2025 raporları her madde için anlatı içeriyor (yasa metni, gerekçe/amaç cümlesi, yararlananlar, vergi harcaması niteliği, hesaplama yöntemi). **2017 raporu yalnızca yeni vergi harcamalarını** anlatıyor; mevcut kalemler için anlatı yok.
5. **Kurumsal değişiklik:** 2016–2018 Maliye/HMB Gelir Politikaları Genel Müdürlüğü; 2020’den itibaren Gelir İdaresi Başkanlığı (Gelir Bütçesi Daire Başkanlığı).
6. **Başlık yılı ile tutar yılı ilişkisi değişti:** 2018–2022 raporlarının özet cümleleri gerçekleşme yılını (ör. “2021 yılında %5,85”) öne çıkarırken 2023–2025 raporları rapor yılının **tahmin** tutarını öne çıkarıyor (ör. 2025 raporu: “2025 yılında 3.170,3 milyar TL, GSYH’nin %5,1’i”), oysa bu raporlarda gerçekleşme yılı bir önceki yıldır (2024: GSYH’nin %6,17’si).
7. **Tahmin dönemi makro temeli:** 2016–2018’de “nominal GSYH artışı”/YEP hedefleri; 2020 sonrası OVP makro çerçevesi ve “son vergisel düzenlemeler”.

## 5. “Gerçekleşme” ve “tahmin” ne anlama geliyor?

- Ek tablo başlıkları ilk sütunu “gerçekleşme” diye etiketlemiyor (2016’da tüm sütunların üstünde “Tahmin (Bin TL)”, 2017’de “Tahmin (*)”, GİB raporlarında yalnızca yıllar ve “(Bin TL)”). Anlam gövde metninden çıkıyor: ör. 2025 raporu: “Vazgeçilen vergi tutarları 2024 yılı verilerine göre hesaplanmış, 2025-2028 yıllarına ilişkin tutarlar ise Orta Vadeli Program kapsamında duyurulan makroekonomik hedefler baz alınarak tahmin edilmiştir.”
- Dolayısıyla **“gerçekleşme”**, o yılın beyanname ve kurum verileriyle yapılmış *statik vazgeçilen gelir hesaplamasıdır* (ölçülmüş bir harcama değil, veriye dayalı ex post bir tahmindir). **“Tahmin”** ise gerçekleşme tutarlarının makro büyüklüklerle (ve bilinen düzenleme değişiklikleriyle) ileriye taşınmasıdır; 2016 raporu bunu açıkça yazıyor (“2015 gerçekleşme rakamları nominal GSYH artışı oranında artırılarak”; bu nedenle tahmin yıllarında GSYH’ye oran sabit kalıyor).
- **Yöntem:** Tüm raporlar vazgeçilen gelir (revenue forgone) yöntemini ve “mükellef davranışında ya da ekonomik aktivitede değişiklik olmayacağı” varsayımını kullandığını belirtiyor. Bu tutarlar **politika etkisi değildir**; kaldırılma halinde elde edilecek gelir de değildir. Makalede böyle sunulmayacak.
- **Tahmin kalitesi:** Tek tanım, “kullanılan verinin güvenirliliği ve kapsamına göre tespiti yapılan vergi harcaması tutarlarının ‘çok iyi’, ‘iyi’ ya da ‘yaklaşık’ şeklinde sınıflandırılan tahmin kalitesi” cümlesidir (2025 raporu, Giriş, PDF s. 15; 2018 ve 2020–2024 raporlarında aynı cümle; 2016 raporunda benzer biçimde “kullanılan verinin güvenirliliği ve kalitesine göre ‘çok iyi’, ‘iyi’ ya da ‘yaklaşık’ ifadeleri kullanılarak” denmekte; 2017 raporunda tanım bulunamadı). Hangi ölçütle hangi etikete karar verildiği, belirsizlik aralığı veya standart hata **açıklanmıyor**. Bu bir veri bulgusudur ve 4. ölçütün kodlanmasında kullanılacak.
- Gerçekleşme yılı hücre durumları (rapor başına kalem): tahmin edilmiş 139–199; “Veri temin edilememiştir” 22–35; “Vergi harcaması oluşmamıştır” 9–23; “Yeni uygulama” 0–16; başka kalem içinde 1–10. Bu dağılım, kalem düzeyinde maliyet bilgisinin ne ölçüde var olduğunu doğrudan gösteriyor.

## 6. Hangi IMF ölçütleri kodlanabilir, hangileri için bilgi yok?

IMF notu (How-To Note 22/05) puanlı bir kontrol listesi vermiyor; değerlendirme sürecini (amaç beyanı, değişim kuramı, önceden tanımlı göstergeler, maliyet ve tahmin güvenilirliği, yararlanıcılar, ek katkı/karşı-olgusal, alternatif araçlar, periyodik değerlendirme ve yayımlama) anlatıyor. Bizim 9 ölçütümüz bu içeriğin belgeye uygulanabilir bir operasyonelleştirmesidir; eşleştirme tablosu `data/codebook.md` içinde verilecek. Notun kendisi kurumsal bir rehberdir, hakemli yayın değildir.

| # | Ölçüt | Bilgi kaynağı | Kodlanabilirlik (ön inceleme) |
|---|---|---|---|
| 1 | Politika amacı | Bölüm 2 anlatıları (“...amacıyla düzenlenmiştir” türü cümleler) | **Kodlanabilir.** Çoğu maddede genel bir gerekçe cümlesi var; ölçülebilir hedef görülmedi. |
| 2 | Yararlanıcı grup/sektör/faaliyet | Anlatılar (uygunluk koşulları), Ek IV (en büyük kalemlerin NACE dağılımı) | **Kodlanabilir.** Tanım düzeyinde bilgi var; yararlanıcı sayısı ön taramada bulunamadı. |
| 3 | Kalem düzeyi maliyet tahmini | Ek I | **Tam kodlanabilir**, tüm rapor-kalem-yıllar için (hücre durumundan). |
| 4 | Tahmin kalitesi/belirsizlik | Ek I kalite sütunu, yöntem metni | **Kodlanabilir.** Etiket var, tanımı ve belirsizlik ölçüsü yok. |
| 5 | Beklenen politika çıktısı | Anlatılar | Kodlanabilir; ön taramada çoğunlukla genel ifadeler (“istihdamı artırmak” vb.). |
| 6 | Gösterge/gerçekleşen çıktı verisi | Tüm metin | Kodlanabilir; ön anahtar sözcük taramasında yararlanıcı sayısı, gösterge veya çıktı verisi bulunamadı (kesinleştirilecek). |
| 7 | Ek katkı/karşı-olgusal | Tüm metin | Kodlanabilir; ön taramada “etki analizi” geçmiyor (kesinleştirilecek). |
| 8 | Maliyet-etkinlik/alternatif araç | Tüm metin | Kodlanabilir; ön taramada “maliyet-etkinlik/fayda-maliyet” geçmiyor; “harcama denkliği” yalnızca yöntem tanımında. |
| 9 | Düzenli gözden geçirme (sona erme, yenileme, değerlendirme) | Anlatılardaki yasa metinleri | Kısmen: bazı hükümlerde yasal süre/bitiş tarihi var (yasa metninden); değerlendirmeye bağlı yenileme ya da gözden geçirme ön taramada yok. |

Önemli ayrım: “belgede yok” (0) ile “politikada yok” aynı şey değildir. Raporlarda bilgi bulunmaması, ilgili kurumların bu bilgiyi hiç üretmediği anlamına gelmez; kodlama yalnızca **resmî raporlama** hakkındadır. Bağımsız ikinci kodlayıcı yoktur; bu açıkça belirtilecek ve tekrar kodlama bağımsız kodlama gibi sunulmayacak.

## 7. Uygulanabilir dönem ve kapsam (öneri)

- **Belgeler:** 2016, 2017, 2018, 2020, 2021, 2022, 2023, 2024, 2025 Vergi Harcamaları Raporları (9 rapor).
- **Mali yıllar:** gerçekleşme yılları 2015, 2016, 2017, 2019–2024 (2018 eksik); tahminler 2016–2028. Rapor “vintage”ları çakıştığı için aynı yıl için tahmin ile sonraki raporun gerçekleşmesi karşılaştırılabilir (ör. 2023 raporunun 2023 tahmini ↔ 2024 raporunun 2023 gerçekleşmesi). Bu bir tahmin revizyonu analizidir, etkililik ölçüsü değildir.
- **Analiz birimleri:**
  - Ölçüt 3–4 ve hücre durumları: **rapor × kalem × yıl** (tüm panel).
  - Ölçüt 1, 2, 5–9: **rapor × anlatı bölümü (madde)**, kalemlere yasal dayanakla bağlanarak. Anlatılar raporlar arasında büyük ölçüde aynen tekrarlandığı için tam kodlama en güncel (2025) ve ilk (2016) raporlarda yapılacak; ara raporlarda metin karşılaştırmasıyla değişen bölümler ayrıca kodlanacak, değişmeyenlerde kodun taşındığı açıkça işaretlenecek.
- **Nicel göstergeler:** Raporların kendi resmî oranları (GSYH’ye ve genel bütçe vergi gelirlerine oran). Nominal TL karşılaştırması yapılmayacak (yüksek enflasyon dönemi; güvenilir bir deflatörle uzun dönem karşılaştırma yerine oranlar kullanılacak). Vergi türü dağılımları ek tablolardan; fonksiyonel sınıflandırma (Ek II) yalnızca 2020–2025’te tutarlı biçimde çıkarılabilirse kullanılacak.
- **Kapsam dışı:** etki/etkililik tahmini; 2008–2015 bütçe eki serisi (yöntem kırılması); Sanayi ve Teknoloji Bakanlığı verileri (erişilemedi, ayrıca maliyet ölçüsü değil).

## 8. Sıradaki adımlar (fizibilite aşamasındaki plan — hepsi tamamlandı)

1. ✅ `data/codebook.md` ve karar günlüğü; IMF ölçüt eşleştirme tablosu (makale Tablo A1).
2. ✅ Anlatı bölümlerinin çıkarımı ve kalem-bölüm bağlantısı; 9 ölçütün sayfa referanslı kodlanması. *[Uygulamada kodlama bütün raporlara kurallarla uygulandı, ardından gözden geçirildi; bkz. kod kitabı §4.]*
3. ✅ Literatür taraması ve `paper/references.bib` (26 kayıt, CrossRef ile doğrulandı).
4. ✅ Tablolar ve şekiller, makale, sınırlılıklar, temiz yeniden çalıştırma. Güncel açık işler §10.5'te.

---

## 9. Tamamlanma durumu (analiz sonrası güncelleme, 22 Kasım 2026)

Yukarıdaki fizibilite bölümleri analiz öncesinde yazıldı; içerikleri korunuyor, sonradan değişen ifadelerin yanına *[güncellendi]* notu eklendi.

**Yapılanlar**
- Kod kitabı ve karar günlüğü: `data/codebook.md`, `data/coding/decision_log.md` (D1–D10), elle düzeltmeler `data/coding/overrides.csv`.
- Anlatı bölümleri: 683 rapor-bölüm (2016: 74, 2017: 22, 2018: 76, 2020–2025: 82–87); her kodun kanıt cümlesi ve PDF sayfası `data/coding/section_codes.csv` içinde.
- Kalem-bölüm eşleştirmesi: 2020–2025'te kalemlerin %74–84'ü bir anlatı bölümüne bağlanıyor; BSMV, MTV ve ÖİV kalemleri için raporlarda anlatı yok.
- Tablolar ve şekiller: `outputs/tables/tables.md`, `outputs/figures/fig1–fig4`. Tam yeniden çalıştırma (`run_all.sh`) art arda iki kez aynı tabloları üretti.
- Literatür: 26 kaynak (ilk sürümde 27; kullanılmayan biri §10'da çıkarıldı), DOI'ler CrossRef ile doğrulandı; her kaynağın neye dayanılarak kullanıldığı (tam metin / özet / üst veri) `data/literature/literature_notes.md` dosyasında.
- Makale (İngilizce): `paper/manuscript.md` (güncel sözcük sayıları §10.4'te); sınırlılıklar: `paper/limitations_and_data_gaps.md`.

**Başlıca bulgular (güncel; yalnızca analiz edilen 9 raporun — 2016–2018 ve 2020–2025 — bilgisine ilişkin)**
- Maliyet tahmini olan kalemlerin payı (uygulanabilir kalemler içinde): 2016–2018 raporlarında %72,1–75,5; 2020 raporunda %79,5, 2025 raporunda %88,1. Tüm zincir boyunca güçlü bağlı ortak kalemlerde 2020'de %82,1, 2025'te %87,2 (Tablo 4, 12). Üç ya da daha fazla raporda görünen 284 kalemden 25'i, göründüğü hiçbir raporda tahmin edilmemiş.
- Tahmin kalitesi etiketleri tanımsız. "Çok iyi" etiketli kalemlerin tutar payı 2016–2018 raporlarında %57,8–61,0, 2020 raporunda %61,5, 2025 raporunda %14,2; 2025'te tutarın %42,5'i "yaklaşık" etiketli (Tablo 5).
- Aynı yıl karşılaştırmaları (Tablo 3): sonraki raporun gerçekleşme tahmini ilk tahminden her karşılaştırmada %5,7–35,7 yüksek. Bütçe kanunu tahminine göre fark 2019'da −%0,6, 2020'de +%21,4, 2021–2024'te +%24,5 ile +%162,1 arasında. 2019 için ilk tahmin yok (2019 raporu bulunamadı).
- Amaç: 2025'te bölümlerin %51'inde kaleme özgü, %23'ünde genel bir amaç ifadesi var. Kalem düzeyinde açık amaç payı alt sınırda %10,0, üst sınırda %48,1 (Tablo 11). Beklenen çıktı hiçbir bölümde ölçülebilir biçimde tanımlanmamış. Yararlanıcı sayısı, gösterge verisi, ek katkı (karşı-olgusal) analizi, maliyet-etkinlik değerlendirmesi ve gözden geçirme sonucu analiz edilen raporların hiçbirinde yok. Bölümlerin yaklaşık yarısında yalnızca yasal süre sınırı görülüyor.

**Açık kalanlar**
- 2019 raporu bulunamadı (2019 ve 2020 bütçe kanunu ekleri ise bulundu; bkz. §0). Sanayi ve Teknoloji Bakanlığı verilerine erişilemedi.
- Bağımsız ikinci kodlayıcı yok. Dergiye göndermeden önce bağımsız bir kodlayıcıyla örneklem üzerinde güvenilirlik denetimi önerilir.
- Bazı Türkçe kaynaklar yalnızca özetten değerlendirildi. Gönderim öncesinde tam metinleri okunmalı.


---

## 10. Denetim (23 Kasım 2026)

### 10.1 2019 araması (erişim tarihi: 22–23 Kasım 2026)

| Aranan | Kaynak / bağlantı | Sonuç |
|---|---|---|
| 2019 Vergi Harcamaları Raporu | HMB arşivi https://www.hmb.gov.tr/gelir-duzenlemeleri-genel-mudurlugu-vergi-harcama-raporlari | Yalnızca 2007, 2016, 2017, 2018 raporları listeleniyor |
| | GİB rapor sayfası https://gib.gov.tr/kurumsal/planlar-ve-raporlar/vergi-harcamalari-raporlari | Yalnızca 2020–2025 |
| | GİB dosya sunucusu `.../objectKey=arsiv/kurumsal/Vergi_Harcamalari_Raporu_2019.pdf` | HTTP 400 |
| | Eski GİB yolu https://gib.gov.tr/sites/default/files/fileadmin/2019_Ver_har_rapor.pdf | HTTP 404 |
| 2019 bütçe kanunu eki | Resmî Gazete 31.12.2018, sayı 30642 (Mükerrer): 7156 sayılı 2019 Yılı Merkezi Yönetim Bütçe Kanunu, https://www.resmigazete.gov.tr/eskiler/2018/12/20181231M1-1.htm; cetvel dosyası https://www.resmigazete.gov.tr/eskiler/2018/12/20181231M1-B221.pdf | **Bulundu.** PDF s. 13–44: "Vergi Harcamaları Listesi – Vergi harcamalarının kanuni dayanaklarına ilişkin liste" (tutarsız). PDF s. 45 (RG s. 1973): "Vergi Türleri İtibarıyla Toplam Vergi Harcaması Tahminleri (TL)", 2019–2021 |
| 2020 bütçe kanunu eki | Resmî Gazete 31.12.2019, sayı 30995 (Mükerrer): 7197 sayılı Kanun, https://www.resmigazete.gov.tr/eskiler/2019/12/20191231-B226.pdf | **Bulundu.** PDF s. 44 (RG s. 1973), 2020–2022 toplamları |
| SBB | https://www.sbb.gov.tr/wp-content/uploads/2019/01/1-2019ButceKanunu.doc | Yalnız kanun metni; vergi harcaması tablosu yok |

Arama terimleri: "2019 Vergi Harcamaları Raporu", "7156 sayılı 2019 Yılı Merkezi Yönetim Bütçe Kanunu", "vergi harcamaları cetveli", "Vergi Türleri İtibarıyla Toplam Vergi Harcaması Tahminleri", "Bütçe Gerekçesi 2019 vergi harcaması". Arama motoru sonuçları yalnızca adres bulmak için kullanıldı; tüm değerler Resmî Gazete PDF'lerinden okundu.

**2019 bütçe eki ve 2018 raporu.** Ek taranmış görüntü olduğundan değerler OCR (Tesseract, Türkçe) ve 200 dpi görüntünün gözle okunmasıyla aktarıldı (`data/interim/budget_law_annexes.csv`). 2019 için toplam 178.695.912.831 TL (GV 68.267.364.779; KV 28.030.970.717; KDV 49.796.734.881; ÖTV 24.903.208.169; Diğer Kanunlar 7.697.634.285). Satır toplamları basılı toplamla 0–1 TL farkla uyuşuyor. 2018 raporu da 2019 tahminini içeriyor: Tablo 2 (bütçe kanununa eklenen tahminler, PDF s. 296) ve Tablo 3 (PDF s. 298), toplam 178.696 milyon TL; ekteki kalem tutarlarının 2019 sütun toplamı 178.695,9 milyon TL. **Üç yılın (2019–2021) tüm satırları 2018 raporuyla milyon TL'ye yuvarlamayla aynıdır** (TL ile milyon TL arasındaki fark yalnızca yuvarlama; en büyük fark 0,5 milyon TL'nin altında). 2018 raporu bu tutarların bütçe kanununa da eklendiğini yazıyor (PDF s. 296). Bu nedenle aynı tahmin iki belgede yayımlanmış ve tek gözlem sayılmıştır (`outputs/tables/budget_law_annex_comparison.csv`, `outputs/tables/budget_law_vs_report_estimates_2019_2020.csv`). Bu rakam bir **tahmindir**: ne 2019 gerçekleşmesidir ne de bağımsız bir bütçe tahmini. 2019 için raporlardaki gerçekleşme tahmini 2020 raporundadır (177.601 milyon TL).

**2020 bütçe eki.** 2020: 195.590.812.732 TL; 2021: 222.661.650.447 TL; 2022: 251.397.082.494 TL. Bu değerler analiz edilen hiçbir raporda yok. 2020 raporunun 2020 tahmininden de farklılar (198.247 milyon TL; +%1,36). Hangi rapora dayandıklarına ilişkin doğrudan kanıt yok; bu nedenle yalnızca 2020 bütçe kanunu ekindeki 2020–2022 bütçe tahminleri olarak adlandırılıyor. *[23 Kasım ikinci denetim: önceki "kayıp 2019 raporu vintajının tek izi" ifadesi kanıtsız olduğu için kaldırıldı.]* Ek yalnızca vergi türü toplamları verdiği için kalem panel şemasına uymuyor; panele eklenmedi, ayrı seri olarak tutuluyor.

**Analize etkisi.** Tablo 3'e 2019 satırı ve 2020 bütçe kanunu tahmini eklendi. Gerçekleşme tahmini bütçe kanunu tahmininin 2019'da %0,6 altında, 2020'de %21,4 üstünde (2021–2024: %24,5–162,1 üstünde). Önceki metindeki "gerçekleşme her yıl bütçe tahminini aşıyor" ifadesi düzeltildi.

### 10.2 Yeniden üretilebilirlik

- Depo geçici bir klasöre kopyalandı, türetilmiş tüm dosyalar silindi ve `run_all.sh` sıfırdan çalıştırıldı. **Hata bulundu:** 2018 glif eşlemesi diğer raporların ek satırlarından öğreniliyor, ama iş akışı bu adımı onlardan önce çalıştırıyordu; temiz çalıştırmada 2018 eki boş çıkıyordu. Sıra düzeltildi. Düzeltmeden sonra temiz çalıştırma panel, kodlar, tablolar ve kaynakçayı bayt düzeyinde aynen üretti.
- Yeni betikler: `scripts/03b_budget_law_annexes.py` (bütçe eki kontrolleri), `scripts/12_number_trace.py`. İkincisi metindeki 70 sayıyı tablo hücrelerinden yeniden hesaplıyor; 70/70 PASS (`outputs/tables/manuscript_number_trace.csv`).
- Sayıların kaynağı: 2.112 = `data/interim/items_by_report.csv` satırı (her raporun her Ek I satırı; 2016'da 5 elle aktarılmış satır dahil); 10.560 = `data/tax_expenditure_panel.csv` satırı (satır başına 5 yıl); 683 = `data/coding/section_codes.csv` satırı (2016: 74, 2017: 22, 2018: 76, 2020–2025: 82–87).

### 10.3 Yöntem ve çıkarım düzeltmeleri

- **Bölüm→kalem aktarımı:** Alt ve üst sınır eklendi (Tablo 11, 11b). 2025'te açık amaçlı kalem payı %48,1 (üst) ile %10,0 (alt) arasında; tutar ağırlıklı %64,8 ile %6,2 arasında. Bölüm düzeyi kodlar ayrıca raporlanıyor (Tablo 7).
- **Zaman karşılaştırması:** İki raporlama dönemi (2016–2018; 2020–2025) ayrıldı. Güçlü bağlı ortak kalemlerde maliyet tahmini payı 2020'de %82,1, 2025'te %87,2; açık amaç payı her iki dönemde de yaklaşık sabit (Tablo 12). "İyileşme" ifadesi yalnızca bu ölçülere bağlandı.
- **"Gerçekleşme":** Raporun kendi tanımıyla (VHR2025 PDF s. 14, 23, 303) aynı yılın verileriyle yapılan statik vazgeçilen gelir tahmini olarak açıklandı.
- **Raporda yok ≠ devlette yok:** Sonuç ve tartışma "the published reporting does not provide / does not allow us to assess" diline çekildi; başka kaynakların incelenmediği açıkça belirtildi.
- **Tek kodlayıcı:** Açıkça belirtildi; uyuşma istatistiği yok.
- **IMF:** Not kurumsal rehber olarak tanıtıldı (BibTeX @techreport, How To Note 22/05). Dokuz ölçüt yazarın operasyonelleştirmesi olarak sunuldu ve IMF unsurları sayfa numaralarıyla Tablo A1'de eşleştirildi.
- **Politika önerileri:** Doğrulanmamış bir veri kaynağını varsayan ifade ("beyannamelerden kolayca") kaldırıldı; yararlanıcı sayıları için önce kaynakların incelenmesi önerildi.
- **Alıntılar:** Tüm doğrudan alıntılar özgün PDF'lerle karşılaştırıldı. Türkçe kaynaklardan yapılanlar özgün Türkçe metin ve çeviri olarak verildi.
- **Kaynakça:** 26 kayıt, hepsi metinde kullanılıyor; kullanılmayan oecd2026 çıkarıldı. Yoruldu (2021) kaydındaki CrossRef "volume 0" hatası kaldırıldı. Tam metni okunmayan kaynaklar yalnızca genel tezleri veya özetleri düzeyinde kullanılıyor.
- **Özet ve metin uzunluğu:** ilk denetimde 197 / 6.756 sözcüktü; güncel sayılar §10.6'da.

### 10.4 Sözcük sayıları

Özet ve metin sözcük sayıları ikinci denetimden sonra yeniden hesaplandı (§10.6).

### 10.5 Açık kalanlar

- 2018 gerçekleşme yılına ait (2019 raporunda yer alacak) kalem düzeyi veri hâlâ yok.
- 2021–2024 bütçe kanunu ekleri ayrıca indirilmedi (değerler raporların yeniden bastığı tablolardan alınıyor). Gönderim öncesinde Resmî Gazete'den aynı yöntemle doğrulanabilir.
- Bağımsız ikinci kodlayıcı yok. Gönderim öncesinde bir örneklem üzerinde bağımsız kodlama ve uyuşma ölçümü önerilir.
- Uluslararası kaynakların tam metinleri ve Türkçe makalelerin tam metinleri okunmalı.
- Sanayi ve Teknoloji Bakanlığı verileri ile Sayıştay raporları incelenmedi.

### 10.6 İkinci denetim (23 Kasım 2026)

**Kaynak doğrulaması**
- 2019 ve 2020 bütçe eki tabloları yerel PDF'lerden (`data/raw/budget_law/20181231M1-B221.pdf` s. 45, `20191231-B226.pdf` s. 44) 200 dpi'da yeniden görüntülenip satır satır okundu. Tüm değerler `data/interim/budget_law_annexes.csv` ile aynı.
- 2018 raporunun Tablo 2 (PDF s. 296) ve Tablo 3 (PDF s. 298) değerleri ve 2020 raporunun Tablo 2'si (PDF s. 308) doğrudan PDF metninden okundu.
- 2018 raporunun "Bu tutarlar aynı zamanda 2019-2021 dönemi Merkezi Yönetim Bütçe Kanununa vergi harcaması tahminleri olarak da eklenmiştir" cümlesi (PDF s. 296) doğrulandı.
- 2020 raporu 2019 sütununu "2019 yılı gerçekleşme tutarları" olarak tanımlıyor ve tutarların 2019 verilerine göre hesaplandığını yazıyor (PDF s. 23, 307).

**Dört tahminin ayrımı** (`outputs/tables/budget_law_vs_report_estimates_2019_2020.csv`, `scripts/03b_budget_law_annexes.py`)

| Mali yıl | Tahmin | Belge ve yer | Milyon TL | Aynı yılın bütçe kanunu tahminine göre |
|---|---|---|---|---|
| 2019 | 2018 raporu, tahmin (2017 verisine dayalı) | Tablo 3, PDF s. 298 | 178.696 | 0,00% |
| 2019 | 2018 raporu, bütçe kanununa eklenen tutarlar | Tablo 2, PDF s. 296 | 178.696 | 0,00% |
| 2019 | 2019 bütçe kanunu eki (7156) | RG s. 1973 (PDF s. 45) | 178.695,913 | — |
| 2019 | 2020 raporu, 2019 verisiyle hesaplanan "gerçekleşme" tahmini | Tablo 2, PDF s. 308 | 177.601 | −0,61% |
| 2020 | 2019 bütçe kanunu eki, ikinci yıl tahmini (= 2018 raporu) | RG s. 1973 (PDF s. 45) | 205.401,393 | +5,02% |
| 2020 | 2020 bütçe kanunu eki (7197) | RG s. 1973 (PDF s. 44) | 195.590,813 | — |
| 2020 | 2020 raporu, tahmin (2019 verisine dayalı) | Tablo 2, PDF s. 308 | 198.247 | +1,36% |
| 2020 | 2021 raporu, 2020 verisiyle hesaplanan "gerçekleşme" tahmini | Tablo 2, PDF s. 316 | 237.395 | +21,37% |

- **2019 bütçe eki ve 2018 raporu:** 36 satırın hepsi milyon TL'ye yuvarlamayla aynı; en büyük fark 0,477 milyon TL. Tek tahmin olarak sayıldı. Bu rakam bir tahmin, 2019 gerçekleşmesi değil.
- **2020 bütçe eki:** Değerler analiz edilen hiçbir raporda ve rapor metinlerinde geçmiyor (rapor metinlerinde rakam araması yapıldı). Kayıp 2019 raporuyla bağlantısını gösteren doğrudan kanıt yok. "Kayıp 2019 raporunun tek izi/vintajı" ifadeleri makaleden, sınırlılıklar dosyasından, bu dosyadan, kaynak envanterinden ve Tablo 3 notundan kaldırıldı.
- **"Gerçekleşme":** Revenue-forgone yöntemiyle, davranış değişikliği olmadığı varsayımıyla yapılan statik bir tahmindir. Politika etkisi ya da kaldırılma halinde elde edilecek gelir olarak sunulmuyor.

**Dönem ifadeleri**
- Makalede "2016–2025 reports", "every report from 2016 to 2025" ve "2016–2020 reports" geçen yerler "2016–2018 and 2020–2025" / "the nine reports analysed" biçiminde düzeltildi. Düzeltilen yerler: özet, §3, §5.1, §5.2, §5.4, §5.6, §6, §7, §8 ve Tablo A1 başlığı.
- Rapor serisinde 2018 gerçekleşme yılının eksik olduğu, 2019 gerçekleşme tahmininin ise 2020 raporunda bulunduğu açıkça yazıldı (§3, §8).
- §5.1'de iki rejimin düzeyleri tek bir eğilim olarak sunulmuyor.
- Kod kitabı başlığı, README ve Tablo 10 etiketi ("göründüğü her raporda") de güncellendi.

**Yeniden çalıştırma:** `run_all.sh` tam çalıştırıldı. `12_number_trace.py`: 75/75 PASS. Özet 200 sözcük; metin (kaynakçaya kadar) 7.007 sözcük.

### 10.7 Bibliography and submission files (23 Nov 2026)

- `paper/references.bib` curated and verified: 36 entries = 24 literature keys (2 unused entries removed; Bar-Siman-Tov book review replaced by the 2018 R&G article) + 9 reports + Laws 5018, 7156, 7197. All 36 cited; no missing keys (`scripts/13_check_citations.py`).
- Law 5018 Art. 15 and Art. 18(2)(c) verified in the consolidated text (`data/raw/law/`); added to Section 3.
- IMF note page locators checked against the PDF; one corrected (pp. 4, 12 → pp. 3, 10, 12).
- Style: APA 7 (no target journal specified). Submission files: `paper/submission/manuscript_anonymised.docx` (with references, tables, figures) and `title_page.docx` (`scripts/14_build_submission.py`). Number trace 75/75 PASS after edits.
- Details: `paper/reference_verification_report.md`.
