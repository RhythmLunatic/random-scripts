"""
Convert SM or SSC to MUSYNC PSM
BPM changes not supported, fairly untested, attempt at your own peril.
"""
import sys
with open("Ancient Scapes.ssc") as file_read:
	content = file_read.readlines()					
	insideNotesBlock = False
	offset = 0.000
	bpm = 0.000
	spacing = 0.000
	#measures = 0
	noteChart = []
	tempNotes = []
	for line in content:
		if (line == "#NOTES:\n"): #Start of #NOTES block
			insideNotesBlock = True
			#print("#START")
		elif line[0] == "#":
			tag, param = line.split(":")
			param = param[:-2] #We're stripping the \n and the ;
			if tag == "#TITLE":
				print("TITLE:"+param)
			elif tag == "#SUBTITLE":
				print("SUBTITLE:"+param)
			elif tag == "#OFFSET":
				print("Start of song: 5000000")
				offset = float(param)*-1 + .5
				print("global offset (incl. start of song): "+str(offset))
			elif tag == "#BPMS":
				bpm = float(param.split("=")[1])
				spacing = 60/bpm*4
				print("BPM:",bpm)
				print("Spacing:",spacing)
			
		if (insideNotesBlock):
			if line[0].isdigit():
				tempNotes.append(line.strip())
			elif line[0] == ",":
				noteChart.append(list(tempNotes))
				tempNotes = []
				#measures+=1
			elif (line == ";\n"): #End of #NOTES block
				insideNotesBlock = False
				#print("Measures: "+str(len(noteChart)))
				#print(noteChart[0])
				for i in range(len(noteChart)):
				#for i in range(2):
					measureLength = len(noteChart[i])
					#print("Length of measure: "+str(measureLength))
					for j in range(measureLength):
						#print(str(i+1) + " " + str(j)+"/"+str(measureLength-1) + " ", end="")
						#print(noteChart[i][j], end="")
						notePosition = int((spacing/measureLength*j + i*spacing + offset)*10000000)
						#print(" "+str(notePosition))
						for k in range(4):
							if noteChart[i][j][k] == "1":
								#musync uses tracks 1,2,6,7, probably because it's BMS?
								if k == 0:
									t = "1"
								elif k == 1:
									t = "2"
								elif k == 2:
									t = "6"
								elif k == 3:
									t = "7"
								print("<Note insertTime=\""+str(notePosition)+"\" track=\"" + t + "\" wavId=\"02\" />")
				sys.exit(0)