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
number_of_posts = 100     #Change number of posts to scrape
sub_to_scrape = 'MurderedByAOC' #Change sub to scrape
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

comment_username_dict = {}
# a function that take in a Url from the post submissions and returns the comment author and flair
def comment_pull(post_url):
    submission = reddit.submission(url=post_url)
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue
        #if comment.body in comment_username_dict:
            continue
        else:
            comment_username_dict[comment.author] = comment.body

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
    for value in comment_username_dict.values():
        if value == '🦍 Voted ✅':
            vote_count +=1
    return vote_count

def flair_counter():
    flair_dict = {}
    for flair in comment_username_dict.values():
        
        if flair not in flair_dict.keys():
            
            flair_dict[flair] = 1
        elif flair in flair_dict.keys():
            flair_dict[flair] +=1
    return flair_dict



print('Comencing scrape of '+ str(sub_to_scrape)+ '...')

scrape_posts(posts)
number_of_unique_users_scraped = len(comment_username_dict)

print('The number of users scraped: ' + str(number_of_unique_users_scraped))
comment_list = [comment for comment in comment_username_dict.values()]
print(Counter(comment_list).most_common(10))





