#!/usr/bin/env python3

from sys import argv,stdin
from utils import chunker


# @TODO: this will dehyphen incorrectly when line is split on, for example, "A-laget".
# @TODO: Guarantee that 
def dehyphenate(chunk):
    ret = []
    part_1 = None
    for line in chunk.split('\n'):
        if line.strip() == '':
            continue

        words = line.split()
       
        if part_1 != None:
            if words[0] in [ 'och', 'eller', 'och/eller' ]:
                words[0] = part_1 + ' ' + words[0]
            elif words[0][0].isupper() or words[0].replace(':', '').isnumeric():
                words[0] = part_1 + words[0]
            else:
                words[0] = part_1[:-1] + words[0]

            part_1 = None

        if words[-1][-1] == '-' and words[-1] != '-':
            part_1 = words[-1]
            words = words[:-1]

        ret += [ ' '.join(words) ]

    return '\n'.join(ret)


if __name__ == '__main__':
    for i,chunk in enumerate(chunker(stdin)):
        if i != 0:
            print()

        print(dehyphenate(chunk))

