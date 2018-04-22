# This Python code uses PRAW to search any one subreddit for keywords.
# https://praw.readthedocs.io/en/latest/
#
# The program loops through a list of search queries. 
# For each query, it searches for posts in the subreddit containing that key word.
# The posts can be no more than a week old (the max age of the post can be configured).
# When a post is found matching the criteria, it will PM the user, notifying and linking them to it.
#
# Note there is a better way to monitor subreddits than using this bot's method, 
# as discussed on the following thread.
# https://www.reddit.com/r/learnpython/comments/5c4jct/my_reddit_notification_bot/d9tz1q1/
# http://praw.readthedocs.io/en/latest/tutorials/reply_bot.html
#
# This bot is ment to catch posts of interests even when it is not running.
# It will only notify the user when it is running.

import praw
import config
import time
import os

receiver_username = config.receiver_username
searched_subreddit = config.searched_subreddit
subject_line = receiver_username + ', a post you may be interested in has appeared on ' + searched_subreddit
break_length = config.break_length
max_post_age = config.time_filter

# Add or remove search keywords from this list that you may want to be notified of.
query_list = config.query_list

# This list will contain all the posts that have already been sent to the user
# and will not be sent again.	
# The elements of this list come from saved_posts.txt.		  
posts_list = []			  

def bot_login():
	print('Logging in...')
	r = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = 'Send PM to Luke_Username when things are mentioned in r/whowouldwin')
	print('Logged in')
	return r
	
def run_bot(r):
	while True:
		for query in query_list:
			for post in r.subreddit(searched_subreddit).search(query, sort='new', syntax='lucene', time_filter=max_post_age):
				if post.shortlink not in posts_list:
					send_mesage(r, subject_line, post, query)
		print('Sleeping for ' + str(break_length) + ' seconds...')
		time.sleep(break_length)

def send_mesage(r, subject, post, query):
	message = subject + '\n\n' +'[' + post.title + ']' + '(' + post.shortlink + ')'
	r.redditor(receiver_username).message(subject, message)
	
	#To prevent messages from being sent multiple times.
	#A list called posts_list is made containing the shortlinks of the posts already captured.
	#When a message is sent, the list and saved_posts.txt file are both appended.
	posts_list.append(post.shortlink)
	
	#"a" is to append to "saved_posts.txt" as variable f
	with open("saved_posts.txt", "a") as f:
		f.write(post.shortlink + '\n')
		
	print('Sent message to ' + receiver_username + ' about ' + query)
	print()
	
def get_saved_posts():
	#Make sure the file exists.
	if not os.path.isfile("saved_posts.txt"):
		posts_list = []
	else:
		#"r" is to read from saved_posts.txt as the variable f
		with open("saved_posts.txt", "r") as f:
			posts_list = f.read()
			posts_list = posts_list.split("\n")
	return posts_list
			
r = bot_login()
posts_list = get_saved_posts()
run_bot(r)
