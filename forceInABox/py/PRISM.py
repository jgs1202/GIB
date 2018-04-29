# -*- coding: utf-8 -*-

# size is 900*600

import csv
import os
import copy
import json
import math
import numpy as np
import matplotlib.pyplot as plt
import sys
import decimal

def makeData(center, links, boxes, data):
    # print(data['links'])
    for i in data['boxes']:
        list = []
        list.extend([ i['one'], i['two'], i['three'], i['four'] ])
        boxes.append(list)
    # print(len(data['boxes']))
    linkWeights = []
    f = open('../data/origin-group-link/weight/' + data['file'][:-5] + '.csv', 'r')
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
    oldcenter = copy.deepcopy(center)
    t = []
    num = 0
    while num < 1000 and int(t.count(1.0)) != int(len(links)):
        t = []
        which = []
        ex = 0
        exex = 0
        length = len(links)
        excenter = copy.deepcopy(center)
        for i in range(length):
            t.append(1.0)

        # center[5][2] = 800
        # print(center)

        for i in range(length):
            dic = {}
            # print(len(center), links[i]['node2'])
            if center[links[i]['node1']][0] != center[links[i]['node2']][0]:
                xover = ( center[links[i]['node1']][2] + center[links[i]['node2']][2] +5) / ( abs( center[links[i]['node1']][0] - center[links[i]['node2']][0]) )
            else:
                xover = float('inf')
            if center[links[i]['node1']][1] != center[links[i]['node2']][1]:
                yover = ( center[links[i]['node1']][3] + center[links[i]['node2']][3] +5) / ( abs( center[links[i]['node1']][1] - center[links[i]['node2']][1]) )
            else:
                yover = float("inf")
            # print(xover, center[links[i]['node1']][2], center[links[i]['node2']][2] ,center[links[i]['node1']][0] , center[links[i]['node2']][0])
            # print(xover, yover)
            if xover < yover:
                dic['key'] = 'x'
                dic['value'] = xover
            else:
                dic['key'] = 'y'
                dic['value'] = yover
            if dic['value'] > 1.0:
                t[i] = dic['value']
                if dic['key']=='y' and ex=='y':
                    dic['key'] = 'x'
                elif dic['key']=='x' and ex=='x' and exex=='x':
                    dic['ey'] = 'y'
                exex = ex
                ex = dic['key']
            else:
                t[i] = 1.0
            if t[i] > 1.5:
                t[i] = 1.5
            which.append(dic)

        for i in range(length):
            if t[i]>1.0:
                # print('ex')
                # print(center[links[i]['node1']])
                # print(center[links[i]['node2']])

                dis1 = math.sqrt( math.pow((center[links[i]['node1']][0] - width/2), 2) + math.pow((center[links[i]['node1']][1] - height/2), 2) )
                dis2 = math.sqrt( math.pow((center[links[i]['node2']][0] - width/2), 2) + math.pow((center[links[i]['node2']][1] - height/2), 2) )
                # print(dis1, dis2)
                # print(which['key'])
                if which[i]['key'] == 'x':
                    # print('xmove')
                    if dis1 > dis2: #which group should we move
                        if center[links[i]['node1']][0] < center[links[i]['node2']][0]: #which direction should we move to
                            # print('1')
                            center[links[i]['node1']][0] = center[links[i]['node2']][0] -  center[links[i]['node1']][2] - center[links[i]['node2']][2] - 10
                        else:
                            # print('2')
                            center[links[i]['node1']][0] = center[links[i]['node2']][0] + center[links[i]['node1']][2] + center[links[i]['node2']][2] + 10
                    else:
                        if center[links[i]['node2']][0] < center[links[i]['node1']][0]: #which direction should we move to
                            # print('3')
                            center[links[i]['node2']][0] = center[links[i]['node1']][0] -  center[links[i]['node1']][2] - center[links[i]['node2']][2] - 10
                        else:
                            # print('4')
                            center[links[i]['node2']][0] = center[links[i]['node1']][0] + center[links[i]['node1']][2] + center[links[i]['node2']][2] + 10
                elif which[i]['key'] == 'y':
                    # print('ymove')
                    if dis1 > dis2: #which group should we move
                        if center[links[i]['node1']][1] < center[links[i]['node2']][1]: #which direction should we move to
                            # print('5')
                            center[links[i]['node1']][1] = center[links[i]['node2']][1] -  center[links[i]['node1']][3] - center[links[i]['node2']][3] - 10
                        else:
                            # print('6')
                            center[links[i]['node1']][1] = center[links[i]['node2']][1] + center[links[i]['node1']][3] + center[links[i]['node2']][3] + 10
                    else:
                        if center[links[i]['node2']][1] < center[links[i]['node1']][1]: #which direction should we move to
                            # print('7')
                            center[links[i]['node2']][1] = center[links[i]['node1']][1] -  center[links[i]['node1']][3] - center[links[i]['node2']][3] - 10
                        else:
                            # print('8')
                            center[links[i]['node2']][1] = center[links[i]['node1']][1] + center[links[i]['node1']][3] + center[links[i]['node2']][3] + 10
                # print('new')
                # print(center[links[i]['node1']])
                # print(center[links[i]['node2']])

        # print( 'num is ' + str(num))
        # print(t)
        # for i in range(10):
        #     print(str(center[i][0] - excenter[i][0]) + ', ' + str(center[i][1] - excenter[i][1]))
        # print('the number of t is ' + str(t.count(1.0)))
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


def checkAll(center, boxes, data):
    oldcenter = copy.deepcopy(center)
    links = []
    ex = 0
    exex =0
    # set viutual links
    length  = len(boxes)
    for i in range(length):
        for j in range(1,length - i):
            dic = {}
            dic['node1'] = i
            dic['node2'] = i + j
            links.append(dic)
    # print(links)

    t = []
    num = 0
    double = 0
    while num < 1000 and double != 2:
        t = []
        which = []
        ex=0
        exex= 0
        length = len(links)
        excenter = copy.deepcopy(center)
        for i in range(length):
            t.append(1.0)

        # center[5][2] = 800
        # print(center)

        for i in range(length):
            dic = {}
            if center[links[i]['node1']][0] != center[links[i]['node2']][0]:
                xover = ( center[links[i]['node1']][2] + center[links[i]['node2']][2] +5) / ( abs( center[links[i]['node1']][0] - center[links[i]['node2']][0]) )
            else:
                xover = float('inf')
            if center[links[i]['node1']][1] != center[links[i]['node2']][1]:
                yover = ( center[links[i]['node1']][3] + center[links[i]['node2']][3] +5) / ( abs( center[links[i]['node1']][1] - center[links[i]['node2']][1]) )
            else:
                yover = float("inf")
            # xover = ( center[links[i]['node1']][2] + center[links[i]['node2']][2]+5) / ( abs( center[int(links[i]['node1'])][0] - center[int(links[i]['node2'])][0]) )
            # yover = ( center[links[i]['node1']][3] + center[links[i]['node2']][3]+5) / ( abs( center[links[i]['node1']][1] - center[links[i]['node2']][1]) )
            # print(xover, center[links[i]['node1']][2], center[links[i]['node2']][2] ,center[links[i]['node1']][0] , center[links[i]['node2']][0])
            # print(xover, yover)
            if xover < yover:
                dic['key'] = 'x'
                dic['value'] = xover
            else:
                dic['key'] = 'y'
                dic['value'] = yover
            # if xover < yover:
            #     if ex!='x' or exex!='x':
            #         which['key'] = 'x'
            #         which['value'] = xover
            #         exex = ex
            #         ex = 'x'
            #     else:
            #         exex = ex
            #         ex = 'y'
            #         which['key'] = 'y'
            #         which['value'] = yover
            # else:
            #     if ex != 'y':
            #         exex = ex
            #         ex = 'y'
            #         which['key'] = 'y'
            #         which['value'] = yover
            #     else:
            #         which['key'] = 'x'
            #         which['value'] = xover
            #         exex = ex
            #         ex = 'x'
            if dic['value'] > 1.0:
                t[i] = dic['value']
                if dic['key']=='y' and ex=='y':
                    dic['key'] = 'x'
                elif dic['key']=='x' and ex=='x' and exex=='x':
                    dic['ey'] = 'y'
                exex = ex
                ex = dic['key']
            else:
                t[i] = 1.0
            if t[i] > 1.5:
                t[i] = 1.5
            which.append(dic)

        for i in range(length):
            if t[i]>1.0:
                # print('ex')
                # print(center[links[i]['node1']])
                # print(center[links[i]['node2']])

                dis1 = math.sqrt( math.pow((center[links[i]['node1']][0] - width/2), 2) + math.pow((center[links[i]['node1']][1] - height/2), 2) )
                dis2 = math.sqrt( math.pow((center[links[i]['node2']][0] - width/2), 2) + math.pow((center[links[i]['node2']][1] - height/2), 2) )
                # print(dis1, dis2)
                # print(which['key'])
                if which[i]['key'] == 'x':
                    # print('xmove')
                    if dis1 > dis2: #which group should we move
                        if center[links[i]['node1']][0] < center[links[i]['node2']][0]: #which direction should we move to
                            # print('1')
                            center[links[i]['node1']][0] = center[links[i]['node2']][0] -  center[links[i]['node1']][2] - center[links[i]['node2']][2] - 10
                        else:
                            # print('2')
                            center[links[i]['node1']][0] = center[links[i]['node2']][0] + center[links[i]['node1']][2] + center[links[i]['node2']][2] + 10
                    else:
                        if center[links[i]['node2']][0] < center[links[i]['node1']][0]: #which direction should we move to
                            # print('3')
                            center[links[i]['node2']][0] = center[links[i]['node1']][0] -  center[links[i]['node1']][2] - center[links[i]['node2']][2] - 10
                        else:
                            # print('4')
                            center[links[i]['node2']][0] = center[links[i]['node1']][0] + center[links[i]['node1']][2] + center[links[i]['node2']][2] + 10
                elif which[i]['key'] == 'y':
                    # print('ymove')
                    if dis1 > dis2: #which group should we move
                        if center[links[i]['node1']][1] < center[links[i]['node2']][1]: #which direction should we move to
                            # print('5')
                            center[links[i]['node1']][1] = center[links[i]['node2']][1] -  center[links[i]['node1']][3] - center[links[i]['node2']][3] - 10
                        else:
                            # print('6')
                            center[links[i]['node1']][1] = center[links[i]['node2']][1] + center[links[i]['node1']][3] + center[links[i]['node2']][3] + 10
                    else:
                        if center[links[i]['node2']][1] < center[links[i]['node1']][1]: #which direction should we move to
                            # print('7')
                            center[links[i]['node2']][1] = center[links[i]['node1']][1] -  center[links[i]['node1']][3] - center[links[i]['node2']][3] - 10
                        else:
                            # print('8')
                            center[links[i]['node2']][1] = center[links[i]['node1']][1] + center[links[i]['node1']][3] + center[links[i]['node2']][3] + 10
                # print('new')
                # print(center[links[i]['node1']])
                # print(center[links[i]['node2']])

        # print( 'num is ' + str(num))
        # print(t)
        # for i in range(10):
        #     print(str(center[i][0] - excenter[i][0]) + ', ' + str(center[i][1] - excenter[i][1]))
        # print('the number of t is ' + str(t.count(1.0)))
        if int(t.count(1.0)) == int(len(links)):
            double += 1
        else:
            double = 0
        num += 1
    # print(num)
    # with open('PRISM_boxes.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     for i in center:
    #         writer.writerow(i)

    if num != 1000:

        length1 = len(center)
        dif = []
        for i in range(length1):
            dif.append([])
        for i in range(length1):
            length2 = len(center[i])
            for j in range(length2) :
                dif[i].append( center[i][j] - oldcenter[i][j] )
        length = len(data['nodes'])
        for i in range(length):
            for j in range(2):
                data['nodes'][i]['x'] += dif[ data['nodes'][i]['group'] ][0]
                data['nodes'][i]['y'] += dif[ data['nodes'][i]['group'] ][1]

        boxesCoo = []
        for i in center:
            dic = {}
            dic['x'] = i[0]-i[2]
            dic['y'] = i[1]-i[3]
            dic['dx'] = i[2]*2
            dic['dy'] = i[3]*2
            boxesCoo.append(dic)
        dic = {}
        dic['x'] = 0
        dic['y'] = 0
        dic['dx'] = width
        dic['dy'] = height
        boxesCoo.append(dic)
        data['groups'] = boxesCoo
        data['layout'] = 'FDGIB'
        del data['boxes']

        f = open(out + str(data['file']), 'w')
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

        # import pylab as pl
        # pl.xticks([0, width])
        # pl.yticks([0, height])
        # for i in center:
        #     # if i[2] == 15:
        #     pl.gca().add_patch( pl.Rectangle(xy=[i[0]-i[2], height - i[1]-i[3]], width=i[2]*2, height=i[3]*2, linewidth='1.0', fill=False) )
        # pl.show()



def main(data, out):
    center = []
    links = []
    boxes = []
    makeData(center, links, boxes, data)
    checkPRISM(center, links, boxes)
    checkAll(center, boxes, data)

if __name__ == '__main__':
    global width
    global height
    width = 1620.7
    height = 1000
    reader = open('../mock/fdData.json', 'r')
    data = json.load(reader)
    for i in data['coordinates']:
        if i['id'] != 1:
            # if i['dir'] == './12-0.0005-0.05/':
            out = '../data/FDGIB/temp/'
            print(i['file'])
            try:
                a = os.listdir(out)
            except:
                os.mkdir(out)
            main(i, out)
            # sys.exit()
    cmd = 'python resize.py'
    os.system(cmd)
