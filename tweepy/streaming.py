# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from tcred import consumer_key as consumer_key
from tcred import consumer_secret as consumer_secret
from tcred import access_token as access_token
from tcred import access_token_secret as access_token_secret
from tcred import gmaps_key as gmaps_key
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd
import time
import googlemaps
from datetime import datetime as dt
import schedule


def geocoding(text):
    gmaps = googlemaps.Client(key=gmaps_key)
    # Geocoding an address
    geocode_result = gmaps.geocode(text)
    return geocode_result


### Try to set cursor...
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
for i, friend in enumerate(tweepy.Cursor(api.friends).items()):
    if i > 10: break
    print(friend.screen_name)


u = api.get_user(783214)
print(u.screen_name)

print("friends gorditou: ")
for i, friend in enumerate(tweepy.Cursor(api.friends,id="cristian_moav").items()):
    if i > 30: break
    print(friend.screen_name)

raw_input("check.")


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        try:
            #

            jdata = [json.loads(data)]
            main_df = pd.read_csv("data.csv")
            df = pd.DataFrame()
            df["created_at"] = map(lambda x: x['created_at'], jdata)
            df["user_location"] = map(lambda x: x['user']['location'], jdata)
            df["user_followers_count"] = map(lambda x: x['user']['followers_count'], jdata)
            df["user_screen_name"] =  map(lambda x: x['user']['screen_name'], jdata)
            try:
                coordinates = map(lambda x: geocoding(x['user']['location']), jdata)
                # address components
                try:
                    addc = coordinates[0][0]["address_components"]
                    addc = [x["long_name"] for x in addc if x["types"][0] == "country"]
                    df["country"] = addc

                except Exception as e:
                    print("Failed getting country: ",str(e))
                # print("coordinates are: ",coordinates)
                df["lat"] = coordinates[0][0]['geometry']['location']['lat']
                df["lng"] = coordinates[0][0]['geometry']['location']['lng']
                
            except Exception as e:
                print('fail geocoding. ', str(e))
                pass
            df["text"] = map(lambda x: x['text'], jdata)
            
            # print(df.head())
            main_df = main_df.append(df)
            main_df = main_df.loc[pd.notnull(main_df["lat"]),:]
            main_df.to_csv("data.csv", index=False, encoding='utf-8')
            print("row added")
            print("len main: ",len(main_df))

        except Exception, e:
            # time.sleep(5)
            print(str(e))
            pass

        return True

    def on_error(self, status):
        print(status)
        pass

# def run_listener():
#     i_time = dt.now()
#     l = StdOutListener()
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)

#     stream = Stream(auth, l)
#     #stream.filter()
#     while 1:
#         stream.filter(track=['messi'], stall_warnings=True)   
#         print(dt.now() )

# run_listener()

# schedule.every(30).minutes.do(import_dels)
# # schedule.every().hour.do(job)
# # schedule.every().day.at("10:30").do(job)

# while 1:
#     schedule.run_pending()
#     time.sleep(1)


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    #stream.filter()
    #stream.filter(track=['antesquenadie','nadie951'], stall_warnings=True)
    stream.filter(track=['messi','cristiano ronaldo'], stall_warnings=True)