# -*- coding: utf-8 -*-

# size is 900*600

import csv
import copy
import json
import math
import numpy as np
import matplotlib.pyplot as plt

def makeData(center, links, boxes):
    f = open('boxes.csv', 'r')
    reader1 = csv.reader(f)
    for i in reader1:
        boxes.append(i)

    # print(boxes)

    linkWeights = []
    f = open('link_boxes.csv', 'r')
    reader2 = csv.reader(f)
    for i in reader2:
        linkWeights.append(i)

    lengthBox = len(boxes)
    for i in range(lengthBox):
        #15 は原因じゃない
        dirx = abs( float(boxes[i][3]) - float(boxes[i][2]) )/2
        diry = abs( float(boxes[i][1]) - float(boxes[i][0])) /2
        # print(dirx, diry)
        if dirx == 0:
            dirx = 15
        if diry == 0:
            diry = 15
        center.append( [ float(boxes[i][2]) + dirx , float(boxes[i][0]) + diry, dirx, diry])

    # print(center)

    num1 = len(linkWeights)
    for i in range(num1):
        num2 = len(linkWeights[i])
        for j in range(num2):
            if float(linkWeights[i][j]) != 0.0:
                dic = {}
                dic['node1'] = i
                dic['node2'] = i+j
                links.append(dic)
    # print(links)

def checkPRISM(center, links, boxes):
    width = 900
    height = 600
    oldcenter = copy.deepcopy(center)
    t = []
    num = 0
    while num < 100 and int(t.count(1.0)) != int(len(links)):
        t = []
        which = {}
        length = len(links)
        excenter = copy.deepcopy(center)
        for i in range(length):
            t.append(1.0)

        # center[5][2] = 800
        # print(center)

        for i in range(length):
            xover = ( center[links[i]['node1']][2] + center[links[i]['node2']][2] +5) / ( abs( center[links[i]['node1']][0] - center[links[i]['node2']][0]) )
            yover = ( center[links[i]['node1']][3] + center[links[i]['node2']][3] +5) / ( abs( center[links[i]['node1']][1] - center[links[i]['node2']][1]) )
            # print(xover, center[links[i]['node1']][2], center[links[i]['node2']][2] ,center[links[i]['node1']][0] , center[links[i]['node2']][0])
            # print(xover, yover)
            if xover < yover:
                which['key'] = 'x'
                which['value'] = xover
            else:
                which['key'] = 'y'
                which['value'] = yover
            if which['value'] > 1.0:
                t[i] = which['value']
            else:
                t[i] = 1.0
            if t[i] > 1.5:
                t[i] = 1.5

        for i in range(length):
            if t[i]>1.0:
                # print('ex')
                # print(center[links[i]['node1']])
                # print(center[links[i]['node2']])

                dis1 = math.sqrt( math.pow((center[links[i]['node1']][0] - width/2), 2) + math.pow((center[links[i]['node1']][1] - height/2), 2) )
                dis2 = math.sqrt( math.pow((center[links[i]['node2']][0] - width/2), 2) + math.pow((center[links[i]['node2']][1] - height/2), 2) )
                # print(dis1, dis2)
                # print(which['key'])
                if which['key'] == 'x':
                    # print('xmove')
                    if dis1 > dis2: #which group should we move
                        if center[links[i]['node1']][0] < center[links[i]['node2']][0]: #which direction should we move to
                            print('1')
                            center[links[i]['node1']][0] = center[links[i]['node2']][0] -  center[links[i]['node1']][2] - center[links[i]['node2']][2] - 15
                        else:
                            print('2')
                            center[links[i]['node1']][0] = center[links[i]['node2']][0] + center[links[i]['node1']][2] + center[links[i]['node2']][2] + 15
                    else:
                        if center[links[i]['node2']][0] < center[links[i]['node1']][0]: #which direction should we move to
                            print('3')
                            center[links[i]['node2']][0] = center[links[i]['node1']][0] -  center[links[i]['node1']][2] - center[links[i]['node2']][2] - 15
                        else:
                            print('4')
                            center[links[i]['node2']][0] = center[links[i]['node1']][0] + center[links[i]['node1']][2] + center[links[i]['node2']][2] + 15
                elif which['key'] == 'y':
                    # print('ymove')
                    if dis1 > dis2: #which group should we move
                        if center[links[i]['node1']][1] < center[links[i]['node2']][1]: #which direction should we move to
                            print('5')
                            center[links[i]['node1']][1] = center[links[i]['node2']][1] -  center[links[i]['node1']][3] - center[links[i]['node2']][3] - 15
                        else:
                            print('6')
                            center[links[i]['node1']][1] = center[links[i]['node2']][1] + center[links[i]['node1']][3] + center[links[i]['node2']][3] + 15
                    else:
                        if center[links[i]['node2']][1] < center[links[i]['node1']][1]: #which direction should we move to
                            print('7')
                            center[links[i]['node2']][1] = center[links[i]['node1']][1] -  center[links[i]['node1']][3] - center[links[i]['node2']][3] - 15
                        else:
                            print('8')
                            center[links[i]['node2']][1] = center[links[i]['node1']][1] + center[links[i]['node1']][3] + center[links[i]['node2']][3] + 15
                # print('new')
                # print(center[links[i]['node1']])
                # print(center[links[i]['node2']])

        print( 'num is ' + str(num))
        print(t)
        # for i in range(10):
        #     print(str(center[i][0] - excenter[i][0]) + ', ' + str(center[i][1] - excenter[i][1]))
        print('the number of t is ' + str(t.count(1.0)))
        num += 1

    # with open('PRISM_boxes.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     for i in center:
    #         writer.writerow(i)
    # length1 = len(center)
    # dif = []
    # for i in range(length1):
    #     dif.append([])
    # for i in range(length1):
    #     length2 = len(center[i])
    #     for j in range(length2) :
    #         dif[i].append( center[i][j] - oldcenter[i][j] )
    #
    # reader = open('nodes.json', 'r')
    # nodes= json.load(reader)
    # length = len(nodes)
    # for i in range(length):
    #     for j in range(2):
    #         nodes[i]['x'] += dif[ nodes[i]['group'] ][0]
    #         nodes[i]['y'] += dif[ nodes[i]['group'] ][1]
    #
    # f = open('PRISM_nodes.json', 'w')
    # json.dump(nodes, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def checkAll(center, boxes):
    width = 900
    height = 600
    oldcenter = copy.deepcopy(center)
    links = []

    # set viutual links
    length  = len(boxes)
    for i in range(length):
        for j in range(1,length - i):
            dic = {}
            dic['node1'] = i
            dic['node2'] = i + j
            links.append(dic)
    print(links)

    t = []
    num = 0
    while num < 100 and int(t.count(1.0)) != int(len(links)):
        t = []
        which = {}
        length = len(links)
        excenter = copy.deepcopy(center)
        for i in range(length):
            t.append(1.0)

        # center[5][2] = 800
        # print(center)

        for i in range(length):
            xover = ( center[links[i]['node1']][2] + center[links[i]['node2']][2]+5) / ( abs( center[int(links[i]['node1'])][0] - center[int(links[i]['node2'])][0]) )
            yover = ( center[links[i]['node1']][3] + center[links[i]['node2']][3]+5) / ( abs( center[links[i]['node1']][1] - center[links[i]['node2']][1]) )
            # print(xover, center[links[i]['node1']][2], center[links[i]['node2']][2] ,center[links[i]['node1']][0] , center[links[i]['node2']][0])
            # print(xover, yover)
            if xover < yover:
                which['key'] = 'x'
                which['value'] = xover
            else:
                which['key'] = 'y'
                which['value'] = yover
            if which['value'] > 1.0:
                t[i] = which['value']
            else:
                t[i] = 1.0
            if t[i] > 1.5:
                t[i] = 1.5

        for i in range(length):
            if t[i]>1.0:
                # print('ex')
                # print(center[links[i]['node1']])
                # print(center[links[i]['node2']])

                dis1 = math.sqrt( math.pow((center[links[i]['node1']][0] - width/2), 2) + math.pow((center[links[i]['node1']][1] - height/2), 2) )
                dis2 = math.sqrt( math.pow((center[links[i]['node2']][0] - width/2), 2) + math.pow((center[links[i]['node2']][1] - height/2), 2) )
                # print(dis1, dis2)
                # print(which['key'])
                if which['key'] == 'x':
                    # print('xmove')
                    if dis1 > dis2: #which group should we move
                        if center[links[i]['node1']][0] < center[links[i]['node2']][0]: #which direction should we move to
                            print('1')
                            center[links[i]['node1']][0] = center[links[i]['node2']][0] -  center[links[i]['node1']][2] - center[links[i]['node2']][2] - 15
                        else:
                            print('2')
                            center[links[i]['node1']][0] = center[links[i]['node2']][0] + center[links[i]['node1']][2] + center[links[i]['node2']][2] + 15
                    else:
                        if center[links[i]['node2']][0] < center[links[i]['node1']][0]: #which direction should we move to
                            print('3')
                            center[links[i]['node2']][0] = center[links[i]['node1']][0] -  center[links[i]['node1']][2] - center[links[i]['node2']][2] - 15
                        else:
                            print('4')
                            center[links[i]['node2']][0] = center[links[i]['node1']][0] + center[links[i]['node1']][2] + center[links[i]['node2']][2] + 15
                elif which['key'] == 'y':
                    # print('ymove')
                    if dis1 > dis2: #which group should we move
                        if center[links[i]['node1']][1] < center[links[i]['node2']][1]: #which direction should we move to
                            print('5')
                            center[links[i]['node1']][1] = center[links[i]['node2']][1] -  center[links[i]['node1']][3] - center[links[i]['node2']][3] - 15
                        else:
                            print('6')
                            center[links[i]['node1']][1] = center[links[i]['node2']][1] + center[links[i]['node1']][3] + center[links[i]['node2']][3] + 15
                    else:
                        if center[links[i]['node2']][1] < center[links[i]['node1']][1]: #which direction should we move to
                            print('7')
                            center[links[i]['node2']][1] = center[links[i]['node1']][1] -  center[links[i]['node1']][3] - center[links[i]['node2']][3] - 15
                        else:
                            print('8')
                            center[links[i]['node2']][1] = center[links[i]['node1']][1] + center[links[i]['node1']][3] + center[links[i]['node2']][3] + 15
                # print('new')
                # print(center[links[i]['node1']])
                # print(center[links[i]['node2']])

        print( 'num is ' + str(num))
        print(t)
        # for i in range(10):
        #     print(str(center[i][0] - excenter[i][0]) + ', ' + str(center[i][1] - excenter[i][1]))
        print('the number of t is ' + str(t.count(1.0)))
        num += 1

    with open('PRISM_boxes.csv', 'w') as f:
        writer = csv.writer(f)
        for i in center:
            writer.writerow(i)
    length1 = len(center)
    dif = []
    for i in range(length1):
        dif.append([])
    for i in range(length1):
        length2 = len(center[i])
        for j in range(length2) :
            dif[i].append( center[i][j] - oldcenter[i][j] )

    reader = open('nodes.json', 'r')
    nodes= json.load(reader)
    length = len(nodes)
    for i in range(length):
        for j in range(2):
            nodes[i]['x'] += dif[ nodes[i]['group'] ][0]
            nodes[i]['y'] += dif[ nodes[i]['group'] ][1]

    f = open('PRISM_nodes.json', 'w')
    json.dump(nodes, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))



if __name__ == '__main__':
    width = 900
    height = 600
    center = []
    links = []
    boxes = []
    makeData(center, links,boxes)
    import pylab as pl
    pl.xticks([0, width])
    pl.yticks([0, height])
    checkPRISM(center, links, boxes)
    checkAll(center, boxes)

    import pylab as pl
    pl.xticks([0, width])
    pl.yticks([0, height])
    for i in center:
        # if i[2] == 15:
        pl.gca().add_patch( pl.Rectangle(xy=[i[0]-i[2], height - i[1]-i[3]], width=i[2]*2, height=i[3]*2, linewidth='1.0', fill=False) )
    pl.show()
