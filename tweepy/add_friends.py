# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from tcred import consumer_key as consumer_key
from tcred import consumer_secret as consumer_secret
from tcred import access_token as access_token
from tcred import access_token_secret as access_token_secret
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


print("Starting at: ",dt.now())

### Try to set cursor...
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# rate_info = api.rate_limit_status()['resources']
# for x in rate_info:
#         try:
#             print(rate_info[x])
#         except:
#             print("fail: ",x)
#             pass

# rate_info = api.rate_limit_status()['resources']
# for x in rate_info:
#         for xx in rate_info[x]:
#             try:
#                 if rate_info[x][xx]['remaining'] < 10:
#                     print(x," ",xx," remaining: ",rate_info[x][xx]['remaining'])
#                     print(x," ",xx," reset time: ",dt.utcfromtimestamp(rate_info[x][xx]['reset']))
#                     time.sleep(15*60*1)
#                     #print(dt.now() - dt.utcfromtimestamp(rate_info[x][xx]['reset']))
#             except:
#                 print("fail: ",x,xx)
#                 pass

main = pd.read_csv("data.csv")

# friends df
fdf = pd.DataFrame()

for i,usn in enumerate(main.loc[pd.notnull(main.user_screen_name),"user_screen_name"].tolist()):
    if i > 1: break
    temp_df = pd.DataFrame()


    for ii, friend in enumerate(tweepy.Cursor(api.friends,id=usn).items()):
        #if ii > 1: break
        
        #time.sleep(1)

        rate_info = api.rate_limit_status()['resources']
        for x in rate_info:
            for xx in rate_info[x]:
                try:
                    if rate_info[x][xx]['remaining'] < 10:
                        print(x," ",xx," remaining: ",rate_info[x][xx]['remaining'])
                        print(x," ",xx," reset time: ",dt.utcfromtimestamp(rate_info[x][xx]['reset']))
                        print("Stalling 15 minutes :<")
                        print(dt.now())
                        time.sleep(15*60*1)
                        print("Continuing")
                        print(dt.now())
                        #print(dt.now() - dt.utcfromtimestamp(rate_info[x][xx]['reset']))
                except:
                    print("fail: ",x,xx)
                    pass

        try:
            print(i," ",usn,"friend: ",friend.screen_name)
            temp_df2 = pd.DataFrame()
            temp_df2["user_screen_name"] = usn
            temp_df2["friend"] = friend.screen_name
            temp_df = temp_df.append(temp_df2)
            fdf = fdf.append(temp_df)
        except:
            try:
                print("Stalling 5 minutes :<")
                print(dt.now())
                time.sleep(5*60*1)
                print("let's go again")
                print(usn,"friend: ",friend.screen_name)
                temp_df2 = pd.DataFrame()
                temp_df2["user_screen_name"] = usn
                temp_df2["friend"] = friend.screen_name
                temp_df = temp_df.append(temp_df2)
                fdf = fdf.append(temp_df)
            except:
                print("Stalling 15 minutes :<")
                print(dt.now())
                time.sleep(10*60*1)
                print("let's go again")
                print(usn,"friend: ",friend.screen_name)
                temp_df2 = pd.DataFrame()
                temp_df2["user_screen_name"] = usn
                temp_df2["friend"] = friend.screen_name
                temp_df = temp_df.append(temp_df2)
                fdf = fdf.append(temp_df)

        time.sleep(0.1)


    # unfortunately twitter limit is 15 calls each 15 minutes... :<


fdf.to_csv("fdf.csv")


