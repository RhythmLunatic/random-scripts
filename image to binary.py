import sys
from PIL import Image

#This decodes an image of pure white and black squares into binary (or text if you use -text)
#Trying to decode monika.chr from Doki Doki Literature Club? Use this!

def decode_binary_string(s):
	return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

if len(sys.argv) == 1:
	print("Usage: pass in an image as the first argument, or use the -text flag to decode binary to text and pass in an image as the second argument.")
	sys.exit(0)

if sys.argv[1] == "-text":
	decode = True
	imgName = sys.argv[2]
else:
	imgName = sys.argv[1]

im = Image.open(imgName, 'r')
width, height = im.size
pixel_values = list(im.getdata())

if decode:
	bstr = ""
	for pixel in pixel_values:
		bstr += str(pixel)
	print(decode_binary_string(bstr))
else:
	for pixel in pixel_values:
		print(pixel, end='')
	print('') #Print newline at end
