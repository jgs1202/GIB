# -*- coding: utf-8 -*-

# size is 900*600

import json
from operator import itemgetter
import math
import csv
import copy
import sys
import os

def readjson(nodes, groups):
    reader = open('../data/origin/data.json', 'r')
    data = json.load(reader)
    nodes = data['nodes']
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

def dougnut(groups, width, height, groupSize, center):

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
        CorD = 0
        sequence  = 0
        while(verify == 0) and CorD < length * 10:
            if i == 0:
                # print('case0')
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
                if max([w/h, h/w]) < 10:
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
            elif i%4 == 2:
                h = height/2 - center[0][4]
                w = width * height * GS[i]['size'] / h
                # if max([w/h, h/w]) < 10:
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
            elif i%4 == 3:
                w = v1RT[0]
                h = width * height * GS[i]['size'] / w
                if max([w/h, h/w]) < 10:
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
            elif i%4 == 0:
                w = width - v2LT[0]
                h = width * height * GS[i]['size'] / w
                if max([w/h, h/w]) < 10:
                    # print('case7')
                    # print(v2LT[1] , h , height - h2LT[1])
                    if v2LT[1] + h >  h2LT[1]:
                        # print('case14')
                        GS.insert(i,'dummy')
                        sequence += 1
                    else:
                        center.append( [ GS[i]['index'], v2LT[0] + w/2 , v2LT[1] + h/2, w/2, h/2 ] )
                        v2LT[1] = v2LT[1] + h
                        sequence
                else:
                    GS.insert(i, 'dummy')
                    # print('case8')
            else:
                print('error')
            if  sequence > 3:
                for j in range(len(groupSize)):
                    groupSize[j]['size'] = groupSize[j]['size'] * 0.9
                print('over')
                break
            # print( str(i) + ' : '+ str(center[i]) )
            if i == len(GS) - 1 :
                verify = 1
            i += 1
            CorD += 1
            if CorD == length*10:
                print('This data is not suited to Doughunt layout.')
                sys.exit()
        num += 1
    # print('center is ')
    # print(center)
    print(num)

    center.sort(key=itemgetter(0))
    print(center)

    length = len(center)
    data = []
    for i in range(length):
        data.append( center[1:] )

    # with open('DGIB_boxes.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     for i in data:
    #         writer.writerow(i)

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


    reader = open('../data/origin/data.json', 'r')
    data = json.load(reader)
    links = data['links']
    nodes = data['nodes']

    forWrite = {}
    forWrite['nodes'] = nodes
    forWrite['links'] = links
    forWrite['groups'] = groupCoo

    try:
        verify = os.listdir('../data/DGIB/' + dir)
    except:
        os.mkdir('../data/DGIB/' + dir)
    f = open('../data/DGIB/' + dir + '/' + file, 'w')
    json.dump(forWrite, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main = '../data/origin/'
    global dir
    for dir in os.listdir(main):
        if (dir != '.DS_Store'):
            try:
                global file
                for file in os.listdir(main + dir):
                    # print(file)
                    if (dir != '.DS_Store'):
                        global path
                        path = main + dir + '/' + file
                        nodes = []
                        groups = []
                        groupSize = []
                        center = []
                        width = 960
                        height = 600
                        readjson(nodes, groups)
                        calcSize(groups, width, height, groupSize)
                        dougnut(groups, width, height, groupSize, center)
                        # print(groupSize)
            except:
                pass

    import pylab as pl
    pl.xticks([0, width])
    pl.yticks([0, height])
    for i in center:
        # if i[2] == 15:
        pl.gca().add_patch( pl.Rectangle(xy=[i[1]-i[3], height - i[2]-i[4]], width=i[3]*2, height=i[4]*2, linewidth='1.0', fill=False) )
        # print(i)
    pl.show()
