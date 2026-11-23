# 01 — Kaynak Doğrulama Raporu

**Bildiri:** Yerel Yönetimlerde Yeşil Finansman ve Sürdürülebilirlik (XII. International Academic Studies Congress, Stuttgart, 24–26 Kasım 2026)
**Doğrulanan dosya:** `kaynak/Yerel_Yonetimlerde_Yesil_Finansman 23.11.2026 son.docx`. Bu dosya özgün hâliyle korunmuştur; MD5 değeri yüklenen dosyayla aynıdır.
**Tarih:** 23 Kasım 2026

## 1. Yöntem ve erişim sınırları

| Adım | Araç | Ne doğrulandı |
|---|---|---|
| Künye ve DOI | Crossref REST API (`scripts/fetch_meta.py`) | DOI çözümlemesi, yazarlar, yıl, dergi, cilt, sayı, sayfa |
| Özet | OpenAlex → Semantic Scholar → Crossref | Metinde kaynağa atfedilen bulgunun özette yer alıp almadığı |
| Özetin bulunamadığı durumlar | Web araması (RePEc/IDEAS, HAL, kurumsal depolar, OECD sayfa özetleri) | Özetin ikincil kopyası |
| Atıf–kaynakça eşleşmesi | `scripts/atif_kontrol.py` | Her atfın kaynakçada, her kaynağın metinde bulunması |

Bu doğrulamanın sınırları şunlardır:

- **Web of Science veya Scopus'a erişim yoktur.** Bu nedenle hiçbir kaynak için indeks durumu veya atıf sayısı iddia edilmemiştir.
- **Hiçbir kaynağın tam metni okunmamıştır.** Bulgular yalnızca özet düzeyinde kontrol edilmiştir.
- nature.com, oecd.org, mdpi.com ve sagepub.com sayfalarına doğrudan erişim engellidir. Bu engeller aşılmaya çalışılmamış; bu kaynaklarda ikincil kopyalar kullanılmıştır.
- Ham API yanıtları `dogrulama/cache/` klasöründe, derlenmiş künyeler `dogrulama/meta_mevcut.json` ve `dogrulama/meta_yeni.json` dosyalarında saklanmıştır.

## 2. Özgün kaynakçanın doğrulanması (36 kaynak)

**Sonuç:** 32 DOI'nin tamamı Crossref'te geçerlidir ve doğru yayına çözümlenmektedir. Bunlara OECD raporlarının DOI'leri de dahildir. **Uydurma veya hayalî görünen kaynak bulunmamıştır.** Bu nedenle özgün kaynakçadan hiçbir kaynak çıkarılmamıştır. DOI'si olmayan dört klasik kitap (Pigou, 1920; Oates, 1972; Mazzucato, 2013; WCED, 1987) için künyeler standart bilgiyle tutarlıdır.

### 2.1. Düzeltilen künye hataları

| Kaynak | Özgün metindeki hâli | Crossref'e göre doğrusu |
|---|---|---|
| Ahmad ve Du | (2025), cilt/sayfa yok | **(2026)**, *Sustainable Development, 34*(1), 510–532. Çevrim içi yayın 29 Eylül 2025 |
| K. de Mello vd. (2023) | 21, 318–325 | **21(4)**, 318–325 |
| L. de Mello ve Ter-Minassian (2024) | cilt/sayfa yok | **23(3), 113–131** |
| Diezmartínez ve Short Gianotti (2024) | 14, 247–252 | **14(3)**, 247–252 |
| Karpf ve Mandel (2018) | 8, 161–165 | **8(2)**, 161–165 |
| Rashidi vd. (2019) | 48, sayfa yok | **48, 131–138** |
| Sun ve Feng (2023) | cilt yok | **430**, Article 139688 |
| García-Lamarca vd. (2022) | 13, 7132 | **13(1)**, Article 7132 |
| OECD (2022) | seri yok | *(OECD Multi-level Governance Studies)* eklendi |
| Bigger ve Millington (2020) | — | Çevrim içi 2019, baskı 2020. APA 7'ye göre 2020 doğru, değiştirilmedi |
| Connolly ve Kythreotis (2026) | — | Çevrim içi 2025, baskı 2026. 2026 doğru, değiştirilmedi |

Bunlara ek olarak tüm kaynakça APA 7 biçimine getirilmiştir. Dergi adı ve cilt italik yazılmış, kitap adları cümle düzeninde yazılmış, makale numaraları "Article" ile belirtilmiştir.

### 2.2. Kaynağa atfedilen bulguların kontrolü

| Kaynak | Özgün metindeki ifade | Özet kontrolü | İşlem |
|---|---|---|---|
| Baker vd. (2022) | "daha yoğunlaşmış, **uzun vadeli** bir yatırımcı tabanında tutulduğu" | Özette "more closely held" ifadesi var; "uzun vadeli" yok. Eşzamanlı ihraçlarda primin ikincil piyasada ortaya çıktığı da belirtiliyor | "Uzun vadeli" çıkarıldı; eşzamanlı ihraç ayrımı eklendi |
| Droste vd. (2017) | Telafi **ve teşvik etkisi "ortaya koymuştur"** | Panel verisi ilişkiyi gösteriyor; nedensellik iddiası güçlü | İlişkisel dile çevrildi; nedensellik uyarısı eklendi |
| Toxopeus ve Polzin (2021) | "gelir akışlarının belirsizliği" | Özetteki ana engeller: kamu-özel koordinasyon ve değerleme/muhasebe entegrasyonu | Özete uygun biçimde yeniden yazıldı |
| Shi ve Varuzzo (2020) | Kıyı belediyelerinin "ciddi gelir kaybı riskiyle" karşı karşıya kaldığı | Özete göre yalnızca birkaç belediye anlamlı kayıp riski taşıyor, diğerlerinde etki önemsiz | Düzeltildi |
| Rashidi vd. (2019) | Yalnız net kazançlı politikalar | Özete göre net maliyetli politikalar da kredi notuna katkı sağlayabiliyor | Eklendi |
| Sun ve Feng (2023) | Etki "sanayi yapısı, enerji verimliliği ve yeşil teknoloji yenilikleri **kanalıyla**" | Özette bu kanallar doğrulanamadı. Doğrulanan bilgi: 2011'den beri gösteri kentleri, zamanla değişen FF yöntemi, enerji tasarrufu ve emisyon azaltımı etkisi, coğrafi konum ve kaynak bağımlılığının zayıflatıcı etkisi | Kanal iddiası çıkarıldı |
| Larcker ve Watts (2020) | "ihraç fiyatlamasında anlamlı fark yok" | ABD belediye piyasası, aynı ihraççı, aynı gün; prim esasen sıfır | Bağlam (ABD belediye, aynı ihraççı/gün) eklendi |
| Gorelick ve Walmsley (2020) | "kent içindeki öncü yöneticiler" | Özette bu kişi kentin mali işler sorumlusu (treasurer/CFO) olarak tanımlanıyor | 5.4'te açıkça belirtildi |
| OECD (2022) | "hem yönetsel hem seçilmiş yetkililerin **üst düzey desteğinin** gerekli olduğu" | Erişilebilen sayfa özetinde doğrulanamadı | Cümle çıkarıldı |
| OECD (2022) | Brittany ve Venedik vakaları | Tam rapora erişilemedi | Vaka ayrıntıları çıkarıldı; yalnız uygulama biçimlerinin çeşitliliği korundu |
| Zerbib (2019); Fatica vd. (2021) | Belediye tartışmasının içinde, ayrım belirtilmeden | Örneklemler şirket, finansal kuruluş ve uluslarüstü ihraççılardan oluşuyor | Ayrı paragrafa alındı; "belediyelere doğrudan aktarılamaz" uyarısı eklendi |
| Flammer (2021) | Şirket örneklemi olarak belirtilmişti | Doğru | Korundu; belediye kanıtı (Campi vd., 2024) eklendi |
| Bachelet vd. (2019) | "daha elverişsiz fiyatlama ve daha düşük likidite" | Özet: doğrulanmamış özel ihraççı tahvilleri likidite ve oynaklık bakımından elverişsiz, pozitif prim (yüksek getiri) taşıyor | Özete göre netleştirildi; belediye örneklemi olmadığı belirtildi |
| Moser-Plautz ve Korac (2025) | Avusturya deneyimi | Odak federal düzey; alt ulusal kaynak eksikliği ve kademeler arası eşgüdüm bilgisi özette var | Federal odak belirtildi |

### 2.3. Özet düzeyinde doğrulanan bulgular

Aşağıdaki sayısal ve nitel bulgular kaynak özetleriyle uyumludur ve korunmuştur:

- **Busch vd. (2021):** 0,35 milyar $ (2007) → 23 milyar $ (2020); beş ülke.
- **K. de Mello vd. (2023):** %5'e varan kayıp; gelirini ikiye katlayan belediyeler.
- **Partridge ve Medda (2020):** ikincil piyasada yaklaşık 5 bp; birincil piyasada kesin prim yok.
- **Goldsmith-Pinkham vd. (2023):** fiyatlama 2013'ten itibaren; uzun vadelerde daha güçlü.
- **Painter (2020).**
- **Karpf ve Mandel (2018).**
- **Moser vd. (2019):** 15 arketip; anket ve 9 çalıştay.
- **Ahmad ve Du (2026):** 121 çalışma; %19 / %15 / %11.
- **Diezmartínez ve Short Gianotti (2024, 2025):** 34 görüşme; 15 kent.
- **OECD (2024):** 36 ülkeden 24 (2020'de 14).
- **OECD (2023):** Türkiye.

OECD verileri yalnızca OECD yayın sayfası özetlerinden doğrulanabilmiştir.

**Özete yayıncı sayfası dışından (ikincil kopyadan) erişilen kaynaklar:**

| Kaynak | İkincil kopya |
|---|---|
| Busch vd. (2021) | ANU, Conservation International |
| Larcker ve Watts (2020) | IDEAS/RePEc |
| Painter (2020) | IDEAS/RePEc |
| Karpf ve Mandel (2018) | HAL |
| Sun ve Feng (2023) | Knowledge Agora |
| Diezmartínez ve Short Gianotti (2024) | Arama motoru özeti |
| Flammer (2021) | — |

## 3. Yeni eklenen kaynakların doğrulanması

Kırk bir aday DOI için Crossref künyesi ve özet çekilmiştir (`dogrulama/yeni.txt`). Bunlardan **32 kaynak** metne eklenmiştir. Tamamının künyesi Crossref'te doğrulanmıştır. Özet erişimi şöyledir:

**Yayıncı veya OpenAlex özeti (26 kaynak):**

- Belediye tahvilleri ve iklim riski: Bunch ve Strauss (2025); Campi vd. (2024); Smull vd. (2023); Jeon vd. (2026); Berry-Stölzle ve Hao (2026); Ko ve Prakash (2022); Shtob (2024); Tran ve Uzmanoglu (2024).
- Yeşil ve iklim bütçelemesi: Brown ve Hoti (2025); Baggio ve Tozer (2025); Davey (2026); Ermasova vd. (2026); Pindiriri ve Kwaramba (2024).
- Mali federalizm ve koordinasyon: Wu vd. (2025, Semantic Scholar üzerinden); Funder ve Dupuy (2022); Deslatte vd. (2023).
- Doğa temelli çözümler: Biasin vd. (2024); Thompson vd. (2023); Papari vd. (2024).
- Sosyal adalet: Anguelovski vd. (2022); Sax vd. (2022).
- Uyum finansmanı ve kalkınma bankaları: Whittaker ve Jespersen (2022); Rogers vd. (2025); Suchodolski vd. (2022); White ve Wahba (2019); Kupper vd. (2026).
- Atık ücretlendirmesi: Romano ve Masserini (2023); Compagnoni ve Torbert (2026).

**İkincil depo özeti (2 kaynak):**

| Kaynak | Özetin alındığı yer | Not |
|---|---|---|
| Ayaydın Hacıömeroğlu vd. (2026) | ODTÜ OpenMETU deposu | Başlıktaki "illiquidity" vurgusunun içeriği doğrulanamadığı için metinde bu yönde bir iddia kurulmadı |
| Yazar vd. (2020) | IDEAS/RePEc | — |

**Yalnız arama motoru özeti (2 kaynak):**

- **Gilmore vd. (2022):** Bu bir Comment yazısıdır. Metinde yalnız genel argümanı kullanıldı; arama özetinde görülen yüzde değeri kullanılmadı.
- **Op de Beeck vd. (2024):** Özet, arama sonucunda yazar, dergi ve yılla eşleşiyor.

### 3.1. Elenen adaylar

Aşağıdaki adayların künyesi doğrulandı, ancak gerekçeleri belirtilen nedenlerle metne alınmadılar. Ayrıntılı liste `02_Literatur_Matrisi.xlsx` dosyasının "Elenen adaylar" sayfasındadır.

| Aday | Gerekçe |
|---|---|
| Sojoudi vd. (2026), *Green spread of US municipal bonds* | Özete erişilemedi |
| Mishra vd. (2026), *Nature Cities* | Özete erişilemedi |
| Jin ve Li (2026), *Ecological Economics* | Özete erişilemedi |
| Xiao vd. (2025), *Ecological Economics* | Özete erişilemedi |
| Di Matteo ve Guadagno (2024) | Özete erişilemedi |
| Diğerleri | Mükerrer kaynak veya metne ek katkı sağlamaması |

## 4. Kullanılan web kaynakları (ikincil özet doğrulaması)

- ANU Research Portal — Busch vd. (2021): https://researchportalplus.anu.edu.au/en/publications/a-global-review-of-ecological-fiscal-transfers/
- Conservation International — Busch vd. (2021): https://www.conservation.org/research/a-global-review-of-ecological-fiscal-transfers
- IDEAS/RePEc — Larcker ve Watts: https://ideas.repec.org/p/ecl/stabus/3766.html
- IDEAS/RePEc — Painter (2020): https://ideas.repec.org/a/eee/jfinec/v135y2020i2p468-482.html
- HAL — Karpf ve Mandel: https://halshs.archives-ouvertes.fr/halshs-01905988v1
- OECD (2024): https://www.oecd.org/en/publications/green-budgeting-in-oecd-countries-2024_9aea61f0-en.html
- OECD (2023): https://www.oecd.org/en/publications/government-at-a-glance-2023_3d5c5d31-en/full-report/component-31
- OECD (2022): https://www.oecd.org/en/publications/aligning-regional-and-local-budgets-with-green-objectives_93b4036f-en.html
- Knowledge Agora — Sun ve Feng (2023): https://xreiss.efri.uniri.hr/article.php?id=32937
- OpenMETU — Ayaydın Hacıömeroğlu vd. (2026): https://open.metu.edu.tr/handle/11511/117858
- IDEAS/RePEc — Yazar vd. (2020): https://ideas.repec.org/a/spr/climat/v160y2020i4d10.1007_s10584-019-02509-3.html
- IDEAS/RePEc — Gilmore vd. (2022): https://ideas.repec.org/a/nat/natcli/v12y2022i3d10.1038_s41558-022-01311-x.html
- Antwerp Üniversitesi InnoFiNS — Op de Beeck vd. (2024): https://uantwerpen.be/en/research-groups/govtrust/projects/innofins
