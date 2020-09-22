from mutagen.oggvorbis import OggVorbis
import glob
import os
import re
#from unidecode import unidecode

def remove_non_ascii(text):
    #return unidecode(text)
	return re.sub(r'[^\x00-\x7F]',' ', text).replace("?", "").replace("*", "").replace('"', "").replace("@", "A").replace(",","").replace("/","").replace(";"," ").replace("*"," ").replace(":","").replace(".","")
	
	
for fileName in glob.glob("*.ogg"):
	SongTitle = OggVorbis(fileName)['title'][0]
	#print(SongTitle)
	CleanTitle = remove_non_ascii(SongTitle)
	#print(CleanTitle)
	os.rename(fileName, CleanTitle+".ogg")