#!/usr/bin/env python3

from sys import argv,stdin,stderr,exit
from utils import chunker
from tqdm import tqdm
from collections import Counter
from re import split
from math import log2

if __name__ == '__main__':
    c = Counter()

    for line in stdin:
        if line.strip() == '':
            continue

        try:
            i,isbn,text = line.split('\t')
            words = split(r'[:,.!? \n]+', text)
            c.update([ 2**int(log2(len(words))) ])
        except Exception as e:
            print(f'warning: {str(e)}', file=stderr)
            print(line, file=stderr)

    for k in sorted(c):
        print(k,c[k])
