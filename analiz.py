# --- GEREKLİ KÜTÜPHANELERİ İÇE AKTARMA ---
import pandas as pd
import logging
import sys
import io
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# --- 0. RAPORLAMA (LOGGING) SİSTEMİNİ AYARLAMA ---

# Rapor dosyasının adı senin istediğin gibi "son_rapor.txt" olarak kaldı.
log_dosyasi = "son_rapor.txt"

# Eski logger'ları temizle (önceki çalışmalardan kalıntı olmasın)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Yeni, "insan okuyacak" seviyede logger'ı ayarla
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",  # Sadece mesajı bas
    encoding='utf-8',
    handlers=[
        logging.FileHandler(log_dosyasi, mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout) # Ekrana da bas
    ]
)

logging.info("="*60)
logging.info("--- E-TİCARET VERİ ANALİZİ YÖNETİCİ RAPORU ---")
logging.info("="*60)
logging.info(f"Rapor Dosyası: {log_dosyasi}\n")

try:
    # --- AŞAMA 1: VERİ YÜKLEME VE HAZIRLIK ---
    logging.info("--- AŞAMA 1: VERİ YÜKLEME VE TEMEL KONTROLLER ---")

    # Dosya yolları senin belirttiğin gibi orijinal (hardcoded) haliyle bırakıldı.
    basket_path = "C:\\Users\\Ayşegül Uçan\\Documents\\YZT\\yzt25takim\\basket_details.csv"
    customer_path = "C:\\Users\\Ayşegül Uçan\\Documents\\YZT\\yzt25takim\\customer_details.csv"
    
    try:
        df_basket = pd.read_csv(basket_path)
        df_customer = pd.read_csv(customer_path)
    except FileNotFoundError as e:
        logging.error(f"[HATA] Gerekli CSV dosyaları belirtilen yolda bulunamadı: {e}")
        logging.error("Analiz durduruldu. Lütfen dosya yollarının doğruluğunu kontrol et.")
        sys.exit() # Hata varsa devam etme

    # Rapora teknik olmayan özet bilgi eklendi
    logging.info(f"Başarılı: 'basket_details.csv' yüklendi ({len(df_basket)} satır).")
    logging.info(f"Başarılı: 'customer_details.csv' yüklendi ({len(df_customer)} satır).")

    # Tarih formatını düzeltme (Görselleştirme için kritik)
    df_basket['basket_date'] = pd.to_datetime(df_basket['basket_date'])
    logging.info("Veri Hazırlığı: 'basket_date' sütunu tarih formatına çevrildi.")
    
    # --- df.info() ve df.head() çıktıları rapordan kaldırıldı ---


    # --- AŞAMA 2: KEŞİFSEL VERİ ANALİZİ (EDA) - PROJE HEDEFLERİ ---
    logging.info("\n--- AŞAMA 2: TEMEL ANALİZ (PROJE HEDEFLERİ) ---")

    # --- Soru 1: Hangi ürünlere odaklanmalı? (Popüler Ürünler) ---
    logging.info("\n[Soru 1]: Hangi ürünlere odaklanmalı?")
    # Ürün ID'sine göre toplam satış (basket_count) miktarını hesapla
    top_10_products = df_basket.groupby('product_id')['basket_count'].sum().nlargest(10)
    logging.info(f"Analiz: En çok satan 10 ürün (product_id) ve toplam satış adetleri:")
    # Raporu temiz tutmak için to_string kullanıyoruz
    logging.info(top_10_products.to_string(name="Toplam Adet"))
    logging.info("(Detaylar için 'top_10_products.png' grafiğine bakınız.)")


    # --- Soru 2: Hangi şehirlerde pazarlama artırılmalı? ---
    logging.info("\n[Soru 2]: Hangi şehirlerde pazarlama artırılmalı?")
    # Müşteri verisinde 'city', 'region' vb. bir kolon var mı?
    if 'city' not in df_customer.columns and 'region' not in df_customer.columns:
        logging.warning("[CEVAP]: Bu soru, mevcut veri setleri ile CEVAPLANAMAMAKTADIR.")
        logging.warning("  Neden: 'customer_details.csv' dosyasında müşterilere ait şehir, bölge veya adres bilgisi bulunmamaktadır.")
    else:
        # (Eğer olsaydı buraya analiz gelecekti)
        logging.info("Müşteri verisinde lokasyon bilgisi tespit edildi, analiz ediliyor...")


    # --- AŞAMA 3: VERİ GÖRSELLEŞTİRME ---
    logging.info("\n--- AŞAMA 3: GÖRSELLEŞTİRME ---")

    # 1. Top 10 Ürün Grafiği (Bar Chart)
    plt.figure(figsize=(12, 7))
    sns.barplot(x=top_10_products.values, y=top_10_products.index.astype(str), palette="viridis", orient='h')
    plt.title('En Çok Satılan 10 Ürün (Toplam Satış Adedine Göre)', fontsize=16, pad=20)
    plt.xlabel('Toplam Satış Adedi', fontsize=12)
    plt.ylabel('Ürün ID (product_id)', fontsize=12)
    plt.tight_layout()
    plt.savefig("top_10_products.png")
    logging.info("Grafik oluşturuldu: 'top_10_products.png'")
    plt.close() # Grafiği kapat

    # 2. Günlük Satış Trendi (Time Series)
    daily_sales = df_basket.groupby(df_basket['basket_date'].dt.date)['basket_count'].sum()
    daily_sales.index = pd.to_datetime(daily_sales.index) # Index'i tekrar datetime yap

    plt.figure(figsize=(14, 7))
    daily_sales.plot(linestyle='-', marker='o', color='b')
    plt.title('Günlük Toplam Satış Trendi (Mayıs-Haziran 2019)', fontsize=16, pad=20)
    plt.xlabel('Tarih', fontsize=12)
    plt.ylabel('Toplam Satış Adedi', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig("daily_sales_trend.png")
    logging.info("Grafik oluşturuldu: 'daily_sales_trend.png'")
    plt.close() # Grafiği kapat
    
    # Satış trendi hakkında kısa bir özet
    logging.info("\nSatış Trendi Özeti:")
    logging.info(f"  Analiz periyodu: {daily_sales.index.min().strftime('%Y-%m-%d')} - {daily_sales.index.max().strftime('%Y-%m-%d')}")
    logging.info(f"  En yoğun satış günü: {daily_sales.idxmax().strftime('%Y-%m-%d')} ({daily_sales.max()} adet)")
    logging.info(f"  En düşük satış günü: {daily_sales.idxmin().strftime('%Y-%m-%d')} ({daily_sales.min()} adet)")


    # --- AŞAMA 4: KRİTİK VERİ KALİTESİ NOTLARI (RAPORLAMA) ---
    logging.info("\n--- AŞAMA 4: KRİTİK VERİ KALİTESİ VE ANALİZ NOTLARI ---")

    # İki veri seti arasındaki eşleşmeyi kontrol et (Kritik sorun)
    basket_customer_ids = set(df_basket['customer_id'].unique())
    customer_detail_ids = set(df_customer['customer_id'].unique())
    
    matching_ids = basket_customer_ids.intersection(customer_detail_ids)
    
    matched_baskets_count = len(df_basket[df_basket['customer_id'].isin(matching_ids)])
    total_baskets_count = len(df_basket)
    match_percentage = (matched_baskets_count / total_baskets_count) * 100

    logging.info(f"[Kritik Sorun]: Müşteri Veri Eşleşmesi")
    logging.info(f"  Sepet verisindeki {total_baskets_count} işlemin SADECE {matched_baskets_count} tanesi ({match_percentage:.2f}%) 'customer_details.csv' tablosundaki bir müşteriyle eşleşebilmiştir.")
    logging.info(f"  Bu durum, 'customer_details.csv' dosyasının (yaş, cinsiyet, vb.) sepet analizleri için KULLANIŞSIZ olduğunu göstermektedir.")
    logging.info(f"  SONUÇ: Yaş, cinsiyet, sadakat (tenure) gibi demografik kırılımlarda yapılacak analizler, toplam satışların sadece %{match_percentage:.2f}'lik kısmını temsil edeceği için YANILTICI olacak ve stratejik kararlarda kullanılmamalıdır.")

    # Yaş verisindeki aykırılıklar (Eşleşen az sayıdaki veriyi kontrol etme)
    if matched_baskets_count > 0:
        merged_df = pd.merge(df_basket, df_customer, on='customer_id', how='inner') # Sadece eşleşenler
        logging.info(f"\n[Aykırı Veri]: Yaş Verisi (Eşleşen {matched_baskets_count} işlem üzerinden)")
        logging.info(f"  Eşleşen verideki 'customer_age' (yaş) istatistikleri:")
        
        age_stats = merged_df['customer_age'].describe()
        logging.info(f"    Min Yaş: {age_stats['min']}")
        logging.info(f"    Max Yaş: {age_stats['max']}")
        logging.info(f"    Ortalama Yaş: {age_stats['mean']:.1f}")
        logging.info(f"  Not: 'min: {age_stats['min']}' ve 'max: {age_stats['max']}' gibi değerler, veri setinde (ör: 123.0 veya 2022.0 gibi) ciddi aykırı değerler ve 'Bilinmiyor' kodlamaları olduğunu göstermektedir. Bu, müşteri veri tabanının temizlenmesi gerektiğini teyit etmektedir.")


    logging.info("\n\n" + "="*60)
    logging.info("--- ANALİZ RAPORU TAMAMLANDI ---")
    logging.info("="*60)

except Exception as e:
    logging.error(f"\n!!! ANALİZ SIRASINDA BEKLENMEDİK BİR HATA OLUŞTU !!!")
    logging.error(f"Hata Detayı: {e}")
    import traceback
    logging.error(f"Traceback: {traceback.format_exc()}")
finally:
    # Logger'ı kapat
    for handler in logging.root.handlers[:]:
        handler.close()
        logging.root.removeHandler(handler)
