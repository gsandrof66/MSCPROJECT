import os, tweepy, pandas as pd
from datetime import datetime


def log(mytext):
    with open("./file.txt", "a") as file:
        file.write(mytext)

def GetTweets(palabra, num_tweets, language):
    log("Start: " + str(datetime.now()) + "\n")
    try:
        auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
        auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"])
        api = tweepy.API(auth)
        listado_tweet = []
        for tweet in api.search_tweets(q=palabra + ' -filter:retweets', count=num_tweets, lang=language):
            try:
                tweetcleaned = (tweet.text).replace("\n"," ")
                tweetcleaned = tweetcleaned.strip()
                tlocal = tweet.user.location
                if len(tlocal) == 0:
                    tlocal = 'None'
                listado_tweet.append({"fecha": tweet.created_at,"tweet": tweetcleaned
                                    , "user": tweet.user.screen_name,"local": tlocal})
            except tweepy.TweepError as e:
                log(e)
            except StopIteration:
                break
    except Exception as e:
        log(e)
        return
    try:
        df = pd.DataFrame(listado_tweet)
        df.to_csv("./dftweets.csv", mode='a', header=False, index=False)
    except Exception as e:
        log(e)
    log("End: " + str(datetime.now()) + "\n")

if __name__ == "__main__":
    # GetTweets('disability accessibility', 5, 'en')
    print("Hello")