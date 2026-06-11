import feedparser
import time
import os
import requests
import threading
from flask import Flask

app = Flask(__name__)

# ÇEVRE DEĞİŞKENLERİ
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
RSS_URL = "https://rss.app/feeds/ufSAESC67kjoyb0A.xml"

# HAFIZA (Son 10 tweeti tutacak liste)
sent_links = []

@app.route('/')
def home():
    return "Bot aktif ve tarama yapıyor.", 200

def check_rss():
    global sent_links
    try:
        feed = feedparser.parse(RSS_URL)
        if feed.entries:
            entry = feed.entries[0]
            # Linkin sonundaki ID'yi alıyoruz (Daha güvenli)
            tweet_id = entry.link.split('/')[-1]
            
            if tweet_id not in sent_links:
                msg = f"📢 **Yeni Tweet**\n\n{entry.link}"
                res = requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                    data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
                )
                
                if res.status_code == 200:
                    sent_links.append(tweet_id)
                    # Sadece son 10 ID'yi tut
                    if len(sent_links) > 10:
                        sent_links.pop(0)
                    print(f"Gönderildi: {tweet_id}")
            else:
                print("Yeni tweet yok (Hafızada mevcut).")
                
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
        time.sleep(120) # 2 dakikada bir kontrol

if __name__ == "__main__":
    threading.Thread(target=worker, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    
