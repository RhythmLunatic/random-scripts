#!/bin/bash
#Do not use this, it's old, it takes ages to run.

#Get width & height
OUTPUT=$(convert $1 -print "%wx%h\n" /dev/null)
#split into two variables (the character after IFS= is the char that it splits at)
IFS=x read width height <<< $OUTPUT
#Because seq ends at the number instead of stopping before it, subtract 1
width=`expr $width - 1`
height=`expr $height - 1`
#Do our amazing loop
for i in `seq 0 $height`;
do
	for j in `seq 0 $width`;
	do
    	#echo -n "$j x $i | "
    	#Oh god why
    	OUTPUT=$(convert $1 -crop "1x1+$j+$i" txt:- | awk 'END {print $NF}')
    	[ "$OUTPUT" == "white" ] || ( echo -n 0 && false ) && echo -n "1"
    	#echo ""
    done
done
echo ""
