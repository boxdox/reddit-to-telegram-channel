# #!/usr/bin/python3
# -*- coding: utf-8 -*-

import praw
from dotenv import load_dotenv
import requests
import os
import random

# Load the config from .env
load_dotenv()

# Init the PRAW
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

# Creating a user-agent according to reddit api rules
USER_AGENT = "python:memebotforreddit:v1.0 (by /u/boxdox)"

reddit = praw.Reddit(client_id=CLIENT_ID, 
                     client_secret=CLIENT_SECRET, 
                     password=REDDIT_PASSWORD, 
                     username=REDDIT_USERNAME, 
                     user_agent=USER_AGENT)

# Get the top posts of subbreddit `memes`
top_posts_from_subreddit = reddit.subreddit('memes').top('day', limit=10)
top_posts = [posts.url for posts in top_posts_from_subreddit]

# Read the posted file into a list
with open('posted.txt', 'w+') as file:
    lines = [line.strip() for line in file]

# Get the difference set
not_posted = list(set(top_posts) - set(lines))

# Select a post
selected_post = random.choice(not_posted)

# Prepend and Limit, a helper function that prepends to a file and pops
# out last element if length is greater than given limit
#
# I know we are reading same file twice, maybe I'll update it sometime later

def prepend_and_limit(file, url, limit=100):
    with open(file, 'r') as f:
        content = [x.strip() for x in f]
    content.insert(0, url)
    if len(content) > limit:
        content.pop()
    with open(file, 'w+') as f:
        f.write('\n'.join(content))

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# Send a request to Telegram API with the url of photo to send to channel
r = requests.get('https://api.telegram.org/bot{}/sendPhoto'.format(TELEGRAM_API_KEY),
                 json={"chat_id": "@memesforlyf", "photo": selected_post})
if r.ok:
    prepend_and_limit("posted.txt", selected_post)