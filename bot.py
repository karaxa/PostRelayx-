import os
import requests
import time
import sys
from flask import Flask
from threading import Thread

# 1. Port hatasını susturan web sunucusu
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

# 2. Bot İşlevleri
sys.stdout.reconfigure(line_buffering=True)
print("--- SİSTEM BAŞLADI ---")

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TWITTER_USERNAME = "Adememrem1"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload, timeout=10)
        print("Telegram mesajı gönderildi.")
    except Exception as e:
        print(f"TELEGRAM GÖNDERİM HATASI: {e}")

def get_latest_tweets():
    url = f"https://syndication.twitter.com/srv/timeline-profile?screen_name={TWITTER_USERNAME}"
    try:
        response = requests.get(url, timeout=15)
        print(f"DEBUG: API Durum Kodu: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            tweets = data.get("timeline", [])
            if tweets:
                # En son tweet metnini döndür
                text = tweets[0].get("text")
                print(f"DEBUG: Çekilen tweet: {text[:30]}...")
                return text
            else:
                print("DEBUG: API yanıt verdi ama tweet bulunamadı.")
        else:
            print(f"DEBUG: API hatası, kod: {response.status_code}")
        return None
    except Exception as e:
        print(f"TWITTER/API HATASI: {e}")
        return None

# İlk çalıştığında bağlantıyı test et
send_to_telegram("Bot başarıyla başlatıldı ve izlemeye başladı!")

# Ana Döngü
last_tweet = ""
while True:
    print("Tweetler kontrol ediliyor...")
    tweet_text = get_latest_tweets()
    
    if tweet_text:
        if tweet_text != last_tweet:
            send_to_telegram(tweet_text)
            last_tweet = tweet_text
        else:
            print("Yeni tweet yok (aynı tweet).")
    
    time.sleep(300) # 5 dakika bekle
