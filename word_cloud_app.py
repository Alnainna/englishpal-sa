from flask import Flask, jsonify, send_file
import redis
from threading import Thread
from wordcloud import WordCloud
import matplotlib.pyplot as plt

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
pubsub = redis_client.pubsub()
pubsub.subscribe('englishpal')

words = {}

def listen_to_redis():
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data'].decode('utf-8')
            word = data.split(':')[1]
            if word in words:
                words[word] += 1
            else:
                words[word] = 1

Thread(target=listen_to_redis).start()

@app.route('/wordcloud')
def word_cloud():
    wc = WordCloud(width=800, height=400).generate_from_frequencies(words)
    plt.figure(figsize=(20, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('/mnt/data/wordcloud.png')
    return send_file('/mnt/data/wordcloud.png', mimetype='image/png')

@app.route('/histogram')
def histogram():
    plt.figure(figsize=(10, 5))
    plt.bar(words.keys(), words.values())
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('/mnt/data/histogram.png')
    return send_file('/mnt/data/histogram.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(port=5000)
