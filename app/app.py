from flask import Flask, render_template, jsonify
import redis
import json
import threading
from collections import Counter

app = Flask(__name__)

# Initialize Redis connection
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()  # Check if Redis is running
    print("Connected to Redis")
except redis.ConnectionError as e:
    print(f"Redis connection error: {e}")
    raise

pubsub = r.pubsub(ignore_subscribe_messages=True)
pubsub.subscribe('englishpal')

word_counter = Counter()

class Frequency:
    def __init__(self, d={}):
        self.freq_dict = d

    def accumulate(self, d):
        ''' Accumulate the frequency of each word given the new word information.
            d looks like {'word': 'architecture'}
        '''
        for k in d:
            word = d[k]
            word_counter[word] += 1
        print(f"Updated word counter: {word_counter}")

freq = Frequency()

def listen_to_redis():
    print("Listening to Redis...")
    for message in pubsub.listen():
        print(f"Message from Redis: {message}")
        if message['type'] == 'message':
            try:
                d = json.loads(message['data'])
                print(f"Received data: {d}")
                freq.accumulate(d)
            except Exception as e:
                print(f"Error processing message: {e}")

# Start a background thread to listen to Redis
listener_thread = threading.Thread(target=listen_to_redis)
listener_thread.daemon = True
listener_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/word_cloud')
def word_cloud():
    return render_template('word_cloud.html')

@app.route('/histogram')
def histogram():
    return render_template('histogram.html')

@app.route('/data')
def data():
    words = [{'word': word, 'count': count} for word, count in word_counter.items()]
    words = sorted(words, key=lambda x: x['count'], reverse=True)
    print(f"Data endpoint returning: {words}")
    return jsonify(words)

if __name__ == '__main__':
    app.run(debug=True)
