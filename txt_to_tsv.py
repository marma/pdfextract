#!/usr/bin/env python3

from sys import argv,stdin
from utils import chunker,is_text
from re import search

if __name__ == '__main__':
    #i = argv[1]

    for line in stdin:
        #print('id', 'isbn', 'text', sep='\t')

        if line.startswith('## START'):
            isbn = search('([0-9Xx-]+)', line)

            if not isbn or isbn.group(1) == 'None':
                continue
            else:
                isbn = isbn.group(1)

                for chunk in chunker(stdin):
                    if is_text(chunk) and chunk.count('.') > 5:
                        print(isbn, chunk.strip().replace('\n', '\\n'), sep='\t')
                        #print(i, isbn, chunk.strip().replace('\n', '\\n'), sep='\t')
