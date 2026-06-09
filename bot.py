import os
import requests
import time
import sys
from flask import Flask
from threading import Thread

# 1. PORT HATASINI GİDEREN KISIM (Render için)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot aktif ve çalışıyor."

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Web sunucusunu arka planda başlat
t = Thread(target=run_web)
t.daemon = True
t.start()

# 2. BOTUN GERÇEK İŞLEVİ
sys.stdout.reconfigure(line_buffering=True)
print("--- BOT BAŞLATILDI ---")

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TWITTER_USERNAME = "Adememrem1"

def get_latest_tweets_syndication():
    # Twitter'ın herkese açık syndication API'si (RSS yerine daha stabil)
    url = f"https://syndication.twitter.com/srv/timeline-profile?screen_name={TWITTER_USERNAME}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            tweets = data.get("timeline", [])
            if tweets:
                # En son tweetin metni
                return tweets[0].get("text")
        return None
    except Exception as e:
        print(f"HATA: {e}")
        return None

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

# Ana Döngü
last_tweet = ""
while True:
    print("Tweetler kontrol ediliyor...")
    tweet_text = get_latest_tweets_syndication()
    
    if tweet_text and tweet_text != last_tweet:
        send_to_telegram(tweet_text)
        last_tweet = tweet_text
        print("Yeni tweet bulundu!")
    
    time.sleep(300) # 5 dakika bekle
