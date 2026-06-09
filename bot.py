import feedparser
import time
import os
import requests
from flask import Flask
from threading import Thread

# Web sunucusu
app = Flask(__name__)
@app.route('/')
def home(): return "Bot aktif."
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def check_rss():
    # Buraya rss.app gibi bir servisten aldığın RSS linkini koy
    rss_url = "https://rss.app/feeds/PPYc94ZN5R9ZQc4e.xml"
    feed = feedparser.parse(rss_url)
    if feed.entries:
        return feed.entries[0].title # En son tweet başlığı
    return None

last_title = ""
while True:
    new_title = check_rss()
    if new_title and new_title != last_title:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": f"Yeni tweet: {new_title}"})
        last_title = new_title
    time.sleep(600) # 10 dakikada bir kontrol et
