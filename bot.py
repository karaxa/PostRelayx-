import os
import requests
import time
import sys
from flask import Flask
from threading import Thread

# Web Sunucusu (Render için)
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

# Bot Ayarları
sys.stdout.reconfigure(line_buffering=True)
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
TWITTER_USERNAME = "Adememrem1"

def get_latest_tweets():
    # BeautifulSoup kullanmadan basit yöntem
    url = f"https://nitter.net/{TWITTER_USERNAME}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            # Sayfa içeriğinde basit bir arama yapıyoruz
            # Nitter yapısında tweet içerikleri genellikle bu class içindedir
            content = response.text
            # Çok basit bir ayıklama (en son tweeti bulmaya çalışır)
            if "tweet-content" in content:
                return "Yeni tweet mevcut (Nitter üzerinden tespit edildi)."
        return None
    except Exception as e:
        print(f"HATA: {e}")
        return None

# Ana Döngü
while True:
    print("Tweetler kontrol ediliyor...")
    tweet_text = get_latest_tweets()
    if tweet_text:
        print(tweet_text)
    time.sleep(300)
    
