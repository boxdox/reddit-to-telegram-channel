#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import praw
from dotenv import load_dotenv
import requests
import os
import random

load_dotenv()

class Reddit_To_Telegram:
    def __init__(self, user_agent, subreddit, chat_id, logfile="posted.txt"):
        self.id = os.getenv("REDDIT_CLIENT_ID")
        self.secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.username = os.getenv("REDDIT_USERNAME")
        self.password = os.getenv("REDDIT_PASSWORD")
        self.telegram_api_key = os.getenv("TELEGRAM_API_KEY")
        self.subreddit = subreddit
        self.chat_id = chat_id
        self.user_agent = user_agent
        self.logfile = logfile

        # Create the logfile if not exists
        if os.path.exists(self.logfile) == False:
            with open(self.logfile, 'w+'):
                pass
        
        # Initialize PRAW
        self.reddit = praw.Reddit(client_id=self.id, 
                     client_secret=self.secret, 
                     username=self.username, 
                     password=self.password, 
                     user_agent=self.user_agent)
    
    def get_top_posts(self, time='day', limit=10):
        top_posts_from_subreddit = self.reddit.subreddit(self.subreddit).top(time, limit=limit)
        return [post.url for post in top_posts_from_subreddit]
    
    # Gets the list of posted items from logfile
    def get_list_of_posted_items(self):
        with open(self.logfile, 'r') as f:
            return [line.strip() for line in f]

    # Select a post which is not posted from array of top_posts
    def select_a_post(self, time="day", limit=10):
        posts = self.get_top_posts(time, limit)
        posted = self.get_list_of_posted_items()
        return random.choice(list(set(posts) - set(posted)))

    def post_to_telegram(self, post, caption=""):
        try:
            r = requests.get('https://api.telegram.org/bot{}/sendPhoto'.format(self.telegram_api_key),
                 json={"chat_id": self.chat_id, "photo": post, "caption": caption})
            if r.ok:
                self.prepend_and_limit(post)
                print("Posted. Check your channel")

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)

    # Prepends the url to top of file and removes the last entry if total entries exceed the limit
    def prepend_and_limit(self, url, limit=100):
        with open(self.logfile, 'r') as f:
            content = [x.strip() for x in f]
        content.insert(0, url)
        if len(content) > limit:
            content.pop()
        with open(self.logfile, 'w+') as f:
            f.write('\n'.join(content))