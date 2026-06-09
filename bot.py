import os
import requests
import time
import sys
from flask import Flask
from threading import Thread

# Logların anlık akması için
sys.stdout.reconfigure(line_buffering=True)
print("--- BOT BAŞLATILDI ---")

# 1. Web Sunucusu (Render için)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot aktif."

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

t = Thread(target=run_web)
t.daemon = True
t.start()

# 2. Bot Ayarları
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TWITTER_USERNAME = "Adememrem1"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload, timeout=10)
        print("Telegram'a mesaj gönderildi.")
    except Exception as e:
        print(f"Telegram Hatası: {e}")

def get_latest_tweets():
    # Nitter üzerinden kontrol
    url = f"https://nitter.net/{TWITTER_USERNAME}"
    try:
        response = requests.get(url, timeout=15)
        print(f"DEBUG: Nitter Yanıt Kodu: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            # 'timeline' anahtar kelimesini arıyoruz
            if "timeline" in content:
                print("DEBUG: Sayfada zaman akışı (timeline) bulundu.")
                return "Yeni içerik mevcut."
            else:
                print(f"DEBUG: Sayfa açıldı ama 'timeline' bulunamadı. İçerik uzunluğu: {len(content)}")
        return None
    except Exception as e:
        print(f"DEBUG: Bağlantı Hatası: {e}")
        return None

# Test mesajı
send_to_telegram("Bot başarıyla başlatıldı ve izlemeye başladı!")

# Ana Döngü
last_status = None
while True:
    print("Tweetler kontrol ediliyor...")
    status = get_latest_tweets()
    
    if status and status != last_status:
        send_to_telegram("Adememrem1 hesabında yeni bir hareketlilik tespit edildi!")
        last_status = status
    
    time.sleep(300) # 5 dakika bekle
