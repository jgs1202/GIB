# -*- coding: utf-8 -*-

import squarify
import json
from operator import itemgetter
import os

def ST(mostConnect, data, groups, path, dir, file, width, height):
    # these values define the coordinate system for the returned rectangles
    # the values will range from x to x + width and y to y + height
    x = 0.
    y = 0.
    total = 0
    groupSize = []
    length = len(groups)
    for i in range(length):
        total += len(groups[i])
    for i in range(length):
        dic = {}
        dic['size'] = (len(groups[i])/total)
        dic['index'] = i
        groupSize.append(dic)
    groupSize.sort(key=itemgetter('size'), reverse = True )

    index = []
    values = []
    for i in groupSize:
        values.append(i['size'])
        index.append(i['index'])

    # the sum of the values must equal the total area to be laid out
    # i.e., sum(values) == width * height
    values = squarify.normalize_sizes(values, width, height)

    # returns a list of rectangles
    rects = squarify.squarify(values, x, y, width, height)

    # padded rectangles will probably visualize better for certain cases
    # padded_rects = squarify.padded_squarify(values, x, y, width, height)
    # print(padded_rects)
    for i in range(length):
        rects[i]['index'] = index[i]
    rects.sort(key=itemgetter('index'), reverse = True )
    for i in range(length):
        del rects[i]['index']

    links = data['links']
    nodes = data['nodes']

    forWrite = {}
    forWrite['nodes'] = nodes
    forWrite['links'] = links
    forWrite['groups'] = rects

    try:
        verify = os.listdir('../data/Chaturvedi/temp/' + dir)
    except:
        os.mkdir('../data/Chaturvedi/temp/' + dir)
    f = open('../data/Chaturvedi/temp/' + dir + '/' + file, 'w')
    json.dump(forWrite, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
