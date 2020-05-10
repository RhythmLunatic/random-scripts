#!/usr/bin/env python3
import requests
import json
from bs4 import BeautifulSoup

"""
A script to check Zenius I Vanisher for new posts because the RSS support is somewhat lacking.
Drop this in /etc/cron.hourly and fill in the webhook url for Discord and configure the PATH.

- Rhythm Lunatic
"""

MAIN_URL = "https://zenius-i-vanisher.com/v5.2/"
WEBHOOK_URL = ""
#Use a hard path because it's a crontab
PATH = "/root/zivChecker/latestThread.json"

r = requests.get(MAIN_URL+"forum?forumid=19&page=1")
soup = BeautifulSoup(r.text, "lxml")

posts = soup.find('table').find_all('tr')
structuredPost = {}

#could be changed to "for post in posts:"
post = posts[1]
thread = post.find(class_="border").a
structuredPost['title'] = thread.text
lastReply = posts[1].find_all(class_='border')[-1].find_all('a')
structuredPost['url'] = MAIN_URL+lastReply[-1]['href']
structuredPost['lastReply'] = lastReply[0].text

print(structuredPost)

with open(PATH,"r") as f:
	text = json.loads(f.read())
	print(text)
	
if text != structuredPost:
	content = "New post by "+structuredPost['lastReply'] + " on thread \""+structuredPost['title'] +"\":"
	content+= "\n"+structuredPost['url']
	r = requests.post(
		WEBHOOK_URL,
		json={
			"content":content,
			"username":"Zenius -I- Vanisher",
			#"avatar_url":j['avatar_url'],
			#"embeds":[{
			#	"image":{
			#		"url":url
			#	}
			#}]
		}
	)
	
	with open(PATH, "wb") as f:
		text = json.dumps(structuredPost, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf8')
		f.write(text)
"""else:
	r = requests.post(
		WEBHOOK_URL,
		json={
			"content":"No new posts. (DEBUGGING!)",
			"username":"Zenius -I- Vanisher",
			#"avatar_url":j['avatar_url'],
			#"embeds":[{
			#	"image":{
			#		"url":url
			#	}
			#}]
		}
	)"""
