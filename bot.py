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
            # Sadece daha önce paylaşılmamış olanları al
            new_entries = [e for e in feed.entries if e.link != last_link]
            
            # Eğer yeni tweet varsa, en eskiden başlayarak sırayla gönder
            if new_entries:
                for entry in reversed(new_entries):
                    # Sadece başlık ve link - RT/Alıntı karmaşasını önlemek için en temiz yol
                    msg = f"📢 **Yeni Tweet**\n\n{entry.link}"
                    
                    res = requests.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                        data={
                            "chat_id": CHAT_ID, 
                            "text": msg, 
                            "parse_mode": "Markdown"
                        }
                    )
                    
                    last_link = entry.link
                    # Mesajların "pat" diye değil, sıra ile gelmesi için bekleme
                    time.sleep(5) 
                    
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
        # RSS'i 2 dakikada bir kontrol etmeye devam et
        time.sleep(120)

if __name__ == "__main__":
    threading.Thread(target=worker, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
