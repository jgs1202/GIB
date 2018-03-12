# -*- coding: utf-8 -*-

# size is 900*600

import json
from operator import itemgetter
import math
import csv
import copy
import sys

def readjson(nodes, groups, links):
    reader = open('data/data.json', 'r')
    nodes= json.load(reader)
    links = nodes['links']
    nodes = nodes['nodes']
    length = len(nodes)

    maxGroup = 0
    for i in range(length):
        current = nodes[i]['group']
        if current > maxGroup:
            maxGroup = current
    for i in range(maxGroup+1):
        groups.append([])

    for i in range(length):
        dic = {}
        dic['number'] = i
        # dic['x'] = nodes[i]['x']
        # dic['y'] = nodes[i]['y']
        groups[nodes[i]['group']].append(dic)
    # print(groups)

def calcSize(groups, width, height, groupSize):
    total = 0
    length = len(groups)
    for i in range(length):
        total += len(groups[i])
    for i in range(length):
        dic = {}
        # print(len(groups[i])/total)
        # dic['size'] = math.sqrt(len(groups[i])/total)
        dic['size'] = (len(groups[i])/total)
        dic['index'] = i
        groupSize.append(dic)
    groupSize.sort(key=itemgetter('size'), reverse = True )
    # print(groupSize)

def croissant(groups, width, height, groupSize, center, nodes, links):

    length = len(groups)
    verify = 0
    num = 0
    print(length)
    while ( verify == 0 and num < 10):
        GS = copy.deepcopy( groupSize )
        print(num)
        print(GS[0])
        lengthC = len(center)
        for i in range(lengthC):
            del center[0]
        i = 0
        sequence = 0
        CorD = 0
        while(verify == 0) and CorD < length * 10:
            print(i)
            if i == 0:
                w = width * math.sqrt(GS[i]['size'])
                h = height * math.sqrt(GS[i]['size'])
                center.append( [ GS[i]['index'], width/2, h/2, w/2, h/2 ] )
                v1RT = [width/2 - w/2, 0]
                v2LT = [width/2 + w/2, 0]
                h2LT = [width/2 - w/2, h]
                print('first')

            elif i%3 == 1:
                print('second')
                h = height - h2LT[1]
                w = width * height * GS[i]['size'] / h
                if max([w/h, h/w]) < 100:
                    if h2LT[0] + w > width:#/2 + center[0][3]:
                        sequence += 1
                        GS.insert(i,'dummy')
                        print('case1')
                    else:
                        center.append( [ GS[i]['index'], h2LT[0] + w/2, h2LT[1] + h/2, w/2, h/2 ])
                        h2LT[0] = h2LT[0] + w
                        sequence = 0
                        print('case2')
                else:
                    GS.insert(i,'dummy')
                    print('case3')
            elif i%3 == 2:
                print('third')
                w = v1RT[0]
                h = width * height * GS[i]['size'] / w
                if max([w/h, h/w]) < 100:
                    if v1RT[1] + h > height:
                        GS.insert(i,'dummy')
                        sequence += 1
                        print('case1')
                    else:
                        center.append( [ GS[i]['index'], 0 + w/2, v1RT[1] + h/2, w/2, h/2 ] )
                        v1RT[1] = v1RT[1] + h
                        print('case2')
                else:
                    GS.insert(i, 'dummy')
                    print('case3')
            elif i%3 == 0:
                print('fourth')
                w = width - v2LT[0]
                h = width * height * GS[i]['size'] / w
                if max([w/h, h/w]) < 100:
                    if v2LT[1] + h > height - center[0][1]:
                        GS.insert(i,'dummy')
                        sequence += 1
                        print('case1')
                    else:
                        center.append( [ GS[i]['index'], v2LT[0] + w/2 , v2LT[1] + h/2, w/2, h/2 ] )
                        v2LT[1] = v2LT[1] + h
                        print('case2')
                else:
                    GS.insert(i, 'dummy')
                    print('case3')
            # print( str(i) + ' : '+ str(center[i]) )
            else:
                print('error')
            if  sequence > 3:
                for j in range(len(groupSize)):
                    groupSize[j]['size'] = groupSize[j]['size'] * 0.9
                print('over')
                break
            if i == len(GS) - 1 :
                verify = 1
            i += 1
            CorD += 1
            if CorD == length*10:
                print('This data is not suited to Croissant layout.')
                sys.exit()
        num += 1
    # print('center is ')
    # print(center)
    print(num)


    print(len(center))
    center.sort(key=itemgetter(0))
    # print(center)

    length = len(center)
    data = []
    for i in range(length):
        data.append( center[1:] )

    with open('CGIB_boxes.csv', 'w') as f:
        writer = csv.writer(f)
        for i in data:
            writer.writerow(i)

    groupCoo = []
    for i in center:
        dic = {}
        dic['x'] = i[1] - i[3]
        dic['y'] = i[2] - i[4]
        dic['dx'] = i[3]*2
        dic['dy'] = i[4]*2
        groupCoo.append(dic)
    dic = {}
    dic['x'] = 0
    dic['y'] = 0
    dic['dx'] = width
    dic['dy'] = height
    groupCoo.append(dic)


    reader = open('data/data.json', 'r')
    nodes= json.load(reader)
    links = nodes['links']
    nodes = nodes['nodes']

    forWrite = {}
    forWrite['nodes'] = nodes
    forWrite['links'] = links
    forWrite['groups'] = groupCoo

    f = open('data/data_CGIB.json', 'w')
    json.dump(forWrite, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    nodes = []
    groups = []
    groupSize = []
    center = []
    links = []
    width = 900
    height = 600
    readjson(nodes, groups, links)
    calcSize(groups, width, height, groupSize)
    croissant(groups, width, height, groupSize, center, nodes, links)
    print(groupSize)

    import pylab as pl
    pl.xticks([0, width])
    pl.yticks([0, height])
    for i in center:
        # if i[2] == 15:
        pl.gca().add_patch( pl.Rectangle(xy=[i[1]-i[3], height - i[2]-i[4]], width=i[3]*2, height=i[4]*2, linewidth='1.0', fill=False) )
        # print(i)
    pl.show()
