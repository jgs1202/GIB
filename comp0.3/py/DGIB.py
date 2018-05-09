# -*- coding: utf-8 -*-

# size is 900*600

import json
from operator import itemgetter
import math
import csv
import copy
import os
import sys

def doughnut( data, groups, path, dir, file, width, height, Gdegree):
    center = []
    total = 0
    length = len(groups)

    for i in range(length):
        total += len(groups[i])
    # for i in range(length):
    #     dic = {}
    #     dic['size'] = (len(groups[i])/total)
    #     dic['index'] = i
    #     groupSize.append(dic)

    #make lisk 'groupSize' along Gdegree
    groupSize = []
    for i in range(length):
        dic = {}
        dic['size'] = (len(groups[Gdegree[i][0]])/total)
        dic['index'] = Gdegree[i][0]
        dic['connect'] = Gdegree[i][1]
        groupSize.append(dic)
    # for i in groupSize:
    #     for j in range(len(groups)):
    #         if Gdegree[j][0] == i['index']:
    #                 print(Gdegree[j])

    # length = len(groups)
    # maxSize = 0
    # for i in range(length):
    #     if groupSize[i]['size'] > groupSize[maxSize]['size']:
    #         maxSize = i
    #
    # top = copy.deepcopy(groupSize[maxSize])
    # del groupSize[maxSize]
    # groupSize.sort(key=itemgetter('size'), reverse = True )
    # groupSize.insert(0, top)

    length = len(groups)
    verify = 0
    num = 0
    while ( verify == 0 and num < 10):
        GS = copy.deepcopy( groupSize )
        lengthC = len(center)
        for i in range(lengthC):
            del center[0]
        i = 0
        CorD = 0
        sequence  = 0
        while(verify == 0) and (CorD < length * 100):
            if i == 0:
                # print('case0')
                # print(GS[i]['connect'])
                w = width * math.sqrt(GS[i]['size'])
                h = height * math.sqrt(GS[i]['size'])
                center.append( [ GS[i]['index'], width/2, height/2, w/2, h/2 ] )
                v1RT = [width/2 - w/2, (height-h)/2 ]
                v2LT = [width/2 + w/2, (height-h)/2 ]
                h1LT = [0, 0]
                h2LT = [width/2 - w/2, (height+h)/2 ]
                # print(v1RT, v2LT, h1LT, h2LT)

            elif i%4 == 1:
                h = height/2 - center[0][4]
                w = width * height * GS[i]['size'] / h
                if max([w/h, h/w]) < 100:
                    # print('case1')
                    if h1LT[0] + w > width:
                        # print('case11')
                        GS.insert(i,'dummy')
                        sequence += 1
                    else:
                        center.append( [ GS[i]['index'], h1LT[0] + w/2, h1LT[1] + h/2, w/2, h/2 ])
                        h1LT[0] = h1LT[0] + w
                        sequence = 0
                else:
                    # print('case2')
                    GS.insert(i,'dummy')
                    sequence += 1
            elif i%4 == 2:
                h = height/2 - center[0][4]
                w = width * height * GS[i]['size'] / h
                if max([w/h, h/w]) < 100:
                    # print('case3')
                    if h2LT[0] + w > width:
                        # print('case12')
                        GS.insert(i,'dummy')
                        sequence += 1
                    else:
                        center.append( [ GS[i]['index'], h2LT[0] + w/2, h2LT[1] + h/2, w/2, h/2 ])
                        h2LT[0] = h2LT[0] + w
                        sequence = 0
                else:
                    # print('case4')
                    GS.insert(i,'dummy')
                    sequence += 1
            elif i%4 == 3:
                w = v1RT[0]
                h = width * height * GS[i]['size'] / w
                if max([w/h, h/w]) < 100:
                    # print('case5')
                    if v1RT[1] + h > height:
                        # print('case13')
                        GS.insert(i,'dummy')
                        sequence += 1
                    else:
                        center.append( [ GS[i]['index'], w/2 , v1RT[1] + h/2, w/2, h/2 ] )
                        v1RT[1] = v1RT[1] + h
                        sequence = 0
                else:
                    GS.insert(i, 'dummy')
                    # print('case6')
                    sequence += 1
            elif i%4 == 0:
                w = width - v2LT[0]
                h = width * height * GS[i]['size'] / w
                if max([w/h, h/w]) < 100:
                    # print('case7')
                    # print(v2LT[1] , h , height - h2LT[1])
                    if v2LT[1] + h >  h2LT[1]:
                        # print('case14')
                        GS.insert(i,'dummy')
                        sequence += 1
                    else:
                        center.append( [ GS[i]['index'], v2LT[0] + w/2 , v2LT[1] + h/2, w/2, h/2 ] )
                        v2LT[1] = v2LT[1] + h
                        sequence = 0
                else:
                    GS.insert(i, 'dummy')
                    sequence += 1
                    # print('case8')
            # else:
                # print('error')
            if sequence > 3:
                for j in range(len(groupSize)):
                    groupSize[j]['size'] = groupSize[j]['size'] * 0.9
                print('over')
                break
            # print( str(i) + ' : '+ str(center[i]) )
            if i == len(GS) - 1 :
                verify = 1
            i += 1
            CorD += 1
            if CorD == length*100:
                print('This data is not suited to Doughunt layout.')
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
    forWrite['file'] = data['file']
    forWrite['groupSize'] = data['groupSize']
    forWrite['pgroup'] = data['pgroup']
    forWrite['pout'] = data['pout']
    forWrite['linkSize'] = data['linkSize']
    forWrite['nodeSize'] = data['nodeSize']

    print(len(forWrite['groups'])-1, data['groupSize'], len(groupSize))
    try:
        # verify = os.listdir('../data/Chaturvedi/temp/' + dir)
        verify = os.listdir('../data/Chaturvedi/temp/')
    except:
        # os.mkdir('../data/Chaturvedi/temp/' + dir)
        os.mkdir('../data/Chaturvedi/temp/')
    # f = open('../data/Chaturvedi/temp/' + dir + '/' + file, 'w')
    f = open('../data/Chaturvedi/temp/' + file, 'w')
    json.dump(forWrite, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    # import pylab as pl
    # pl.xticks([0, width])
    # pl.yticks([0, height])
    # for i in center:
    #     # if i[2] == 15:
    #     pl.gca().add_patch( pl.Rectangle(xy=[i[1]-i[3], height - i[2]-i[4]], width=i[3]*2, height=i[4]*2, linewidth='1.0', fill=False) )
    #     # print(i)
    # pl.show()
