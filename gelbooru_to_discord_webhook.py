#!/usr/bin/env python3
import requests
import json
import datetime
import sys
import os.path
#import xml.etree.ElementTree as ET
import urllib.parse
#from xml.dom import minidom
import html

"""
A cron script to check gelbooru and check new posts.
Don't run it every minute, sometimes it takes longer than a minute to run the check so another process spawns, tries opening the file, then fails and overwrites it and then it reposts old links
Btw, my cronjob:
*/2  *  * * *   root    /root/.pyenv/shims/python3 /root/zivChecker/gelbooru_to_discord_webhook.py > /tmp/out.txt

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
TAGS_TO_CHECK = ["fischl_(genshin_impact) rating:safe", "girls_frontline rating:safe highres"]
#Increase or reduce this depending on how often the cronjob runs... Default is 24
NUM_POSTS_TO_CHECK = 5
WEBHOOK_URL = ""
#PATH = "./"
PATH = "/root/zivChecker/"

#For safe file names
def slugify(value):
	return "".join([x if x.isalnum() else "_" for x in value])

#Returns number of new posts, number of removed posts.
def getNumNewPosts(oldJson, latestJson):
	for j in range(NUM_POSTS_TO_CHECK):
		oldLatestPost = oldJson[j]
		#if it reaches the end of the for loop then all posts are new
		#"What if there more than 24 posts an hour"? Idk maybe don't do that
		for i in range(NUM_POSTS_TO_CHECK):
			latestPost = latestJson[i]
			if latestPost == oldLatestPost:
				print("Matched post after "+str(i)+" iteration")
				return i,j
			else:
				print(latestPost['file_url'] + " != "+oldLatestPost['file_url'])
		print("Couldn't find the last saved post, trying the next last saved post...")
	print("Failed to find any posts. Giving up and posting them all.")
	return NUM_POSTS_TO_CHECK,0

print(datetime.datetime.now())
for tag in TAGS_TO_CHECK:
	print("checking "+tag)
	#r = requests.get("https://old.reddit.com/r/"+sub+"/new/.json?count="+str(NUM_POSTS_TO_CHECK), headers = {'User-agent': 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'})
	r = requests.get("https://gelbooru.com/index.php?page=dapi&json=1&s=post&q=index&limit="+str(NUM_POSTS_TO_CHECK)+"&tags="+tag.replace(' ','+'))
	print("Got JSON from server.")
	latestJson = json.loads(r.text)
	#print(latestJson)
	
	#Number of new posts since last check
	newPosts = NUM_POSTS_TO_CHECK
	numRemovedPosts = 0
	fileName = PATH+slugify(tag)+".json"
	if os.path.exists(fileName):
		with open(fileName,"r") as f:
			oldJson = json.loads(f.read())
			newPosts,numRemovedPosts = getNumNewPosts(oldJson, latestJson)
		
		#with open(PATH+sub+".xml","r") as f:
				#if newPosts == NUM_POSTS_TO_CHECK:
				#	print("comparison failed! exiting...")
				#	sys.exit(0)
	else:
		print("File not found. If this is the first time checking the tag, ignore this message.")
		newPosts = 2
	with open(fileName,"w") as f:
		f.write(r.text)
	print("Number of new posts: "+str(newPosts))
	for i in range(newPosts):
		post = latestJson[i]
		
		description="\n[Source]("+html.unescape(post['source'])+")"
		#description = post['tags']
		if i==0 and numRemovedPosts>1:
			description+="\nNote: The last post before this one was removed from this subreddit!"

		dataToSend = {
			"username":tag,
			"embeds": [{
				"title":tag,
				"description":description,
				"url":"https://gelbooru.com/index.php?page=post&s=view&id="+str(post['id'])
			}]
		}
		if post['file_url'].endswith(('.jpg', '.jpeg', '.png', '.gif')):
			dataToSend['embeds'][0]["image"]= {
				"url":post['file_url']
			}
		else:
			dataToSend['embeds'][0]["image"]= {
				"url":post['preview_url']
			}
		r = requests.post(
			WEBHOOK_URL,
			json = dataToSend
		)
