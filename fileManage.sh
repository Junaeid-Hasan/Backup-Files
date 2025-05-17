#!/bin/bash

BASE="/home/munna/Downloads"

if [ ! -d "$BASE" ]; then
    echo "Directory does not exist"
    exit 1
fi

# PDF directory creation
if [ ! -d "$BASE/PDFs" ]; then
    mkdir "$BASE/PDFs"
fi
# Images directory creation
if [ ! -d "$BASE/Images" ]; then
    mkdir "$BASE/Images"
fi
# Presentation directory Creation
if [ ! -d "$BASE/Presentation" ];then
	mkdir "$BASE/Presentation"
fi
#Videos directory Creation
if [ ! -d "$BASE/Videos" ];then
	mkdir "$BASE/Videos"
fi
#Application Directory Creation
if [ ! -d "$BASE/Apps" ];then
	mkdir "$BASE/Apps"
fi
# Sorting PDF files
find "$BASE" -type f \( -name '*.pdf' -o -name '*.odt' -o -name '*.docx' -o -name '*.doc'  \) -exec mv {} "$BASE/PDFs/" \;

# Sorting image files (jpg and png)
find "$BASE" -type f \( -name '*.jpg' -o -name '*.png' \) -exec mv {} "$BASE/Images" \;

#Sorting Presentation files
find "$BASE" -type f \( -name '*.pptx' -o -name '*.ppt'\) -exec mv {} "$BASE/Presentation/" \;

#Sorting Videos
find "$BASE" -type f \( -name '*.mkv' -o -name '*.mp4' \) -exec mv {} "$BASE/Videos/" \;

#Sorting Application files
find "$BASE" -type f \( -name '*.rpm' -o -name '*.zip' -o -name '*.bz2' -o -name '*.AppImage' \) -exec mv {} "$BASE/Apps/" \;

