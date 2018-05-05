# -*- coding: utf-8 -*-

# size is 900*600

import json
import os
from operator import itemgetter
import math
import csv
import copy
import sys
from itertools import combinations
from statistics import mean, stdev
import community
import networkx as nx
from networkx.readwrite import json_graph


def edgeCross(data):
    nodes = [(node['cx'], node['cy']) for node in data['nodes']]
    links = [(link['source'], link['target']) for link in data['links']]
    total = 0

    for (index1, index2), (index3, index4) in combinations(links, 2):
        sx1, sy1 = nodes[index1]
        tx1, ty1 = nodes[index2]
        sx2, sy2 = nodes[index3]
        tx2, ty2 = nodes[index4]

        # if an either of thw two links is vertical, we do not count
        if tx1 == sx1 and tx2 != sx2:
            x = tx1
            y = (ty2 - sy2) / (tx2 - sx2) * (x - sx2) + sy2
        elif tx1 != sx1 and tx2 == sx2:
            x = tx2
            y = (ty1 - sy1) / (tx1 - sx1) * (x - sx1) + sy1
        else:
            tan1 = (ty1 - sy1) / (tx1 - sx1)
            tan2 = (ty2 - sy2) / (tx2 - sx2)
            # tan1 * x - tan1 * sx1 + sy1 = tan2 * x - tan2 * sx2 + sy2
            x = (sy2 - sy1 + tan1 * sx1 - tan2 * sx2) / (tan1 - tan2)
            y = tan1 * (x - sx1) + sy1
        # if intersection point is same as either of source or target we do not count
        if x == sx1 and y == sy1:
            continue
        if x == sx2 and y == sy2:
            continue
        if x == tx1 and y == ty1:
            continue
        if x == tx2 and y == ty2:
            continue
        if (sx1 > x and tx1 > x) or (sx1 < x and tx1 < x):
            continue
        if (sx2 > x and tx2 > x) or (sx2 < x and tx2 < x):
            continue
        if (sy1 > y and ty1 > y) or (sy1 < y and ty1 < y):
            continue
        if (sy1 > y and ty1 > y) or (sy1 < y and ty1 < y):
            continue
        total += 1
    return total


def modularity(data):
    G = nx.Graph()
    G = json_graph.node_link_graph(data)
    part = community.best_partition(G)
    mod = community.modularity(part,G)
    return mod

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
            data[i][9] = float(data[i][9])
        if data[i][0] == 'FDGIB':
            data[i][7] = 1.0
    for i in data:
        if i[0] != 'type':
            dic = {}
            dic['type'], dic['groupSize'], dic['pgroup'], dic['pout'], dic['nodeSize'], dic['linkSize'], dic['edgeCross'], dic['meanAspect'], dic['meanSpaceWasted'], dic['meanModularity'] = i[0], i[1], i[2], i[3], 0,0,[],[],[],[]
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
                list[i]['meanModularity'].append(datum[9])
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
        list[i]['devEdgeCross'] = stdev(list[i]['edgeCross'])
        list[i]['edgeCross'] = mean(list[i]['edgeCross'])
        list[i]['devAspect'] = stdev(list[i]['meanAspect'])
        list[i]['meanAspect'] = mean(list[i]['meanAspect'])
        list[i]['devSpaceWasted'] = stdev(list[i]['meanSpaceWasted'] )
        list[i]['meanSpaceWasted'] = mean(list[i]['meanSpaceWasted'] )
        list[i]['meanModularity'] = mean(list[i]['meanModularity'])
    f = open('./result.json', 'w')
    json.dump(list, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))



if __name__ == '__main__':
    pathes = []
    pathes.append( './data/')
    # pathes.append( '../data/TRGIB/comp/')
    # pathes.append( '../data/Chaturvedi/comp/')
    # pathes.append( '../data/FDGIB/comp/')
    outputData = [['type', 'groupSize', 'pgroup', 'pout', 'nodeSize', 'linkSize', 'edgeCross', 'meanAspect', 'meanSpaceWasted', 'meanModularity']]
    for path in pathes:
        type = 'STGIB'
        for file in os.listdir(path):
            if file != '.DS_Store':
            # if file == '0.json' or file=='1.json'or file=='2.json':
                print(file)
                data = json.load( open(path + file, 'r') )
                list = []
                crossing = edgeCross(data)
                list.extend( [type,  data['groupSize'], data['pgroup'], data['pout'], data['nodeSize'], data['linkSize'], crossing, aspect(data), spaceWasted(data), modularity(data) ] )
                outputData.append(list)
    getStatic(outputData)


