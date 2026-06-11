import feedparser
import time
import os
import requests
import threading
from flask import Flask

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
RSS_URL = "https://rss.app/feeds/ufSAESC67kjoyb0A.xml"

# Botun hafızası: Son gönderilen 10 linki burada tutuyoruz
sent_links = [] 

@app.route('/')
def home():
    return "Bot aktif ve tarama yapıyor.", 200

def check_rss():
    global sent_links
    try:
        feed = feedparser.parse(RSS_URL)
        if feed.entries:
            # En son gelen tweet (RSS.app beslemesinin en başındaki)
            entry = feed.entries[0]
            
            # Eğer bu link daha önce gönderilenler listesinde YOKSA:
            if entry.link not in sent_links:
                msg = f"📢 **Yeni Tweet**\n\n{entry.link}"
                
                res = requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                    data={
                        "chat_id": CHAT_ID, 
                        "text": msg, 
                        "parse_mode": "Markdown",
                        "disable_web_page_preview": "False" 
                    }
                )
                
                # Eğer gönderim başarılıysa, bu linki hafızaya ekle
                if res.status_code == 200:
                    sent_links.append(entry.link)
                    # Hafızayı sadece son 10 linkle sınırla (gereksiz yer kaplamasın)
                    if len(sent_links) > 10:
                        sent_links.pop(0)
                        
                print(f"Telegram Gönderim Durumu: {res.status_code}")
            else:
                print("Tweet zaten gönderilmiş, pas geçildi.")
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
        time.sleep(3600) # 60 dakika (RSS.app ile uyumlu)

if __name__ == "__main__":
    threading.Thread(target=worker, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
