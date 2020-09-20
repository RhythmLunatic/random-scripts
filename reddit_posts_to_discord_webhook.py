#!/usr/bin/env python3
import requests
import json
import datetime
import sys
import os.path

"""
A cron script to check subreddits and check new posts.
Don't run it every minute, sometimes it takes longer than a minute to run the check so another process spawns, tries opening the file, then fails and overwrites it and then it reposts old links
Btw, my cronjob:
*/2  *  * * *   root    /root/.pyenv/shims/python3 /root/zivChecker/reddit_posts_to_discord_webhook.py > /tmp/out.txt

It's AGPLv3 becuase I said so, don't put this in your closed source discord bot.
Special thanks to https://discohook.org for the embed previewer

Copyright (C) 2020 Rhythm Lunatic

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
SUBREDDITS_TO_CHECK = ["dankmemes"]
#Increase or reduce this depending on how often the cronjob runs... Default is 24
NUM_POSTS_TO_CHECK = 10
WEBHOOK_URL = ""
PATH = "/root/zivChecker/"
#https://old.reddit.com/r/dankmemes/new/.json?count=24


#Returns number of new posts, number of removed posts.
def getNumNewPosts(oldJson, latestJson):
	for j in range(NUM_POSTS_TO_CHECK):
		oldLatestPost = oldJson['data']['children'][j]['data']['permalink']
		#if it reaches the end of the for loop then all posts are new
		#"What if there more than 24 posts an hour"? Idk maybe don't do that
		for i in range(NUM_POSTS_TO_CHECK):
			latestPost = latestJson['data']['children'][i]['data']['permalink']
			if latestPost == oldLatestPost:
				print("Matched post after "+str(i)+" iteration")
				return i,j
			else:
				print(latestPost + " != "+oldLatestPost)
		print("Couldn't find the last saved post, trying the next last saved post...")
	print("Failed to find any posts. Giving up and posting them all.")
	return NUM_POSTS_TO_CHECK,0

print(datetime.datetime.now())
for sub in SUBREDDITS_TO_CHECK:
	print("checking "+sub)
	r = requests.get("https://old.reddit.com/r/"+sub+"/new/.json?count="+str(NUM_POSTS_TO_CHECK), headers = {'User-agent': 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'})
	latestJson = json.loads(r.text)
	#print(latestJson)
	
	#Number of new posts since last check
	newPosts = NUM_POSTS_TO_CHECK
	numRemovedPosts = 0
	if os.path.exists(PATH+sub+".json"):
		with open(PATH+sub+".json","r") as f:
			oldJson = json.loads(f.read())
			newPosts,numRemovedPosts = getNumNewPosts(oldJson, latestJson)
				#if newPosts == NUM_POSTS_TO_CHECK:
				#	print("comparison failed! exiting...")
				#	sys.exit(0)
	else:
		print("File not found. If this is the first time checking the subreddit, ignore this message.")
		newPosts = 2
	with open(PATH+sub+".json","w") as f:
		f.write(r.text)
	print("Number of new posts: "+str(newPosts))
	for i in range(newPosts):
		post = latestJson['data']['children'][i]['data']
		description = post['link_flair_text']+"\n"+"[Discuss on Reddit](https://old.reddit.com"+post['permalink']+")"
		if i==0 and numRemovedPosts>1:
			description+="\nNote: The last post before this one was removed from this subreddit!"

		dataToSend = {
			"username":"/r/"+sub,
			"embeds": [{
				"title":post['title'],
				"description":description,
				"url":post['url']
			}]
		}
		if post['url'].endswith(('.jpg', '.jpeg', '.png', '.gif')):
			dataToSend['embeds'][0]["image"]= {
				"url":post['url']
			}
		elif post['thumbnail'] != 'default':
			dataToSend['embeds'][0]["image"]= {
				"url":post['thumbnail']
			}
		r = requests.post(
			WEBHOOK_URL,
			json = dataToSend
		)
