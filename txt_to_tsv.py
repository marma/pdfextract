#!/usr/bin/env python3

from sys import argv,stdin
from utils import chunker,is_text
from re import search
from uuid import uuid4

if __name__ == '__main__':
    i = uuid4().hex

    for line in stdin:
        if line.startswith('## START'):
            isbn = search('([0-9Xx-]+)', line)
            
            if not isbn or isbn.group(1) == 'None':
                isbn = 'None'
            else:
                isbn = isbn.group(1)

            for chunk in chunker(stdin):
                if is_text(chunk) and chunk.count('.') > 5:
                    #print(isbn, chunk.strip().replace('\n', '\\n'), sep='\t')
                    print(i, isbn, chunk.strip().replace('\n', '\\n'), sep='\t')
