import json
import sys
from datetime import datetime, timedelta

from tweepy import StreamListener, OAuthHandler, Stream

streaming_duration_in_seconds = 30


class StdOutListener(StreamListener):
    def __init__(self):
        super().__init__()
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=streaming_duration_in_seconds)
        self.hashtag_frequency = {}

    def on_data(self, data):
        hashtags = json.loads(data)["entities"]["hashtags"]
        for hashtag in hashtags:
            text = hashtag["text"]
            self.hashtag_frequency[text] = self.hashtag_frequency.get(text, 1) + 1
        if datetime.now() > self.end_time:
            for i in sorted(
                    self.hashtag_frequency.items(),
                    key=lambda x: self.hashtag_frequency[x[0]],
                    reverse=True
            )[:10]:
                print(i[0], '->', i[1])
            print("*********************Streaming end.*********************")
            sys.exit(0)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler('CONSUMER_KEY', 'CONSUMER_SECRET')
    auth.set_access_token('ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET')

    stream = Stream(auth, listener)

    stream.filter(track=['testing'])
