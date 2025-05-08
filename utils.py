from re import split
from collections import Counter

common_words = [
    'i', 'och', 'att', 'det',
    'som', 'en', 'på', 'är',
    'av', 'för', 'med', 'till',
    'den', 'har', 'de', 'inte',
    'om', 'ett', 'han', 'men',
    'var', 'jag', 'sig', 'från',
    'vi', 'så', 'kan', 'man',
    'när', 'år', 'säger', 'hon',
    'under', 'också', 'efter', 'eller',
    'nu', 'sin', 'där', 'vid',
    'mot', 'ska', 'skulle', 'kommer',
    'ut', 'får', 'finns,' 'vara',
    'hade', 'alla', 'andra', 'mycket',
    'än', 'här', 'då', 'sedan',
    'över', 'bara', 'in', 'blir' ]


def is_text(s):
    s = [ x for x in split('[ ,\.!?;\']+', s.strip()) if x ]

    return sum([ value for key,value in Counter(s).items() if key in common_words ]) / max(len(s),1) > 0.1

def chunker(i):
    chunk = []
    for line in i:
        if line == '\n' and chunk != []:
            yield ''.join(chunk)
            chunk = []
        else:
            chunk += [ line ]

    if chunk != []:
        yield ''.join(chunk)

