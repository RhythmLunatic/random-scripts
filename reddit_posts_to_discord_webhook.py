import requests
import json

"""
A cron script to check subreddits and check new posts.
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
SUBREDDITS_TO_CHECK = ["dankmemes","memes"]
WEBHOOK_URL = ""
#https://old.reddit.com/r/dankmemes/new/.json?count=24

for sub in SUBREDDITS_TO_CHECK:
	print("checking "+sub)
	r = requests.get("https://old.reddit.com/r/"+sub+"/new/.json?count=24", headers = {'User-agent': 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'})
	latestJson = json.loads(r.text)
	#print(latestJson)
	latestPost = latestJson['data']['children'][0]['data']['permalink']
	
	#Number of new posts since last check
	newPosts = 24
	try:
		with open(sub+".json","r") as f:
			oldJson = json.loads(f.read())
			#if it reaches the end of the for loop then all posts are new
			#"What if there more than 24 posts an hour"? Idk maybe don't do that
			for i in range(newPosts):
				if latestPost == oldJson['data']['children'][i]['data']['permalink']:
					newPosts = i
					break
	except:
		print("File not found, creating a new one.")
		with open(sub+".json","w") as f:
			f.write(r.text)
	print("Number of new posts: "+str(newPosts))
	for i in range(newPosts):
		post = latestJson['data']['children'][i]['data']
		dataToSend = {
			"username":"/r/"+sub,
			"embeds": [{
				"title":post['title'],
				"description":post['link_flair_text'],
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