import os
import requests
import time
import sys
from flask import Flask
from threading import Thread

# Logları anlık akıt
sys.stdout.reconfigure(line_buffering=True)
print("--- BOT BAŞLATILIYOR ---")

# 1. Web Sunucusu
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot aktif."

def run_web():
    port = int(os.environ.get("PORT", 8080))
    print(f"Web sunucusu {port} portunda başlıyor...")
    app.run(host='0.0.0.0', port=port)

t = Thread(target=run_web)
t.daemon = True
t.start()

# 2. Bot İşlevleri
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TWITTER_USERNAME = "Adememrem1"

def send_to_telegram(text):
    print("Telegram'a mesaj gönderiliyor...")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        r = requests.post(url, data=payload, timeout=10)
        print(f"Telegram yanıtı: {r.status_code}")
    except Exception as e:
        print(f"Telegram Hatası: {e}")

def get_latest_tweets():
    # Nitter üzerinden kontrol
    url = f"https://nitter.net/{TWITTER_USERNAME}"
    print(f"Nitter'a bağlanılıyor: {url}")
    try:
        response = requests.get(url, timeout=15)
        print(f"DEBUG: Nitter Yanıt Kodu: {response.status_code}")
        
        if response.status_code == 200:
            if "tweet-content" in response.text:
                print("DEBUG: Tweet içeriği sayfada bulundu.")
                return "Yeni tweet var!"
            else:
                print("DEBUG: Sayfa açıldı ama 'tweet-content' bulunamadı.")
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
    
    time.sleep(300)
    
