## SI 206 2017
## Final Project
## Your name: Frankie Antenucci

import unittest
import itertools
import collections
import json
import sqlite3
import facebook
import facebook_info
import requests
# import datetime how to make a datetime into a weekday


CACHE_FNAME = "final_project.json"

try:
    cache_file = open(CACHE_FNAME,'r') #opens and reads file
    cache_contents = cache_file.read() #converts contents to string
    cache_file.close() #closes file
    CACHE_DICTION = json.loads(cache_contents) #loads contents to dictionary
except:
    CACHE_DICTION = {}


fb_access_token = facebook_info.fb_access_token
fb_user = facebook_info.fb_user
fb_feature = '/feed'


def get_facebook_info(user):
    fb_url = 'https://graph.facebook.com/v2.11/' + fb_user + fb_feature
    url_params = {}
    url_params['access_token'] = fb_access_token
    url_params['limit'] = 100

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

information = get_facebook_info(fb_user)
print(information)


conn = sqlite3.connect('final_project.sqlite') #writing sqlite file
cur = conn.cursor()
