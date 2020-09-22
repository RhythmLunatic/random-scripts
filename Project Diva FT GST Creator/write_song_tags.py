from mutagen.oggvorbis import OggVorbis
import glob
import os
import re

content = []
f = open("pv_db.txt", mode="r", encoding="utf-8")
for line in f.readlines():
	if line[:2] != "pv":
		continue
	else:
		content.append(line[3:].strip())
f.close()
songCount = 1000
l = [{
	'song_file_name':None,
	'song_name':None,
	'artist':None,
	'composer':None
	} for x in range(songCount)]
	
for line in content:
	#print(line)
	index,keyVal = line.split(".",1)
	index = int(index)
	key,value = keyVal.split("=",1)
	#print(key,"=",value)
	if key == "song_file_name":
		l[index]['song_file_name'] = value.split("/")[-1]
	elif key == "songinfo_en.arranger":
		l[index]['artist'] = value
	elif key == "songinfo_en.music":
		l[index]['composer'] = value
	elif key == "song_name_en":
		l[index]['song_name'] = value

#sortedList = sorted(l, key=lambda k: int(k['id']))

"""for i in range(songCount):
	if l[i]['song_name'] == None:
		continue
	print("ID"+str(i)+": "+ l[i]['song_name'])"""
#print(sortedList)

#filter(fulfills_some_condition, lst)
for fileName in glob.glob("*.ogg"):
	songID = int(re.search(r'\d+', fileName).group())
	file = OggVorbis(fileName)
	if l[songID]['song_name'] == None:
		print("No song found for ID ",str(songID),"!")
		continue
	print("ID"+str(songID)+": "+ l[songID]['song_name'])
	if fileName.split(".")[0].endswith("miku"):
		file["title"] = l[songID]["song_name"] + " (Miku ver.)"
	elif fileName.split(".")[0].endswith("kaito"):
		file["title"] = l[songID]["song_name"] + " (Kaito ver.)"
	elif fileName.split(".")[0].endswith("len"):
		file["title"] = l[songID]["song_name"] + " (Len ver.)"
	elif fileName.split(".")[0].endswith("rin"):
		file["title"] = l[songID]["song_name"] + " (Rin ver.)"
	elif fileName.split(".")[0].endswith("luka"):
		file["title"] = l[songID]["song_name"] + " (Luka ver.)"
	elif fileName.split(".")[0].endswith("meiko"):
		file["title"] = l[songID]["song_name"] + " (Meiko ver.)"
	elif fileName.split(".")[0].endswith("all"):
		file["title"] = l[songID]["song_name"] + " (All VOCALOIDs ver.)"
	else:
		file["title"] = l[songID]["song_name"]
	file["artist"] = l[songID]["artist"]
	file["composer"] = l[songID]["composer"]
	
	file.save()