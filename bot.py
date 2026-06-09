import feedparser
import time
import os
import sys
import requests
from flask import Flask
from threading import Thread

# 1. Ayarları güvenli al
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Eğer değerler girilmediyse botu hata vererek durdur
if not TOKEN or not CHAT_ID:
    print("HATA: BOT_TOKEN veya CHAT_ID Render panelinde tanımlı değil!")
    sys.exit(1)

# 2. Web Sunucusu (Render için)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot aktif."

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# 3. RSS Kontrolü
def check_rss():
    # https://rss.app/feeds/HXScZ2SZ5dwrKNp4.xml
    rss_url = "https://rss.app/feeds/..." 
    try:
        feed = feedparser.parse(rss_url)
        if feed.entries:
            return feed.entries[0].link # En son linki al
    except Exception as e:
        print(f"RSS Hatası: {e}")
    return None

# 4. Ana Döngü
if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()
    
    last_link = ""
    print("--- BOT BAŞLATILDI VE İZLİYOR ---")
    
    while True:
        new_link = check_rss()
        
        # Sadece yeni ve farklı bir linkse gönder
        if new_link and new_link != last_link:
            try:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                              data={"chat_id": CHAT_ID, "text": f"Yeni tweet paylaşıldı: {new_link}"})
                print(f"Bildirim gönderildi: {new_link}")
                last_link = new_link
            except Exception as e:
                print(f"Telegram Gönderme Hatası: {e}")
        
        time.sleep(600) # 10 dakika bekle
