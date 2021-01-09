#!/usr/bin/env python3
import requests
#import json
import datetime
import sys
import os.path
import xml.etree.ElementTree as ET
import urllib.parse
from xml.dom import minidom
import html
from html.parser import HTMLParser
from bs4 import BeautifulSoup

"""
A cron script to check RSS feeds and check new posts.
Don't run it every minute, sometimes it takes longer than a minute to run the check so another process spawns, tries opening the file, then fails and overwrites it and then it reposts old links
Btw, my cronjob:
*/2  *  * * *   root    /root/.pyenv/shims/python3 /root/zivChecker/rss_discord_webhook.py > /tmp/out.txt

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

WEBSITES_TO_CHECK = []
#Increase or reduce this depending on how often the cronjob runs... Default is 24
NUM_POSTS_TO_CHECK = 10
WEBHOOK_URL = ""
PATH = "./"
#PATH = "/root/zivChecker/"

#For safe file names
def slugify(value):
	return "".join([x if x.isalnum() else "_" for x in value])


#Remove HTML tags in text
class HTMLFilter(HTMLParser):
	text = ""
	def handle_data(self, data):
		self.text += data

#Returns number of new posts, number of removed posts.
def getNumNewPosts(oldXml, latestXml):
	for j in range(NUM_POSTS_TO_CHECK):
		oldLatestPost = oldXml[j]
		#if it reaches the end of the for loop then all posts are new
		#"What if there more than 24 posts an hour"? Idk maybe don't do that
		for i in range(NUM_POSTS_TO_CHECK):
			latestPost = latestXml[i]
			if latestPost.find('link').text == oldLatestPost.find('link').text:
				print("Matched post after "+str(i)+" iteration")
				return i,j
			else:
				print(latestPost['file_url'] + " != "+oldLatestPost['file_url'])
		print("Couldn't find the last saved post, trying the next last saved post...")
	print("Failed to find any posts. Giving up and posting them all.")
	return NUM_POSTS_TO_CHECK,0

print(datetime.datetime.now())
for site in WEBSITES_TO_CHECK:
	print("checking "+site)
	#r = requests.get("https://old.reddit.com/r/"+sub+"/new/.json?count="+str(NUM_POSTS_TO_CHECK), headers = {'User-agent': 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'})
	r = requests.get(site)
	print("Got XML from server.")
	latestXml = ET.fromstring(r.text)
	#print(latestXml)
	latestXml = latestXml.find('channel').findall('item')
	#print(latestJson)
	
	#Number of new posts since last check
	newPosts = NUM_POSTS_TO_CHECK
	numRemovedPosts = 0
	fileName = PATH+slugify(site)+".xml"
	if os.path.exists(fileName):
		oldXml = ET.parse(fileName).getroot().find('channel').findall('item')
		newPosts,numRemovedPosts = getNumNewPosts(oldXml, latestXml)
	else:
		print("File not found. If this is the first time checking the tag, ignore this message.")
		newPosts = 2
	with open(fileName,"w") as f:
		f.write(r.text)
	print("Number of new posts: "+str(newPosts))
	for i in range(newPosts):
		post = latestXml[i]
		print(post.find('title').text)
		
		content = post.find("{http://purl.org/rss/1.0/modules/content/}encoded")
		soup = None
		if content != None:
			soup = BeautifulSoup(content.text)
		
		description = "No description."
		if post.find('description') != None:
			print("desc found.")
			f = HTMLFilter()
			f.feed(post.find('description').text)
			description = f.text.strip()
			print(description)
		elif content:
			description = soup.get_text()
		
		dataToSend = {
			"username":"RSS Webhook",
			"embeds": [{
				"title":post.find('title').text,
				"description":description,
				"url":post.find('link').text
			}]
		}
		
		if soup != None:
			img = soup.find('img')
			if img:
				dataToSend['embeds'][0]["image"]= {
					"url":img['src']
				}
			"""if post['file_url'].endswith(('.jpg', '.jpeg', '.png', '.gif')):
				dataToSend['embeds'][0]["image"]= {
					"url":post['file_url']
				}
			else:
				dataToSend['embeds'][0]["image"]= {
					"url":post['preview_url']
				}"""
		r = requests.post(
			WEBHOOK_URL,
			json = dataToSend
		)
