"""
Convert a .sm file to .tja.
How to write your .sm:
A note on any of the inner two lanes is a don (0010 or 0100)
A note on any of the outer two lanes is a kat (1000 or 0001)
One hold note on any lane is a roll note (2000, 0200, 0020, 0002)
Two notes on the inner lanes is a big don (0110)
Two notes on the outer lanes is a big kat (1001)
Two holds on the inner lanes or outer lanes is a big roll (2002 or 0220)
Anything else will be ignored and turned into an empty space.
"""

import sys
import random
import os

with open("255.sm") as file_read:
	content = file_read.readlines()					
	insideNotesBlock = False
	
	for line in content:
		if (line == "#NOTES:\n"): #Start of #NOTES block
			insideNotesBlock = True
			print("#START")
		elif (line == ";\n"): #End of #NOTES block
			insideNotesBlock = False
			print("\n#END")
			
		if (insideNotesBlock):
			#Found a beat line
			if line[0].isdigit():
				#don
				if (line[1] == "1" and line[2] == "0") or (line[1] == "0" and line[2] == "1"):
					print("1", end="")
				#kat
				elif (line[0] == "1" and line[3] == "0") or (line[0] == "0" and line[3] == "1"):
					print("2", end="")
				#large don
				elif line[1] == "1" and line[2] == "1":
					print("3", end="")
				#large kat
				elif line[0] == "1" and line[3] == "1":
					print("4", end="")
				#large drumroll
				elif (line[1] == "2" and line[2] == "2") or (line[0] == "2" and line[3] == "2"):
					print("6", end="")
				#drumroll
				elif "2" in line:
					print("5", end="")
				#end of drumroll
				elif "3" in line:
					print("8", end="")
				else:
					print("0", end="")
			elif line == ",\n":
				#Finding a comma means end of current measure
				print(",");
			else:
				print("Error: "+line.strip()+" is not a valid chart character")
				
		else:
			#Line not within the #NOTES block, write the unmodified line to file
			print(line)