#!/usr/bin/env python3

from sys import argv
from xml.etree import ElementTree as ET
from collections import Counter
from re import findall
from sklearn.cluster import KMeans
from hashlib import md5
from numpy import array
from kneed import KneeLocator
from math import sqrt

HEADER_PERCENT=10
FOOTER_PERCENT=10

n_pages = -1
max_static = 3
element_counts = Counter()


def is_header(page, box): 
    page_bbox = [ float(x) for x in page.attrib.get('bbox').split(',') ]
    bbox = [ float(x) for x in box.attrib.get('bbox').split(',') ]
    delta = [ bbox[2]-bbox[0], bbox[3]-bbox[1] ]
    center = [ bbox[0] + delta[0]/2, bbox[1] + delta[1]/2 ]

    #print('header', bbox, delta, center, center[1] / page_bbox[3], FOOTER_PERCENT/100, (center[1] / page_bbox[3]) > (1-FOOTER_PERCENT/100))

    # origo is left botttom corner
    if (center[1] / page_bbox[3]) > (1-HEADER_PERCENT/100):
        return True

    return False


def is_footer(page, box):
    page_bbox = [ float(x) for x in page.attrib.get('bbox').split(',') ]
    bbox = [ float(x) for x in box.attrib.get('bbox').split(',') ]
    delta = [ bbox[2]-bbox[0], bbox[3]-bbox[1] ]
    center = [ bbox[0] + delta[0]/2, bbox[1] + delta[1]/2 ]

    #print('footer', bbox, delta, center, center[1] / page_bbox[3], FOOTER_PERCENT/100, (center[1] / page_bbox[3]) < (FOOTER_PERCENT/100))

    # origo is left botttom corner
    if (center[1] / page_bbox[3]) < FOOTER_PERCENT/100:
        return True

    return False

def is_number(box):
    return get_boxtext(box).replace('.', '').isnumeric()


def in_cluster(box, cluster, font_size):
    c = get_center(box)

    return sqrt((c[0]-cluster[0])**2 + (c[1]-cluster[1])**2) < 2*font_size


def in_clusters(box, number_clusters, font_size):
    return any([ in_cluster(box, c, font_size) for c in number_clusters ])


def is_pagenumber(page, box, number_clusters, font_size):
    if is_number(box) and in_clusters(box, number_clusters, font_size):
        #print('page number', get_boxtext(box))

        return True

    return False


def is_static(page, box):
    key = ''.join(get_textlines(page, box)) + box.attrib.get('bbox')

    return elements_counts[key] > max_static


def in_bbox(center, bbox):
    return center[0] >= bbox[0] and center[1] >= bbox[1] and center[0] <= bbox[2] and center[1] <= bbox[3]


def get_bbox(element, clip=None):
    bbox = [ float(x) for x in element.attrib.get('bbox').split(',') ]

    if clip:
        bbox = [ max(bbox[0], clip[0]), max(bbox[1], clip[1]), min(bbox[2], clip[2]), min(bbox[3], clip[3]) ]

    return bbox


def get_center(element):
    bbox = get_bbox(element)
    delta = [ bbox[2]-bbox[0], bbox[3]-bbox[1] ]
    center = [ bbox[0] + delta[0]/2, bbox[1] + delta[1]/2 ]

    return center


def get_textlines(element):
    for line in element.findall('.//textline'):
        text = ' '.join(''.join([ x.text for x in line.findall('text') ]).strip().split())

        yield text


def get_isbn(root):
    max_page = 5
    pattern = r'((?:978-)?91-[0-9]+-[0-9]+-[0-9xX]|(?:978)?91[0-9]+[0-9]+[0-9xX])'

    for i,page in enumerate(root.findall('.//page')):
        if i + 1 > max_page:
            break

        for line in get_textlines(page):
            for isbn in findall(pattern, line):
                return isbn
        

def get_boxtext(box, fonts=None):
    ret = []
    size = float(fonts.most_common(1)[0][0][1]) if fonts else None

    for i,line in enumerate(box.findall('textline')):
        text = [ (x.text, j, float(x.attrib.get('size', '0.0'))) for j,x in enumerate(line.findall('text')) ]

        # include initial large character
        text = [ (x,s) for x,j,s in text if (s == size or size == None) or (i, j) == (0, 0) ]

        if len(text) > 0:
            if len(text) == 1 and text[0][1] != size and size != None:
                ...
            else:
                ret += [ ''.join([ x[0] for x in text ]).replace('\n', '').strip() ]
    
    return '\n'.join([ x for x in ret if x != '' ])


def get_number_boxes(root):
    for box in root.findall('.//textbox'):
        text = get_boxtext(box).replace('.', '')

        if text.isnumeric():
            yield box


def get_pagenumber_clusters(root):
    pagenumber_kmeans = KMeans(n_clusters=6, random_state=0)
    centers = []
    n_pages = len([ 1 for x in root.findall('.//page') ])

    for box in get_number_boxes(root):
        centers += [ get_center(box) ]

    if len(centers) > n_pages/2:
        centers = array([ [ float(x), float(y) ] for (x,y) in centers ])

        sse = []
        for n_clusters in range(1, min(len(centers), 8)):
            pagenumber_kmeans = KMeans(n_clusters=n_clusters, random_state=0)
            pagenumber_kmeans.fit(centers)
            sse.append(pagenumber_kmeans.inertia_)

        # find optimal number of clusters
        kl = KneeLocator(range(1, min(len(centers), 8)), sse, curve='convex', direction='decreasing')
        n_clusters = kl.elbow

        #print('clusters:', n_clusters)

        pagenumber_kmeans = KMeans(n_clusters=n_clusters,random_state=0)
        pagenumber_kmeans.fit(centers)

        return pagenumber_kmeans.cluster_centers_

    return []


def get_fonts(root):
    counts = Counter()
    
    # update font sized
    for text in root.findall('.//text'):
        counts.update([ (text.attrib.get("font"), text.attrib.get("size")) ])

    return counts


if __name__ == '__main__':
    root = ET.parse(argv[1])
    counts = get_fonts(root)
    pages = []
    isbn = get_isbn(root)
    number_clusters = get_pagenumber_clusters(root)
    size = float(counts.most_common(1)[0][0][1])

    #print(number_clusters)

    # create page number clusters

    print(f'## START ## ISBN {isbn}')

    if len(counts) != 0:
        eos = False

        for page in root.findall('.//page'):
            bottom = float(page.attrib['bbox'].split(',')[3])

            i=0
            for box in page.findall('textbox'):
                if not (is_header(page, box) or is_footer(page, box) or is_pagenumber(page, box, number_clusters, size)):
                    text = get_boxtext(box, counts)

                    if text.strip() != '':
                        top = float(box.attrib['bbox'].split(',')[3])
                        
                        #print(bottom-top, size, i, eos)
                        if (i != 0 and bottom-top > size or i == 0 and eos) and not top > bottom:
                            print('\n')

                        print(text)

                        bottom = float(box.attrib['bbox'].split(',')[1])
                        eos = text[-1] in [ '.', '!', '?' ] or bottom / float(page.attrib['bbox'].split(',')[3]) > 0.25
                        i += 1

