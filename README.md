# 📊 Proje: E-Ticaret Satış Veri Analizi

Bu proje, bir e-ticaret sitesine ait satış veri setini analiz ederek şirketin satış performansını, popüler ürünlerini ve müşteri davranışlarını anlamayı amaçlamaktadır.

## 🎯 Amaç

Analiz sonucunda yönetime aşağıdaki konularda içgörüler sunulmuştur:
* Hangi ürünlere odaklanılmalı?
* Genel satış trendleri nasıldır?
* Mevcut veri setindeki **kritik kalite sorunları** nelerdir ve hangi analizler **yapılamaz**?

## 🛠️ Kullanılan Teknolojiler

* **Python 3**
* **Pandas:** Veri manipülasyonu ve analizi
* **Numpy:** Sayısal hesaplamalar
* **Matplotlib & Seaborn:** Veri görselleştirme

## 📈 Analizden Çıkan Sonuçlar

### 1. En Popüler Ürünler

*Analiz, en çok satan 10 ürünü belirlemiştir. **`43524799`** ID'li ürün, 69 adet satış ile listenin başındadır. Stok ve pazarlama bütçesi bu ürünlere odaklanabilir.*

![En Çok Satılan 10 Ürün](top_10_products.png)

### 2. Günlük Satış Trendi

*Satışlar özellikle **27 Mayıs 2019** tarihinde (3478 adet) bir zirve yaparak Mayıs sonu ve Haziran başında yoğunlaşmıştır. Günlük bazda dalgalanmalar mevcuttur.*

![Günlük Satış Trendi](daily_sales_trend.png)

### 3. ❗ Kritik Veri Kalitesi Bulgusu

Analizin en önemli çıktısı, mevcut veri setlerindeki ciddi kalite sorunudur:

* **%0.48 Eşleşme:** Sepet verisindeki (`basket_details.csv`) 15.000 işlemin **sadece 72 tanesi (%0.48)**, müşteri detayları (`customer_details.csv`) tablosu ile eşleşmiştir.
* **Sonuç:** Bu durum, yaş, cinsiyet veya sadakat (tenure) gibi demografik analizlerin, toplam satışın %99'undan fazlasını temsil etmeyeceği için **yanıltıcı olacağını** göstermiştir. Bu nedenle bu analizler rapora dahil edilmemiştir.
* **Aykırı Veri:** Eşleşen az sayıdaki veride bile 'customer\_age' (yaş) sütununda `5.0` ve `2022.0` gibi aykırı değerler tespit edilmiştir.

### 4. Cevaplanamayan Sorular

* **Bölgesel Analiz:** `customer_details.csv` dosyasında müşterilere ait 'şehir' veya 'bölge' bilgisi bulunmadığı için "Hangi şehirlerde pazarlama artırılmalı?" sorusu bu veri seti ile **cevaplanamamıştır**.

## 📝 Nihai Analiz Raporu

Tüm bulguların ve yönetici özetinin yer aldığı detaylı metin raporuna **`son_rapor.txt`** dosyasından ulaşabilirsiniz.

## 🚀 Projeyi Çalıştırma

1.  Bu depoyu klonlayın veya indirin.
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install pandas numpy matplotlib seaborn
    ```
3.  Veri setini [bu Kaggle linkinden](https://www.kaggle.com/datasets/berkayalan/ecommerce-sales-dataset/data) indirin.
4.  `basket_details.csv` ve `customer_details.csv` dosyalarını `analiz.py` kodunun bulunduğu ana klasöre kopyalayın.
5.  `analiz.py` dosyasını çalıştırın (dosya yollarının kod içinden temizlendiği varsayılarak):
    ```bash
    python analiz.py
    ```
Kod çalıştığında, `son_rapor.txt` metin dosyasını ve `top_10_products.png` ile `daily_sales_trend.png` görsellerini oluşturacaktır.
