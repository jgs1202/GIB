# -*- coding: utf-8 -*-

# size is 900*600

import json
import os
from operator import itemgetter
import math
import csv
import copy
import sys
from statistics import mean, stdev

def edgeCross(data):

    nodes = data['nodes']
    links = data['links']

    length = len(links)
    total = 0

    for i in range(length):
        # sx1 = nodes[ links[i]['source']['index'] ]['x']
        # sy1 = nodes[ links[i]['source']['index'] ]['y']
        # tx1 = nodes[ links[i]['target']['index'] ]['x']
        # ty1 = nodes[ links[i]['target']['index'] ]['y']
        # index1 = links[i]['source']['index']
        # index2 = links[i]['target']['index']
        sx1 = nodes[ links[i]['source'] ]['cx']
        sy1 = nodes[ links[i]['source'] ]['cy']
        tx1 = nodes[ links[i]['target'] ]['cx']
        ty1 = nodes[ links[i]['target'] ]['cy']
        index1 = links[i]['source']
        index2 = links[i]['target']
        # print('i = ' + str(i))

        for j in range (length - i - 1):
            sx2 = nodes[ links[i+j+1]['source'] ]['cx']
            sy2 = nodes[ links[i+j+1]['source'] ]['cy']
            tx2 = nodes[ links[i+j+1]['target'] ]['cx']
            ty2 = nodes[ links[i+j+1]['target'] ]['cy']
            index3 = links[i+j+1]['source']
            index4 = links[i+j+1]['target']

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
    # import numpy as np
    # import matplotlib.pyplot as plt
    # plt.gca().invert_yaxis()
    # for i in links:
    #     plt.plot([ nodes[ i['source']['index']] ['x'], nodes[i['target']['index']] ['x'] ],  [ nodes[ i['source']['index']] ['y'], nodes[i['target']['index']] ['y']  ], 'k-')
    #
    # x = []
    # y = []
    # for i in nodes:
    #     x.append(i['x'])
    #     y.append(i['y'])
    #     plt.plot(x, y, 'o')
    # plt.show()
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

def spaceWasted(data):
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
    # print((area - total)/total)
    return ((area - total)/total)

def getStatic(data):
    list = []
    for i in range(len(data)):   
        if i != 0:
            data[i][1] = int(data[i][1])
            data[i][2] = float(data[i][2]) 
            data[i][3] = float(data[i][3])
            data[i][4] = int(data[i][4])
            data[i][5] = int(data[i][5])
            data[i][6] = int(data[i][6])
            data[i][7] = float(data[i][7])
            data[i][8] = float(data[i][8])
        if data[i][0] == 'FDGIB':
            data[i][7] = 1.0
    for i in data:
        if i[0] != 'type':
            dic = {}
            dic['type'], dic['groupSize'], dic['pgroup'], dic['pout'], dic['nodeSize'], dic['linkSize'], dic['edgeCross'], dic['meanAspect'], dic['meanSpaceWasted'] = i[0], i[1], i[2], i[3], 0,0,[],[],[]
            if dic not in list:
                list.append(dic)
    for datum in data:
        for i in range(len(list)):
            if datum[0] == list[i]['type'] and datum[1] == list[i]['groupSize'] and datum[2] == list[i]['pgroup'] and datum[3] == list[i]['pout']:
                # print(datum[4])
                list[i]['nodeSize'] += datum[4]
                list[i]['linkSize'] += datum[5]
                list[i]['edgeCross'].append(datum[6])
                list[i]['meanAspect'].append(datum[7])
                list[i]['meanSpaceWasted'].append(datum[8])
                if 'total' in list[i].keys():
                    list[i]['total'] += 1
                else:
                    list[i]['total'] = 0
    for i in range(len(list)):
        try:
            list[i]['nodeSize'] /= list[i]['total']
            list[i]['linkSize'] /= list[i]['total']
        except:
            print('total is zero')
        print(list[i]['edgeCross'])
        list[i]['devEdgeCross'] = stdev(list[i]['edgeCross'])
        list[i]['edgeCross'] = mean(list[i]['edgeCross'])
        list[i]['devAspect'] = stdev(list[i]['meanAspect'])
        list[i]['meanAspect'] = mean(list[i]['meanAspect'])
        list[i]['devSpaceWasted'] = stdev(list[i]['meanSpaceWasted'] )
        list[i]['meanSpaceWasted'] = mean(list[i]['meanSpaceWasted'] )
    f = open('../data/result.json', 'w')
    json.dump(list, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))



if __name__ == '__main__':
    pathes = []
    pathes.append( '../data/STGIB/comp/')
    pathes.append( '../data/TRGIB/comp/')
    pathes.append( '../data/Chaturvedi/comp/')
    pathes.append( '../data/FDGIB/comp/')
    outputData = [['type', 'groupSize', 'pgroup', 'pout', 'nodeSize', 'linkSize', 'edgeCross', 'meanAspect', 'meanSpaceWasted']]
    for path in pathes:
        type = (path[8:13])
        for file in os.listdir(path):
            if file != '.DS_Store':
            # if file == '0.json' or file=='1.json'or file=='2.json':
                print(file)
                data = json.load( open(path + file, 'r') )
                list = []
                crossing = edgeCross(data)
                list.extend( [type,  data['groupSize'], data['pgroup'], data['pout'], data['nodeSize'], data['linkSize'], crossing, aspect(data), spaceWasted(data) ] )
                outputData.append(list)
    getStatic(outputData)


