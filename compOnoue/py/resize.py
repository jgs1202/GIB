# -*- coding: utf-8 -*-

import os
import copy
import json
import math
import numpy as np
import matplotlib.pyplot as plt
import sys

def resize(path, num, main):
    margin = 20
    reader = open(path, 'r')
    data = json.load(reader)
    old = (data['groupSize'])

    # import pylab as pl
    # pl.xticks([0, width])
    # pl.yticks([0, height])
    # for i in data['groups']:
    #     # if i[2] == 15:
    #     pl.gca().add_patch( pl.Rectangle(xy=[i['x'], height - i['y']], width=i['dx'], height=i['dy'], linewidth='1.0', fill=False) )
    # pl.show()

    del data['groups'][-1]

    first = 0
    for i in data['groups']:
        if first == 0:
            first += 1
            xmin = i['x']
            xmax = xmin + i['dx']
            ymin = i['y']
            ymax = ymin + i['dy']
        else:
            if i['x'] < xmin and i['x']:
                xmin = i['x']
            elif i['x'] + i['dx'] > xmax:
                xmax = i['x'] + i['dx']
            if i['y'] < ymin:
                ymin = i['y']
            elif i['y'] + i['dy'] > ymax:
                ymax = i['y'] + i['dy']

    reWidth = xmax - xmin
    reHeight = ymax - ymin
    reAspect = reWidth / reHeight
    trueAspact = outWidth / outHeight
    if reAspect > trueAspact:
        which = 'x'
    else :
        which = 'y'
    # print(xmin, xmax, ymin, ymax, reWidth, reHeight)
    if which == 'x':
        # print('width')
        span = (reWidth * outHeight / outWidth - reHeight)/2
        ymin -= span
        ymax += span
        reHeight = reWidth * height / width
        ratio = (outHeight) / reHeight
    if which == 'y':
        # print('height')
        span = (reHeight * outWidth / outHeight - reWidth)/2
        xmin -= span
        xmax += span
        reWidth = reHeight * width / height
        ratio = outHeight / reHeight

    # print(xmin, xmax, ymin, ymax, reWidth, reHeight)

    if which == 'x':
        for i in  range(len(data['groups'])):
            data['groups'][i]['x'] = (data['groups'][i]['x'] - xmin) * ratio
            data['groups'][i]['y'] = (data['groups'][i]['y'] - ymin - span) * ratio
            data['groups'][i]['dx'] *= ratio
            data['groups'][i]['dy'] *= ratio
            # data['groups'][i]['x'] = (data['groups'][i]['x'] - xmin - span)
            # data['groups'][i]['y'] = (data['groups'][i]['y'] - ymin)
    if which == 'y':
        for i in  range(len(data['groups'])):
            data['groups'][i]['x'] = (data['groups'][i]['x'] - xmin - span) * ratio
            data['groups'][i]['y'] = (data['groups'][i]['y'] - ymin) * ratio
            data['groups'][i]['dx'] *= ratio
            data['groups'][i]['dy'] *= ratio
    # print(ratio)


    for i in range(len(data['groups'])):
        if which == 'x':
            data['groups'][i]['x'] += margin
            data['groups'][i]['y'] += margin + span * ratio
        if which == 'y':
            data['groups'][i]['x'] += margin + span*ratio
            data['groups'][i]['y'] += margin

    # print(span, (outWidth - reWidth)/2)
    # print(reWidth, reHeight)

    first = 0
    for i in data['groups']:
        if first == 0:
            first += 1
            xmin = i['x']
            xmax = xmin + i['dx']
            ymin = i['y']
            ymax = ymin + i['dy']
        else:
            if i['x'] < xmin and i['x']:
                xmin = i['x']
            elif i['x'] + i['dx'] > xmax:
                xmax = i['x'] + i['dx']
            if i['y'] < ymin:
                ymin = i['y']
            elif i['y'] + i['dy'] > ymax:
                ymax = i['y'] + i['dy']
    # print(data['groups'])
    dic = {}
    dic['x'] = 0
    dic['y'] = 0
    dic['dx'] = outWidth + margin*2
    dic['dy'] = outHeight + margin*2
    data['groups'].append(dic)
    for i in range(len(data['nodes'])):
        data['nodes'][i]['x'] += margin
        data['nodes'][i]['y'] += margin

    sizes.append(data['groupSize'])
    #
    # import pylab as pl
    # pl.xticks([0, outWidth + margin*2])
    # pl.yticks([0, outHeight + margin *2])
    # for i in data['groups']:
    #     pl.gca().add_patch( pl.Rectangle(xy=[i['x'], outHeight + margin*2 - i['y'] - i['dy']], width=i['dx'], height=i['dy'], linewidth='1.0', fill=False))
    # pl.show()
    #
    print(data['file'])
    f = open( '../data/FDGIB/temp/' + data['file'], 'w')
    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    # sys.exit()


def main():
    main = '../data/FDGIB/temp/'
    global sizes
    sizes = []
    # for dir in os.listdir(main):
    #     if (dir != '.DS_Store'):
    num = 0
    for file in os.listdir(main):
        if file[-5:] == '.json':
            print(file)
            path = main + file
            # print(path)
            resize(path, num, main)
            num += 1
    print(sizes.count(8), sizes.count(17))

if __name__ == '__main__':
    global width
    global height
    global outWidth
    global outHeight
    width = 1620.7
    height = 1000
    outWidth = 920
    outHeight = 560
    main()
