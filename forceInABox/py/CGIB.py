# -*- coding: utf-8 -*-

# size is 900*600

import json
from operator import itemgetter
import math
import csv
import copy
import os
import sys

def croissant( mostConnect, data, groups, path, dir, file, width, heigh):
    center = []
    total = 0
    length = len(groups)
    for i in range(length):
        total += len(groups[i])
    for i in range(length):
        dic = {}
        dic['size'] = (len(groups[i])/total)
        dic['index'] = i
        groupSize.append(dic)

    length = len(mostConnect)
    maxSize = 0
    for i in range(length):
        if groupSize[i] > groupSize[maxSize]:
            maxSize = i

    top = copy.deepcopy(groupSize[maxSize])
    del groupSize[maxSize]
    groupSize.sort(key=itemgetter('size'), reverse = True )
    groupSize.insert(0, top)

    length = len(groups)
    verify = 0
    num = 0
    # print(length)
    while ( verify == 0 and num < 10):
        GS = copy.deepcopy( groupSize )
        # print(num)
        # print(GS[0])
        lengthC = len(center)
        for i in range(lengthC):
            del center[0]
        i = 0
        sequence = 0
        CorD = 0
        while(verify == 0) and CorD < length * 10:
            # print(i)
            if i == 0:
                w = width * math.sqrt(GS[i]['size'])
                h = height * math.sqrt(GS[i]['size'])
                center.append( [ GS[i]['index'], width/2, h/2, w/2, h/2 ] )
                v1RT = [width/2 - w/2, 0]
                v2LT = [width/2 + w/2, 0]
                h2LT = [width/2 - w/2, h]
                # print('first')

            elif i%3 == 1:
                # print('second')
                h = height - h2LT[1]
                w = width * height * GS[i]['size'] / h
                if max([w/h, h/w]) < 100:
                    if h2LT[0] + w > width:#/2 + center[0][3]:
                        sequence += 1
                        GS.insert(i,'dummy')
                        # print('case1')
                    else:
                        center.append( [ GS[i]['index'], h2LT[0] + w/2, h2LT[1] + h/2, w/2, h/2 ])
                        h2LT[0] = h2LT[0] + w
                        sequence = 0
                        # print('case2')
                else:
                    GS.insert(i,'dummy')
                    # print('case3')
            elif i%3 == 2:
                # print('third')
                w = v1RT[0]
                h = width * height * GS[i]['size'] / w
                if max([w/h, h/w]) < 100:
                    if v1RT[1] + h > height:
                        GS.insert(i,'dummy')
                        sequence += 1
                        # print('case1')
                    else:
                        center.append( [ GS[i]['index'], 0 + w/2, v1RT[1] + h/2, w/2, h/2 ] )
                        v1RT[1] = v1RT[1] + h
                        # print('case2')
                else:
                    GS.insert(i, 'dummy')
                    # print('case3')
            elif i%3 == 0:
                # print('fourth')
                w = width - v2LT[0]
                h = width * height * GS[i]['size'] / w
                if max([w/h, h/w]) < 100:
                    if v2LT[1] + h > height - center[0][1]:
                        GS.insert(i,'dummy')
                        sequence += 1
                        # print('case1')
                    else:
                        center.append( [ GS[i]['index'], v2LT[0] + w/2 , v2LT[1] + h/2, w/2, h/2 ] )
                        v2LT[1] = v2LT[1] + h
                        # print('case2')
                else:
                    GS.insert(i, 'dummy')
                    # print('case3')
            # print( str(i) + ' : '+ str(center[i]) )
            # else:
                # print('error')
            if sequence > 3:
                for j in range(len(groupSize)):
                    groupSize[j]['size'] = groupSize[j]['size'] * 0.9
                # print('over')
                break
            if i == len(GS) - 1 :
                verify = 1
            i += 1
            CorD += 1
            if CorD == length*10:
                print('This data is not suited to Croissant layout.')
                sys.exit()
        num += 1

    # print('complete')
    center.sort(key=itemgetter(0))
    # print(center)

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

    links = data['links']
    nodes = data['nodes']

    forWrite = {}
    forWrite['nodes'] = nodes
    forWrite['links'] = links
    forWrite['groups'] = groupCoo
    forWrite['groupSize'] = data['groupSize']
    forWrite['pgroup'] = data['pgroup']
    forWrite['pout'] = data['pout']

    try:
        verify = os.listdir('../data/Chaturvedi/temp/' + dir)
    except:
        os.mkdir('../data/Chaturvedi/temp/' + dir)
    f = open('../data/Chaturvedi/temp/' + dir + '/' + file, 'w')
    json.dump(forWrite, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
