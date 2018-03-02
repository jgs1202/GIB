# -*- coding: utf-8 -*-

# size is 900*600

import csv

def makeData(center, links, boxes):
    f = open('boxes.csv', 'r')
    reader1 = csv.reader(f)
    for i in reader1:
        boxes.append(i)
    print(boxes)

    linkWeights = []
    f = open('link_boxes.csv', 'r')
    reader2 = csv.reader(f)
    for i in reader2:
        linkWeights.append(i)
    print(linkWeights)

    # center = [] # cx, cy, dirx, diry
    lengthBox = len(boxes)
    for i in range(lengthBox):
        dirx = ( float(boxes[i][3]) - float(boxes[i][2]) )/2
        diry = ( float(boxes[i][1]) - float(boxes[i][0])) /2
        center.append( [ float(boxes[i][2]) + dirx , float(boxes[i][0]) + diry, dirx, diry])

    # links = []
    num1 = len(linkWeights)
    for i in range(num1):
        num2 = len(linkWeights[i])
        for j in range(num2):
            if float(linkWeights[i][j]) != 0.0:
                dic = {}
                dic['node1'] = i
                dic['node2'] = j
                links.append(dic)

if __name__ == '__main__':
    center = [], links = [], boxes=[]
    makeData(center, links, boxes)
    print(center)
    print(links)
