## Reddit to Telegram Channel
This bot script can select a random top of the day post from reddit and send it to a telegram channel via a bot, while saving the url of post into a file, so as to not post the same image twice.

#### Requirements
```
praw
python-dotenv
```

#### Available Methods
---
#### Get Top Posts
Returns an array of top posts based on time and limit entered (from PRAW)
`get_top_posts(time, limit)`

Parameters:

- `time`: Can be one of: all, day, hour, month, week, year (default: day)
- `limit`: Number of posts to fetch (default: 10)

#### Select a post
Returns a single post. It first calls `get_top_posts`, then calls `get_list_of_posted_items` and chooses a random element from difference of the two.

`select_a_post(time, limit)`
Parameters:
Same as above.

#### Post to Telegram
Sends the given post to the channel.
`get_top_posts(post, caption)`

Parameters:

- `post`: URL of the image.
- `caption`: Caption for the `post` (Optional)


#### How to?
1. Git clone this repo
2. Rename .env.example to .env
3. Replace all data in .env with your own
4. Create a virtual environment (optional)
5. Run `pip install -r requirements.txt`
6. Create a new file named `bot.py` with the following contents:
```py
from reddit_to_telegram import Reddit_to_telegram

x = Reddit_To_Telegram(user_agent, subreddit, channel_name)

selected_post = x.select_a_post()

x.post_to_telegram(selected_post)
```

#### TODO
- [x] ~~Enclose into a function for easier calling~~ Converted to class
- [x] Generalize this for any subreddit
- [ ] Allow calling multiple subreddits
- [ ] Generate a dockerfile (update: testing this.)

#### Licence
[MIT 2020](https://boxdox.mit-license.org/)