## SI 206 Fall 2017
## Final Project
## Your name: Frankie Antenucci

import unittest
import itertools
import collections
import re #regex for retrieving date
import json
import sqlite3
import facebook
import facebookinfo #file containing Facebook access token
import requests
import datetime #created_time into Weekday
import plotly #for bar graph visualization
import plotly.plotly as py
import plotly.graph_objs as go
import plotlyinfo #file containing Plotly username and access token


## Creating cache file name
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
fb_access_token = facebookinfo.fb_access_token #user Facebook access code
fb_user = '/me' #accessing myself as the user
fb_feature = '/feed' #accessing my timeline as the feature being pulled from Facebook


## Utilizing Facebook API for social media site
def get_facebook_info(user):
    fb_url = 'https://graph.facebook.com/v2.11/' + fb_user + fb_feature
    url_params = {}
    url_params['access_token'] = fb_access_token #accesstoken from facebookinfo.py file
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
        return CACHE_DICTION[user]
post_data = get_facebook_info(fb_user) #timeline data in finalproject.json
# print(post_data)


## Finding the days the interactions from user timeline took place
def day_of_week(post): #function for converting created_time to day of the week
    date = post['created_time'] #from json dictionary
    # print(date)
    match = re.match(r'(\d+\-\d{2}\-\d{2})', date) #regex to match the date before "T" character
    # print(match)
    if match: #once matched
        date1 = match.group(1)
        day_of_week = datetime.datetime.strptime(date1, '%Y-%m-%d').strftime('%A') #converting date to day
        # print(day_of_week)
    return day_of_week


## Counting the number of posts for each day of the week
days_dict = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0} #initalizing dictionary
for post in post_data['data']:
    day = day_of_week(post) #calling day_of_week function
    if day == 'Monday':
        days_dict['Monday'] += 1
    if day == 'Tuesday':
        days_dict['Tuesday'] += 1
    if day == 'Wednesday':
        days_dict['Wednesday'] += 1
    if day == 'Thursday':
        days_dict['Thursday'] += 1
    if day == 'Friday':
        days_dict['Friday'] += 1
    if day == 'Saturday':
        days_dict['Saturday'] += 1
    if day == 'Sunday':
        days_dict['Sunday'] += 1
print(days_dict) #printing dictionary to display number of posts for each day of the week


## Writing data into database
conn = sqlite3.connect('finalproject.sqlite') #writing sqlite file
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Posts') #creating Posts table
cur.execute('CREATE TABLE Posts (story TEXT, created_time DATETIME, message TEXT, day_of_week TEXT)')

for post in post_data['data']:
    try: #some posts only have a 'story' or a 'message'
        post_tup = post['story'], post['created_time'], day_of_week(post) #if 'story' for post
        cur.execute('INSERT OR IGNORE INTO Posts (story, created_time, day_of_week) VALUES (?, ?, ?)', post_tup) #add to Posts table in database
    except:
        post_tup = post['message'], post['created_time'], day_of_week(post) #if not 'story' but 'message' for post
        cur.execute('INSERT OR IGNORE INTO Posts (message, created_time, day_of_week) VALUES (?, ?, ?)', post_tup) #add to Posts table in database
conn.commit()


## Creating visualization of number of posts per day on Facebook
fb_access_token = facebookinfo.fb_access_token
plotly_username = plotlyinfo.plotly_username
plotly_access_token = plotlyinfo.plotly_access_token
plotly.tools.set_credentials_file(username = plotly_username, api_key = plotly_access_token) #initalizing plotly API
x_axis = list(days_dict.keys()) #x-axis containing the keys (days of the week) of the day_of_week dictionary
y_axis = list(days_dict.values()) #y-axis containing the values (number of posts) of the day_of_week dictionary
graph = [go.Bar(
            x = x_axis,
            y = y_axis,
            marker = dict(
            color = 'rgb(79, 239, 228)', #teal blue color for bars on graph
            line = dict(
                    color = 'black', #black outline for bars on graph
                    width = 2, #width of outline on bars
            )
        )
    )]
layout = go.Layout(
            title = 'Frequency of Facebook Posts by Day for Last 100 Interactions', #title of the graph
            xaxis = dict(
                    title = 'Day of the Week' #title of the x-axis
            ),
            yaxis = dict(
                    title = 'Number of Posts' #title of the y-axis
            ),
            plot_bgcolor = 'rgb(217, 221, 226)' #gray background color for the graph

)
fig = go.Figure(data = graph, layout = layout)
py.plot(fig, filename = 'facebook-bar') #plotting bar graph of number of posts per day on Facebook
