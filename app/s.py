# Subscriber that has subscribed to the redis channel englishpal-channel and listens to it for new messages

import redis
import time
import json
import pprint

class Frequency:
    def __init__(self, d={}):
        self.freq_dict = d

    def accumulate(self, d):
        ''' Accumulate the frequency of each word given the new word information.
            d looks like {'word': 'architecture'}
        '''
        for k in d:
            word = d[k]
            if word in self.freq_dict:
                self.freq_dict[word] += 1
            else:
                self.freq_dict[word] = 1


r = redis.Redis(host='localhost', port=6379, db=0)
pubsub = r.pubsub(ignore_subscribe_messages=True)
pubsub.subscribe('englishpal-channel')

freq = Frequency()

# Keep getting message (if any) from the channel englishpal-channel
for message in pubsub.listen():
    print(message)            
    d = json.loads(message['data'])
    freq.accumulate(d)
    pprint.pprint(freq.freq_dict)
