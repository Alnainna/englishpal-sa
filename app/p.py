# Publisher
# Publish to channel englishpal-channel a word from a text file
# each second

import redis
import json
import time
from dataclasses import asdict
from event import NewWordAdded

r = redis.Redis(host='localhost', port=6379, db=0) # message broker

with open('simple.txt', encoding='utf8') as f: # pg768.txt can be downloaded from https://www.gutenberg.org/ebooks/768.txt.utf-8
    all_words = f.read().split()
    for word in all_words:
        time.sleep(1)
        r.publish('englishpal-channel', json.dumps(asdict(NewWordAdded(word=word))))
