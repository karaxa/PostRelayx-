import feedparser
import time
import os
import requests
import threading
from flask import Flask

app = Flask(__name__)

# ÇEVRE DEĞİŞKENLERİNİ AL
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
# Buraya RSS linkini tırnak içinde yapıştır
RSS_URL = "https://rss.app/feeds/HXScZ2SZ5dwrKNp4.xml" 

last_link = ""

@app.route('/')
def home():
    return "Bot aktif ve tarama yapıyor.", 200

def check_rss():
    global last_link
    try:
        feed = feedparser.parse(RSS_URL)
        if feed.entries:
            entry = feed.entries[0]
            # Eğer yeni bir tweet varsa ve daha önce gönderilmediyse
            if entry.link != last_link:
                msg = f"Yeni tweet:\n{entry.title}\n{entry.link}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                    data={"chat_id": CHAT_ID, "text": msg})
                print(f"Telegram Gönderim Durumu: {res.status_code}")
                last_link = entry.link
            else:
                print("Yeni tweet yok, bekleniyor...")
    except Exception as e:
        print(f"Hata oluştu: {e}")

# Kendi kendini canlı tutma (Ping) fonksiyonu
def keep_alive():
    while True:
        try:
            # Buradaki linki kendi render linkinle güncelle: https://ollo-hwvh.onrender.com/
            requests.get("https://ollo-hwvh.onrender.com/") 
        except:
            pass
        time.sleep(300) # 5 dakikada bir kendi adresine ping at

def worker():
    while True:
        check_rss()
        time.sleep(120) # 2 dakikada bir RSS kontrolü

if __name__ == "__main__":
    # 1. RSS Kontrolcüsünü başlat
    threading.Thread(target=worker, daemon=True).start()
    # 2. Uyanık kalma ping'ini başlat
    threading.Thread(target=keep_alive, daemon=True).start()
    # 3. Web sunucusunu başlat
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
