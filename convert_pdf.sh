#!/bin/bash

FILE=$1
TMPFILE=/tmp/$$.xml

if [ $# -ne 1 ] ; then
  echo "usage: $0 <pdf-file>" 1>&2
  exit 1
fi


pdf2txt.py -t xml -o $TMPFILE "$FILE"
python3 extract_text.py $TMPFILE | ./dehyphenate.py | ./txt_to_tsv.py

rm $TMPFILE
