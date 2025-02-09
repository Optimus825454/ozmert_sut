# **---::::---LIMK---::::---**

# Süt ve Yem Yönetim Sistemi Projesi

## 1. Proje Hedefleri

- Süt toplama, yem dağıtımı, muhasebe ve raporlama süreçlerini dijitalleştirerek daha verimli hale getirmek.
- Minimum veri girişi ile maksimum analiz ve raporlama sağlayarak insan hatalarını azaltmak.
- Yapay zeka entegrasyonu ile kullanıcıları yönlendiren, uyarılar yapan ve soruları cevaplayan akıllı bir sistem oluşturmak.

------

## 2. Proje Modülleri

### 2.1. Araç/Rota Yönetimi

- [ ] **Araç ve şoför tanımları:** Araçlar ve şoförler bir arada kaydedilir (ör. Araç A - Şoför Mehmet).
- [ ] **Müstahsil listesi:** Hangi müstahsillerin hangi rotaya bağlı olduğu görüntülenir.

### 2.2. Süt Toplama ve Yem Dağıtımı

- [ ] Süt Kartı:
  - Şoförün, her müstahsilden topladığı süt miktarı ve dağıttığı yem miktarını elle yazdığı fiziksel kart.
  - Kartta tarih, miktar, müstahsil adı-soyadı gibi bilgiler bulunur.
- [ ] Sistem Girişi:
  - Şoförler, süt kartlarını her ayın 1’i ve 15’inde merkeze teslim eder.
  - Merkez, bu karttaki verileri sisteme işler.

### 2.3. Yem Satışı ve Tedariki

- Yem Tedariki:
  - [ ] Şoför, yem siparişi olduğunda yem tedarikçisinden yemleri teslim alır.
  - [ ] Tedarik sırasında alınan belge WhatsApp üzerinden merkeze gönderilir.
  - [ ] Merkez, alınan yem miktarını ve tarihini sisteme kaydeder.
- Yem Satışı ve Dağıtımı:
  - Dağıtılan yem miktarı süt kartına eklenir ve hangi müstahsile ne kadar yem verildiği not edilir.
  - Sistem, toplam alınan yem miktarı ile dağıtılan yem miktarını kontrol eder. Fazla giriş yapılmasına izin verilmez.
- Çapraz Kontrol:
  - Tedarik edilen yem miktarı ile dağıtılan yem miktarı karşılaştırılır.

### 2.4. Süt Teslimatı

- [ ] **Fabrikaya teslimat:** Şoför, topladığı sütleri fabrikaya teslim eder ve belge alır.
- [ ] **Belge paylaşımı:** Fabrika belgeleri WhatsApp üzerinden merkeze iletilir.
- [ ] **Sistem girişi:** Merkez, süt teslimatlarını sisteme kaydeder.
- [ ] Çapraz kontrol:
  - Müstahsillerden alınan süt miktarı ile fabrikaya teslim edilen süt miktarı karşılaştırılır.
  - Fazla veya eksik girişlere izin verilmez.

### 2.5. Muhasebe Modülü

- [ ] Gelir/Gider Takibi:
  - Toplanan sütlerin satışından elde edilen gelir kaydedilir.
  - Yem alımı ve dağıtımı gider olarak kaydedilir.
- [ ] Hesap Kesimi:
  - Sistem, belirlenen periyotlarda müstahsillerin borç/alacak durumlarını hesaplar.
- [ ] Hesap Pusulası:
  - Müstahsillere özel raporlar (A5 boyutunda) hazırlanır ve yazdırılır.
- [ ] Kar/Zarar Analizi:
  - Günlük, haftalık, aylık ve yıllık raporlar oluşturulur.

### ve Analiz

- [ ] Standart Raporlar:
  - Müstahsil performansı, araç yakıt tüketimi, şoför verimliliği gibi raporlar.
- [ ] Özel Raporlar:
  - Belirli tarih aralıklarında veya kategorilere göre oluşturulan özelleştirilmiş raporlar.

------

## 3. Teknik Yapı

### 3.1. Veri Tabanı

- [ ] MySQL:
  - Araç, şoför, rota, müstahsil, süt toplama, yem dağıtımı, muhasebe ve raporlama verilerini saklamak için kullanılacak.
  - İlişkisel yapı ile verilerin tutarlı ve düzenli şekilde saklanması sağlanacak.

### 3.3. Kullanıcı Arayüzü (UI/UX)

- [ ] **Web Tabanlı Panel:**
  - Adminler için rota ve müstahsil yönetimi, veri girişi ve raporlama ekranları.
- [ ] **Mobil Uyum:**
  - Mobil cihazlarda kolay kullanım için responsive tasarım.

###

------

- [ ] ## 4. Proje Adımları

- [ ] ### 4.1. Analiz ve Planlama

- [ ] - İş akışlarının ve veri yapısının detaylı analizi.
  - Gerekli özelliklerin önceliklendirilmesi.

- [ ] ### 4.2. Veri Tabanı Tasarımı

- [ ] - MySQL üzerinde tabloların ve ilişkilerin oluşturulması.

- [ ] ### 4.3. Backend Geliştirme

- [ ] - Veri tabanı işlemleri ve iş kuralları için API geliştirilmesi (Python - Flask).

- [ ] ### 4.4. Frontend Geliştirme

- [ ] - Kullanıcı arayüzlerinin geliştirilmesi (React).

  ###

- [ ] ------

- [ ] ## 5. OLUŞTURMA AŞAMALARI

- [ ] - **1:** Analiz, veri tabanı tasarımı ve planlama.
  - **2:** Backend geliştirme.
  - **3:** Frontend geliştirme.
  
- [ ] ------

- [ ] ##
