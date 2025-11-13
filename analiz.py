# --- GEREKLİ KÜTÜPHANELERİ İÇE AKTARMA ---
import pandas as pd
import logging
import sys
import io
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Tarih formatlaması için matplotlib'den 'dates' modülünü ekliyoruz
import matplotlib.dates as mdates


# --- 0. RAPORLAMA (LOGGING) SİSTEMİNİ AYARLAMA ---

# --- DEĞİŞİKLİK BURADA ---
# Çıktılarımızın kaydedileceği dosyanın adını 'son_rapor.txt' olarak güncelliyoruz.
log_dosyasi = "son_rapor.txt"
# --- DEĞİŞİKLİK BURADA ---

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    encoding='utf-8',
    handlers=[
        # 1. Handler: FileHandler (Dosyaya yazar, mode='w' üzerine yazar)
        logging.FileHandler(log_dosyasi, mode='w', encoding='utf-8'),
        # 2. Handler: StreamHandler (Ekrana/konsola yazar)
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info(f"--- RAPORLAMA BAŞLATILDI ---")
# Mesajı da yeni dosya adını yansıtacak şekilde güncelliyoruz.
logging.info(f"Tüm çıktılar '{log_dosyasi}' dosyasına kaydedilecek (mevcut dosyanın üzerine yazılarak).")


# --- TÜM ANALİZ İÇİN ANA 'TRY' BLOĞU BAŞLANGICI ---
# Kodun tamamı bu 'try' bloğunun içinde olmalı.
try:
    # --- AŞAMA 1: VERİ YÜKLEME VE HAZIRLIK ---
    logging.info("\nAşama 1: Veri Yükleme ve Hazırlık Başladı...")
    
    # (Senin bilgisayarındaki tam yolları kullanıyoruz)
    basket_file_path = "dosya yolu"
    customer_file_path = "dosya yolu"

    # 1. Verileri yükleme
    basket = pd.read_csv(basket_file_path)
    customers = pd.read_csv(customer_file_path)
    
    logging.info(f"'{basket_file_path}' başarıyla yüklendi.")
    logging.info(f"'{customer_file_path}' başarıyla yüklendi.")
    
    # --- 'basket' Veri Seti İncelemesi ---
    logging.info("\n--- 'basket_details.csv' Ön İzleme (İlk 5 Satır) ---")
    logging.info(basket.head().to_string())
    logging.info("\n--- 'basket_details.csv' Veri Yapısı (Info) ---")
    s = io.StringIO(); basket.info(buf=s); logging.info(s.getvalue())
    
    # --- 'customers' Veri Seti İncelemesi ---
    logging.info("\n--- 'customer_details.csv' Ön İzleme (İlk 5 Satır) ---")
    logging.info(customers.head().to_string())
    s_cust = io.StringIO(); customers.info(buf=s_cust); logging.info(s_cust.getvalue())
    logging.info("\n--- AŞAMA 1 TAMAMLANDI ---")

    
    # ===================================================================
    # --- AŞAMA 2: KEŞİFSEL VERİ ANALİZİ (EDA) ---
    # ===================================================================
    logging.info("\n\n--- AŞAMA 2: KEŞİFSEL VERİ ANALİZİ (EDA) BAŞLADI ---")
    
    # --- 2a: Sepet Verisi (basket) Analizi ---
    
    # 1. 'basket_date'i datetime'e çevirme
    logging.info("\n1. 'basket_date' sütunu 'datetime' formatına dönüştürülüyor...")
    basket['basket_date'] = pd.to_datetime(basket['basket_date'])
    logging.info("Dönüşüm tamamlandı.")
    s_basket_updated = io.StringIO(); basket.info(buf=s_basket_updated); logging.info(s_basket_updated.getvalue())
    
    # 2. Tarih Aralığı
    min_tarih = basket['basket_date'].min()
    max_tarih = basket['basket_date'].max()
    logging.info("\n--- 2. Veri Setinin Kapsadığı Tarih Aralığı ---")
    logging.info(f"En Eski Tarih: {min_tarih}")
    logging.info(f"En Yeni Tarih: {max_tarih}")
    
    # 3. Aylık satış sayısı
    logging.info("\n--- 3. Aylık Toplam Satış Sayısı ---")
    monthly_sales = basket.groupby(basket['basket_date'].dt.to_period("M"))['basket_count'].sum()
    logging.info(monthly_sales.to_string())

    # 4. En çok alınan 10 ürün (Aşama 3a ve 4'te kullanılacak)
    logging.info("\n--- 4. En Çok Satın Alınan 10 Ürün (product_id) ---")
    top_products = basket.groupby('product_id')['basket_count'].sum().sort_values(ascending=False).head(10)
    logging.info(top_products.to_string())

    # 5. En aktif 10 müşteri
    logging.info("\n--- 5. En Aktif 10 Müşteri (Toplam Ürün Alımına Göre) ---")
    top_customers = basket.groupby('customer_id')['basket_count'].sum().sort_values(ascending=False).head(10)
    logging.info(top_customers.to_string())
    
    # 6. GÜNLÜK SATIŞ SAYISI (Aşama 3b'de kullanılacak)
    logging.info("\n--- 6. Günlük Toplam Satış Sayısı (İlk 10 Gün) ---")
    daily_sales = basket.groupby('basket_date')['basket_count'].sum()
    logging.info(daily_sales.head(10).to_string())
    logging.info("\n--- AŞAMA 2 (Bölüm a: Sepet Analizi) TAMAMLANDI ---")

    
    # --- 2b: Birleştirme ve Müşteri Analizi ---
    logging.info("\n--- AŞAMA 2 (Bölüm b: Müşteri Analizi) BAŞLADI ---")

    # 7. Birleştirme
    logging.info("\n7. 'basket' ve 'customers' tabloları birleştiriliyor (how='left')...")
    merged = pd.merge(basket, customers, on="customer_id", how="left")
    logging.info("\n--- 8. Birleştirilmiş Veri Ön İzlemesi (İlk 5 Satır) ---")
    logging.info(merged.head().to_string())

    # 9. EŞLEŞME KONTROLÜ
    logging.info("\n--- 9. Birleştirilmiş Veri Yapısı (Info) - Eşleşme Kontrolü ---")
    s_merged = io.StringIO(); merged.info(buf=s_merged); logging.info(s_merged.getvalue())
    logging.info("\n--- ÖNEMLİ YORUM (Veri Kalitesi) ---")
    logging.info("Yukarıdaki 'info' çıktısı, 15000 'basket' işlemi için")
    logging.info("'sex', 'customer_age' gibi müşteri detaylarının çok az satırda bulunduğunu (72 non-null) göstermektedir.")
    logging.info("Aşağıdaki analizler, tüm veri setini DEĞİL, sadece bu az sayıdaki eşleşen müşteriyi temsil etmektedir.")
    
    # 10. Genel istatistikler (Aşama 4'te kullanılacak)
    total_sales = merged["basket_count"].sum()
    total_unique_customers_in_baskets = merged["customer_id"].nunique()
    avg_basket_size = merged["basket_count"].mean()
    logging.info("\n--- 10. GENEL İSTATİSTİKLER (Tüm Sepet Verisine Göre) ---")
    logging.info(f"Toplam satılan ürün sayısı: {total_sales}")
    logging.info(f"Toplam benzersiz müşteri sayısı (sepetlerde): {total_unique_customers_in_baskets}")
    logging.info(f"İşlem başına ortalama ürün sayısı (sepet büyüklüğü): {round(avg_basket_size, 2)}")

    # 11-15. Analizler (Sadece Eşleşen Müşteriler)
    logging.info("\n--- 11. CİNSİYETE GÖRE ORTALAMA SEPET BÜYÜKLÜĞÜ (Sadece Eşleşen Müşteriler) ---")
    gender_avg = merged.groupby("sex")["basket_count"].mean().sort_values(ascending=False); logging.info(gender_avg.to_string())
    logging.info("\n--- 12. YAŞ DAĞILIMI (İstatistiksel Özet - Sadece Eşleşen Müşteriler) ---")
    logging.info(merged["customer_age"].describe().to_string())
    logging.info("\n--- 13. EN ÇOK ALIŞVERİŞ YAPAN YAŞLAR (İLK 10 - Sadece Eşleşen Müşteriler) ---")
    age_sales = merged.groupby("customer_age")["basket_count"].sum().sort_values(ascending=False).head(10); logging.info(age_sales.to_string())
    logging.info("\n--- 14. YAŞ GRUBUNA GÖRE ORTALAMA SEPET BÜYÜKLÜĞÜ (Sadece Eşleşen Müşteriler) ---")
    merged["age_group"] = pd.cut(merged["customer_age"], bins=[0, 20, 30, 40, 50, 60, 150], labels=["<20", "20-30", "30-40", "40-50", "50-60", "60+"])
    age_group_avg = merged.groupby("age_group", observed=True)["basket_count"].mean().sort_values(ascending=False); logging.info(age_group_avg.to_string())
    logging.info("\n--- 15. EN SADIK 10 MÜŞTERİ (Toplam Alışveriş * Tenure - Sadece Eşleşen Müşteriler) ---")
    loyal_customers_sum = merged.groupby('customer_id').agg(total_basket_count=('basket_count', 'sum'), mean_tenure=('tenure', 'mean')).dropna()
    loyal_customers_sum['loyalty_score'] = loyal_customers_sum['total_basket_count'] * loyal_customers_sum['mean_tenure']
    logging.info(loyal_customers_sum.sort_values('loyalty_score', ascending=False).head(10).to_string())
    logging.info("\n\n--- AŞAMA 2 (TÜMÜ) TAMAMLANDI ---")

    
    # ===================================================================
    # --- AŞAMA 3: VERİ GÖRSELLEŞTİRME ---
    # ===================================================================
    logging.info("\n\n--- AŞAMA 3: VERİ GÖRSELLEŞTİRME BAŞLADI ---")
    
    # --- 3a: En Çok Satılan 10 Ürün Grafiği ---
    top_products_df = top_products.reset_index()
    top_products_df['product_id'] = top_products_df['product_id'].astype(str)
    logging.info("\n3a. 'En Çok Satılan 10 Ürün' grafiği oluşturuluyor...")
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")
    ax = sns.barplot(x='basket_count', y='product_id', data=top_products_df, orient='h', palette='viridis', order=top_products_df.sort_values('basket_count', ascending=False).product_id)
    plt.title('En Çok Satılan 10 Ürün (product_id)', fontsize=16, fontweight='bold')
    plt.xlabel('Toplam Satış Adedi', fontsize=12)
    plt.ylabel('Ürün ID', fontsize=12)
    for p in ax.patches:
        width = p.get_width()
        plt.text(width + 0.5, p.get_y() + p.get_height() / 2., f'{int(width)}', ha='left', va='center')
    plt.xlim(0, top_products.max() * 1.15) 
    plt.tight_layout()
    grafik_dosya_adi = "top_10_products.png"
    plt.savefig(grafik_dosya_adi)
    logging.info(f"Grafik başarıyla '{grafik_dosya_adi}' olarak kaydedildi.")
    plt.close() # Grafiği kapat
    logging.info("\n--- AŞAMA 3 (Bölüm a: Ürün Grafiği) TAMAMLANDI ---")

    
    # --- 3b: Günlük Satış Trendi ---
    logging.info("\n3b. 'Günlük Satış Trendi' grafiği oluşturuluyor...")
    plt.figure(figsize=(16, 7))
    sns.set_style("darkgrid")
    ax_trend = sns.lineplot(x=daily_sales.index, y=daily_sales.values, marker='o', color='mediumblue')
    plt.title('Günlük Toplam Satış Trendi (Mayıs-Haziran 2019)', fontsize=16, fontweight='bold')
    plt.xlabel('Tarih', fontsize=12)
    plt.ylabel('Toplam Satış Adedi', fontsize=12)
    date_format = mdates.DateFormatter('%b %d')
    ax_trend.xaxis.set_major_formatter(date_format)
    plt.xticks(rotation=45)
    plt.tight_layout()
    grafik_trend_adi = "daily_sales_trend.png"
    plt.savefig(grafik_trend_adi)
    logging.info(f"Grafik başarıyla '{grafik_trend_adi}' olarak kaydedildi.")
    plt.close() # Grafiği kapat
    logging.info("\n--- AŞAMA 3 (Bölüm b: Trend Grafiği) TAMAMLANDI ---")


    # ===================================================================
    # --- AŞAMA 4: RAPORLAMA VE YÖNETİCİ ÖZETİ ---
    # ===================================================================
    
    # Bu bölüm, tüm analizler bittikten sonra, rapor dosyasına bir özet ekler.
    
    logging.info("\n\n" + "="*60)
    logging.info("--- AŞAMA 4: RAPORLAMA VE YÖNETİCİ ÖZETİ ---")
    logging.info("="*60 + "\n")
    
    logging.info("PROJE: E-Ticaret Satış Veri Analizi")
    # 'min_tarih' ve 'max_tarih' Aşama 2a'da hesaplanmıştı. .date() ile sadece tarih kısmını alıyoruz.
    logging.info(f"ANALİZ TARİH ARALIĞI: {min_tarih.date()} - {max_tarih.date()}\n")
    
    logging.info("--- 1. TEMEL PERFORMANS GÖSTERGELERİ ---")
    # Bu değişkenler Aşama 2b'de (madde 10) hesaplanmıştı.
    logging.info(f"* Toplam Satılan Ürün Sayısı: {total_sales}")
    logging.info(f"* Analiz Edilen Toplam İşlem Sayısı: {len(basket)}")
    logging.info(f"* İşlem Başına Ortalama Ürün Sayısı: {round(avg_basket_size, 2)}")
    logging.info(f"* Toplam Benzersiz Müşteri (Sepetlerde): {total_unique_customers_in_baskets}")
    
    logging.info("\n--- 2. YÖNETİCİ İÇGÖRÜLERİ VE CEVAPLAR ---")
    
    logging.info("\n[SORU 1]: 'Hangi ürünlere odaklanmalı?'")
    # 'top_products' Aşama 2a'da (madde 4) hesaplanmıştı. .index[0] en üsttekini verir.
    logging.info(f"[CEVAP]: Stok ve pazarlama bütçesi öncelikle 'product_id'si '{top_products.index[0]}' (69 satış) olan ürüne odaklanmalıdır.")
    logging.info(f"         İkinci en popüler ürün '{top_products.index[1]}' (59 satış) olmuştur.")
    logging.info(f"         (Detaylar için 'top_10_products.png' grafiğine bakınız.)")

    logging.info("\n[SORU 2]: 'Hangi şehirlerde pazarlama artırılmalı?'")
    logging.info(f"[CEVAP]: Bu soru, mevcut veri setleri ile CEVAPLANAMAMAKTADIR.")
    logging.info(f"         'customer_details.csv' dosyasında müşterilere ait şehir, bölge veya adres bilgisi bulunmamaktadır.")

    logging.info("\n--- 3. SATIŞ TRENDİ ---")
    logging.info(f"* Satışlar 1 aylık dönemde (Mayıs sonu - Haziran başı) yoğunlaşmıştır.")
    logging.info(f"* Günlük satışlarda belirgin dalgalanmalar mevcuttur. Özellikle 26-28 Mayıs 2019 arası güçlü bir satış zirvesi yaşanmıştır.")
    logging.info(f"  (Detaylar için 'daily_sales_trend.png' grafiğine bakınız.)")
    
    logging.info("\n--- 4. ÖNEMLİ VERİ KALİTESİ NOTLARI ---")
    logging.info(f"[Kritik Sorun]: Müşteri Veri Eşleşmesi")
    logging.info(f"  Analiz edilen 15,000 sepet işleminin SADECE 72 tanesi (%0.48'i) 'customer_details.csv' tablosundaki bir müşteriyle eşleşebilmiştir.")
    logging.info(f"  Bu nedenle, yaş, cinsiyet ve sadakat (tenure) üzerine yapılan analizler (Raporun Aşama 2b bölümündekiler) veri setinin tamamını temsil etmemektedir ve bu analizlere dayanarak stratejik karar alınması YANILTICI olabilir.")
    
    logging.info(f"\n[Aykırı Veri]: Yaş Verisi")
    logging.info(f"  Eşleşen 72 müşterinin yaş verisi incelendiğinde, 'min: 5.0' ve 'max: 2022.0' gibi aykırı değerler tespit edilmiştir.")
    logging.info(f"  Ayrıca '123.0' gibi değerlerin 'Bilinmiyor' için bir kodlama olduğu düşünülmektedir. Bu, müşteri verisinin temizlenmesi gerektiğini göstermektedir.")
    
    logging.info("\n\n" + "="*60)
    logging.info("--- PROJE ANALİZİ TAMAMLANDI ---")
    logging.info("="*60)


# --- HATA YAKALAMA (EXCEPT) BLOKLARI ---
# 'try' bloğunun *tamamı* bittikten sonra, en sonda yer alırlar.
except FileNotFoundError as e:
    logging.error(f"\nHATA: Dosya bulunamadı.")
    logging.error(f"Detay: {e}")
except ImportError as e:
    logging.error(f"\nHATA: Gerekli bir kütüphane eksik.")
    logging.error(f"Detay: {e}")
except Exception as e:
    logging.error(f"\nBeklenmedik bir hata oluştu: {e}")
