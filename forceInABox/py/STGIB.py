# -*- coding: utf-8 -*-

import squarify
import json
from operator import itemgetter
import os

def ST(data, groups, path, dir, file, width, height, use):
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
        dic['name'] = i
        groupSize.append(dic)
    groupSize.sort(key=itemgetter('size'), reverse = True )

    index = []
    values = []
    for i in groupSize:
        values.append(i['size'])
        index.append(i['name'])

    # the sum of the values must equal the total area to be laid out
    # i.e., sum(values) == width * height
    values = squarify.normalize_sizes(values, width, height)

    # returns a list of rectangles
    rects = squarify.squarify(values, x, y, width, height)
    # padded rectangles will probably visualize better for certain cases
    # padded_rects = squarify.padded_squarify(values, x, y, width, height)
    # print(padded_rects)
    for i in range(length):
        rects[i]['name'] = index[i]

    rects.sort(key=itemgetter('name'))
    # for i in range(length):
    #     del rects[i]['index']

    dic = {}
    dic['x'] = 0
    dic['y'] = 0
    dic['dx'] = width
    dic['dy'] = height
    rects.append(dic)

    links = data['links']
    nodes = data['nodes']

    forWrite = {}
    forWrite['nodes'] = nodes
    forWrite['links'] = links
    forWrite['groups'] = rects
    forWrite['groupSize'] = data['groupSize']
    forWrite['pgroup'] = data['pgroup']
    forWrite['pout'] = data['pout']
    forWrite['mostConnected'] = data['mostConnected']
    forWrite['nodeSize']= data['nodeSize']
    forWrite['linkSize'] = data['linkSize']
    forWrite['nodeMax']= data['nodeMax']
    forWrite['nodeMin'] = data['nodeMin']
    forWrite['linkMax'] = data['linkMax']
    forWrite['linkMin'] = data['linkMin']

    try:
        # verify = os.listdir('../data/' + use  + '/temp/' + dir)
        verify = os.listdir('../data/' + use  + '/temp/')
    except:
        # os.mkdir('../data/' + use  + '/temp/' + dir)
        os.mkdir('../data/' + use  + '/temp/')
    # f = open('../data/' + use  + '/temp/' + dir + '/' + file, 'w')
    print('../data/' + use  + '/temp/' + file)
    f = open('../data/' + use  + '/temp/' + file, 'w')
    json.dump(forWrite, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

if __name__ == '__main__':
    main = '../data/origin/STGIB/'
    width = 960
    height = 600
    num = 0
    dir = False
    for file in os.listdir(main):
        if file != '.DS_Store':
            # try:
            # for file in os.listdir(main + dir):
                # print(file)
                # dir = "18-0.0005-0.05"
            # if (dir != '.DS_Store'):
            num += 1
            # path = main + dir + '/' + file
            path = main + file
            width = 960
            height = 600
            reader = open(path, 'r')
            data = json.load(reader)
            nodes = data['nodes']
            length = len(nodes)
            maxGroup = 0
            # get length of group
            for i in range(length):
                current = nodes[i]['group']
                if current > maxGroup:
                    maxGroup = current
            groups = [ [] for i in range(maxGroup+1)]
            # make list 'groups' a list have nodes' index
            for i in range(length):
                dic = {}
                dic['number'] = i
                groups[nodes[i]['group']].append(dic)

            use = 'STGIB'
            ST(data, groups, path, dir, file, width, height, use)
