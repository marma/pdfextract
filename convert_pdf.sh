#!/bin/bash

FILE=$1
TMPFILE=/tmp/$$.xml

pdf2txt -t xml -o $TMPFILE "$FILE"
python extract_text_2.py $TMPFILE

rm $TMPFILE
