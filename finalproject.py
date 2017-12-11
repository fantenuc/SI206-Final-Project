## SI 206 2017
## Final Project
## Your name: Frankie Antenucci

import unittest
import itertools
import collections
import re
import json
import sqlite3
import facebook
import facebookinfo #file containing Facebook access token
import requests
from datetime import datetime #how to make a datetime into a weekday
import calendar

CACHE_FNAME = "finalproject.json"

## Initializing Caching Setup
try:
    cache_file = open(CACHE_FNAME,'r') #opens and reads file
    cache_contents = cache_file.read() #converts contents to string
    cache_file.close() #closes file
    CACHE_DICTION = json.loads(cache_contents) #loads contents to dictionary
except:
    CACHE_DICTION = {}

## Accessing access token from facebookinfo.py
fb_access_token = facebookinfo.fb_access_token
fb_user = '/me' #accessing myself as the user
fb_feature = '/feed' #accessing my timeline as the feature being pulled from Facebook


## Utilizing Facebook API for social media site
def get_facebook_info(user):
    fb_url = 'https://graph.facebook.com/v2.11/' + fb_user + fb_feature
    url_params = {}
    url_params['access_token'] = fb_access_token
    url_params['limit'] = 100 #accessing 100 interactions from user timeline

    if user in CACHE_DICTION:
        print('Accessing Cached Data') #access cached data if user in dictionary
        return CACHE_DICTION[user]
    else:
        print('Using Facebook API') #access Facebook API if user not in dictionary
        facebook_results = requests.get(fb_url, params = url_params)
        CACHE_DICTION[user] = json.loads(facebook_results.text)

        f = open(CACHE_FNAME, 'w') #writing json
        f.write(json.dumps(CACHE_DICTION, indent = 2)) #indent for easier read
        f.close()
        return facebook_results

information = get_facebook_info(fb_user) #printing the timeline data in finalproject.json
# print(information)


## Finding the days the interactions from user timline took place
for post in information['data']:
    date = post['created_time']
    # print(date)
    match = re.match(r'(\d+\-\d{2}\-\d{2})', date)
    print(match)
    if match:
        date1 = match.group(1)
        day_of_week = datetime.datetime.strptime(date1, '%Y-%m-%d').strftime('%A')
        print(int(day_of_week))




# conn = sqlite3.connect('final_project.sqlite') #writing sqlite file
# cur = conn.cursor()
