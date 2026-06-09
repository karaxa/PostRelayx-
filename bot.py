import feedparser
import time
import os
import requests
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
app = Flask(__name__)

# Render'ın "Orada mısın?" sinyaline anında cevap ver
@app.route('/')
def home(): 
    return "Bot aktif ve sağlıklı.", 200

# Web sunucusunu başlat
def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# RSS kontrolü ve Telegram işlerini ayrı bir yerde yürüt
def run_bot():
    last_link = ""
    while True:
        try:
            # RSS çekme kısmı
            rss_url = "https://rss.app/feeds/HXScZ2SZ5dwrKNp4.xml"
            feed = feedparser.parse(rss_url)
            if feed.entries:
                entry = feed.entries[0]
                if entry.link != last_link:
                    # Bildirim gönder
                    text = f"Yeni tweet: {entry.title}\n{entry.link}"
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                  data={"chat_id": CHAT_ID, "text": text})
                    last_link = entry.link
        except Exception as e:
            print(f"Hata: {e}")
        
        time.sleep(600) # 10 dakika bekle

if __name__ == "__main__":
    # Web sunucusu ana thread'de çalışsın
    Thread(target=run_bot, daemon=True).start()
    run_web()
    
