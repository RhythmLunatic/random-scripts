#!/bin/bash
#Script to make Weiss Schwarz cards using https://berander.deviantart.com/art/Weiss-Schwarz-MSE-Template-540676659

if [[ ("$1" == "") || ("$2" == "") || ("$3" == "") || ("$4" == "") || ("$5" == "")]]; then
    echo "Usage: cardMaker.sh image \"English name\" \"Japanese name\" \"quote\" output"
else
    
    convert "$1" -gravity Center -resize 448x626^ -crop 448x626+0+0 +repage \
    -draw "image over 0,0 0,0 'event/H - Schwarz Blue.png'" \
    -draw "image over 0,170 0,0 'flavorbar.png'" \
    -draw "image over 0,235 0,0 'bars/blue.png'" \
    -pointsize 18 -stroke '#000C' -strokewidth 2 -annotate +22+274 "$2" -stroke none -fill white -annotate +22+274 "$2" \
    -pointsize 16 -stroke none -fill black -annotate +0+172 "$4"\
    -font HeiseiMinStd-W7 -pointsize 13 -stroke none -fill black -annotate +0+235 "$3"\
    "$5"
fi

# Since I can't add comments when using backslash, here's what the commands do
# Line 1: Crop image and resize canvas to fit
# Line 2: Add the bottom bar where the english name goes
# Line 3: Add the top bar where the flavor text goes (Quotes from a character, usually)
# Line 4: Add the middle bar where the Japanese name goes
# Line 5: Add the english name, with text outlining
# Line 6: Add the quote in black text
# Line 7: Add the japanese name. This must be last since I have to choose a Japanese font for Japanese characters to show up.