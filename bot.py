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
RSS_URL = "https://rss.app/feeds/ufSAESC67kjoyb0A.xml" # Kendi linkini buraya yapıştır

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
            if entry.link != last_link:
                # 1. Metni 200 karakterde kesme işlemi
                short_title = (entry.title[:200] + '...') if len(entry.title) > 200 else entry.title
                
                # 2. Mesaj formatı
                msg = f"📢 **Yeni Tweet**\n\n📌 {short_title}\n🔗 {entry.link}"
                
                # 3. Telegram'a gönderim (Önizleme AKTİF - disable_web_page_preview kaldırıldı)
                res = requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                    data={
                        "chat_id": CHAT_ID, 
                        "text": msg, 
                        "parse_mode": "Markdown"
                    }
                )
                print(f"Telegram Gönderim Durumu: {res.status_code}")
                last_link = entry.link
            else:
                print("Yeni tweet yok, bekleniyor...")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def keep_alive():
    while True:
        try:
            requests.get("https://ollo-hwvh.onrender.com/") 
        except:
            pass
        time.sleep(300)

def worker():
    while True:
        check_rss()
        time.sleep(120)

if __name__ == "__main__":
    threading.Thread(target=worker, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
