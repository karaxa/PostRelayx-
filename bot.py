import feedparser
import time
import os
import requests
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def check_rss():
    # RSS.app'den aldığın linki buraya yaz
    rss_url = "https://rss.app/feeds/HXScZ2SZ5dwrKNp4.xml" 
    feed = feedparser.parse(rss_url)
    if feed.entries:
        entry = feed.entries[0]
        # Görseli bulmaya çalış (rss.app bunu summary içinde verir)
        image_url = None
        if 'media_content' in entry:
            image_url = entry.media_content[0]['url']
        
        return {
            "link": entry.link,
            "title": entry.title,
            "image": image_url
        }
    return None

def send_telegram(tweet):
    base_url = f"https://api.telegram.org/bot{TOKEN}"
    text = f"Yeni tweet paylaşıldı!\n\n{tweet['title']}\n\nLink: {tweet['link']}"
    
    # Eğer görsel varsa sendPhoto, yoksa sendMessage kullan
    if tweet['image']:
        requests.post(f"{base_url}/sendPhoto", data={"chat_id": CHAT_ID, "photo": tweet['image'], "caption": text})
    else:
        requests.post(f"{base_url}/sendMessage", data={"chat_id": CHAT_ID, "text": text})

# Ana döngü
last_link = ""
while True:
    new_tweet = check_rss()
    if new_tweet and new_tweet['link'] != last_link:
        send_telegram(new_tweet)
        last_link = new_tweet['link']
    time.sleep(600)
    
