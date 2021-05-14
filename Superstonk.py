import praw
import os
from praw.models import MoreComments
import random
from dotenv import load_dotenv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter #might use this to make better use of og dict

load_dotenv()
Redd = os.getenv('REDDIT_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')
USER_AGENT = os.getenv('USER_AGENT')
#Go here to get OAUTH2 Tokens -> https://towardsdatascience.com/scraping-reddit-data-1c0af3040768

#access reddit API
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret= Redd, user_agent=USER_AGENT)

# !! CHANGE TO CONFIGURE SCRAPER
time_frame = 'month'       #Change time frame to pull if applicable
number_of_posts = 250     #Change number of posts to scrape
sub_to_scrape = 'Superstonk' #Change sub to scrape
sub_filter = 'top'  #Able to be changed between {top, hot, new, rising}



global top_title
global top_url
global post
# pull title and URL from reddit
posts =[]
def scraper(sub_filter):
    if sub_filter.lower() == 'top':
        for submission in reddit.subreddit(sub_to_scrape).top(time_frame, limit=number_of_posts):
            top_title = submission.title
            top_url = "https://www.reddit.com/"+ submission.permalink
            #appneds tuples to list
            posts.append((top_title, top_url))
    elif sub_filter.lower() == 'hot':
        for submission in reddit.subreddit(sub_to_scrape).hot(limit=number_of_posts):
            top_title = submission.title
            top_url = "https://www.reddit.com/"+ submission.permalink
            #appneds tuples to list
            posts.append((top_title, top_url))
    elif sub_filter.lower() == 'new':
        for submission in reddit.subreddit(sub_to_scrape).new(limit=number_of_posts):
            top_title = submission.title
            top_url = "https://www.reddit.com/"+ submission.permalink
            #appneds tuples to list
            posts.append((top_title, top_url))
    elif sub_filter.lower() == 'rising':
        for submission in reddit.subreddit(sub_to_scrape).rising(limit=number_of_posts):
            top_title = submission.title
            top_url = "https://www.reddit.com/"+ submission.permalink
            #appneds tuples to list
            posts.append((top_title, top_url))
    else:
        print('That option is not avalible yet')

scraper(sub_filter)

comment_username_flair_dict = {}
# a function that take in a Url from the post submissions and returns the comment author and flair
def comment_pull(post_url):
    submission = reddit.submission(url=post_url)
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        if comment.author in comment_username_flair_dict:
            continue
        else:
            comment_username_flair_dict[comment.author] = comment.author_flair_text

def scrape_posts(post_list):
    for index, post in enumerate(post_list):
        print('Scraping Post #'+str(index +1))
        try:
            comment_pull(post[1])
        except:
            print('url error at index:' + str(index))
        print('Complete.'+'\n')

def vote_counter():
    vote_count = 0
    for value in comment_username_flair_dict.values():
        if value == '🦍 Voted ✅':
            vote_count +=1
    return vote_count

def flair_counter():
    flair_dict = {}
    for flair in comment_username_flair_dict.values():
        
        if flair not in flair_dict.keys():
            
            flair_dict[flair] = 1
        elif flair in flair_dict.keys():
            flair_dict[flair] +=1
    return flair_dict



print('Comencing scrape of '+ str(sub_to_scrape)+ '...')

scrape_posts(posts)
number_of_unique_users_scraped = len(comment_username_flair_dict)

print('The number of users scraped: ' + str(number_of_unique_users_scraped))
#print('The number of users with 🦍 Voted ✅ flairs is:' + str(vote_counter())+'\n')



print(Counter(comment_username_flair_dict.values()).most_common(5))

'''
#draw pie chart of user flairs
pie_flair = comment_username_flair_dict
Counter()

labels, data = zip(*(Counter(pie_flair.values()).most_common(5)))
#  print(labels)

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%".format(pct, absolute)


wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"))

ax.legend(wedges, labels,
          title="Flair",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")

ax.set_title("Top 3 Flairs")
fig.tight_layout()
plt.show()
'''


