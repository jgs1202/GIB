# -*- coding: utf-8 -*-

# size is 900*600

import json
from operator import itemgetter
import math
import csv
import copy
import sys

def edgeCross(data):

    nodes = data['nodes']
    links = data['links']

    length = len(links)
    total = 0

    for i in range(length):
        sx1 = nodes[ links[i]['source']['index'] ]['x']
        sy1 = nodes[ links[i]['source']['index'] ]['y']
        tx1 = nodes[ links[i]['target']['index'] ]['x']
        ty1 = nodes[ links[i]['target']['index'] ]['y']
        index1 = links[i]['source']['index']
        index2 = links[i]['target']['index']
        # print('i = ' + str(i))

        for j in range (length - i - 1):
            sx2 = nodes[ links[i+j+1]['source']['index'] ]['x']
            sy2 = nodes[ links[i+j+1]['source']['index'] ]['y']
            tx2 = nodes[ links[i+j+1]['target']['index'] ]['x']
            ty2 = nodes[ links[i+j+1]['target']['index'] ]['y']
            index3 = links[i+j+1]['source']['index']
            index4 = links[i+j+1]['target']['index']

            try:
                # if an either of thw two links is vertical, we do not count
                if tx1 == sx1 and tx2 != sx2:
                    x = tx1
                    y = (ty2 - sy2)/(tx2- sx2) * (x - sx2) + sy2
                elif tx1 != sx1 and tx2 == sx2:
                    x = tx2
                    y = (ty1 - sy1)/(tx1- sx1) * (x - sx1) + sy1
                else:
                    tan1 = (ty1 - sy1)/(tx1- sx1)
                    tan2 = (ty2 - sy2)/(tx2- sx2)
                    # tan1 * x - tan1 * sx1 + sy1 = tan2 * x - tan2 * sx2 + sy2
                    x = ( sy2 - sy1 + tan1 * sx1 - tan2* sx2) / (tan1 - tan2)
                    y = tan1 * (x - sx1) + sy1
                # if intersection point is same as either of source or target we do not count
                if [x,y] == [sx1, sy1] or [x,y] == [sx2, sy2] or [x,y] == [tx1, ty1] or [x,y] == [tx2, ty2]:
                    pass
                else :
                    if (sx1 - x)*(tx1 - x) <= 0 and (sx2 - x)*(tx2 - x) <= 0 and (sy1 - y)*(ty1 - y) <= 0 and (sy2 - y)*(ty2 - y) <= 0:
                        total += 1
            except:
                pass

    # print(len(links))
    import numpy as np
    import matplotlib.pyplot as plt
    plt.gca().invert_yaxis()
    for i in links:
        plt.plot([ nodes[ i['source']['index']] ['x'], nodes[i['target']['index']] ['x'] ],  [ nodes[ i['source']['index']] ['y'], nodes[i['target']['index']] ['y']  ], 'k-')

    x = []
    y = []
    for i in nodes:
        x.append(i['x'])
        y.append(i['y'])
        plt.plot(x, y, 'o')
    plt.show()
    return total

def aspect(data):
    boxes = data['groups']
    mean = 0
    for i in boxes:
        as1 = i['dx']/i['dy']
        as2 = i['dy']/i['dx']
        aspect = max([as1, as2])
        mean += aspect
    return mean / len(boxes)

def spaceWasteddata(data):
    boxes = data['groups']
    minx = boxes[0]['x']
    maxx = minx + boxes[0]['dx']
    miny = boxes[0]['y']
    maxy = miny + boxes[0]['dy']
    area = 0
    for i in boxes:
        area += i['dx'] * i['dy']
        minx = min([minx, i['x']])
        maxx = max([maxx, i['x'] + i['dx']])
        miny = min([miny, i['y']])
        maxy = max([maxy, i['y'] + i['dy']])
    total = (maxx - minx)*(maxy - miny)
    return area / total


if __name__ == '__main__':
    print( 'The number of crossing is ' + str(edgeCross()) )
    print('Mean aspect ratio is ' + str(aspect() ) )
    print('Mean space wasted is ' + str(spaceWasted()))
