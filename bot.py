import feedparser
import time
import os
import requests
from flask import Flask
from threading import Thread

# ... (web sunucusu kısmı aynı kalsın)

def check_rss():
    rss_url = "https://rss.app/feeds/HXScZ2SZ5dwrKNp4.xml"
    try:
        feed = feedparser.parse(rss_url)
        if feed.entries:
            # Sadece başlığı değil, tweetin linkini alıyoruz (Bu benzersizdir)
            return feed.entries[0].link 
        return None
    except:
        return None

last_link = "" # Başlangıçta boş
while True:
    new_link = check_rss()
    
    # Sadece link gerçekten değiştiyse (yani yeni tweetse) işlem yap
    if new_link and new_link != last_link:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": f"Yeni tweet paylaşıldı: {new_link}"})
        
        # ÖNEMLİ: En son gönderilen linki artık 'last_link' olarak kaydet
        last_link = new_link 
    
    time.sleep(600) 
