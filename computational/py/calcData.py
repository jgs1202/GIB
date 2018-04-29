# -*- coding: utf-8 -*-
import random
from operator import itemgetter
import json
import os
import sys
import csv
import numpy as np

def makeData():
    eachNum = 5
    mset = [8, 11, 14, 17]
    thre = 0.1
    pin = 0.2
    pbridge = 0.05
    pgroupset = [ 0, 0.05, 0.1, 0.2]
    poutset = [0, 0.001, 0.002]
    total = len(mset) * len(pgroupset) * len(poutset)
    name = 0
    outputdata = [ ["id", "groupSize", "linkSize", "nodeSize"] ]

    for i in range(total):
        print('step = ' + str(i))
        for each in range(eachNum):
            if each == 0:
                m = mset[ int( i /( len(pgroupset) * len(poutset)) ) ]
                pout = poutset[ i % len(poutset) ]

                pout *= thre
                pgroup = pgroupset[ (int( i / len(poutset) )) % len(pgroupset) ]
                print(m, pout, pgroup)
            if pgroup == 0 and pout == 0:
                verify = True
            elif pgroup != 0 or pout != 0:
                nodes = []
                for l in range(m):
                    nodes.append([])

                num = 0
                for l in range(m):
                    rand = np.random.normal(52.5, 35.3, 1)
                    rand = round(rand[0]).astype(np.int32)
                    if rand < 4:
                        rand = 4
                    try:
                        rand = round(rand).astype(np.int32)
                    except:
                        rand = int(rand)
                    for j in range(rand):
                        nodes[l].append(num)
                        num += 1

                links = []
                total = 0
                for l in range(m):
                    length = len (nodes[l])
                    total += len(nodes[l])
                    for j in range( length ):
                        for k in range( length - j - 1):
                            if random.random() < pin:
                                dic = {}
                                dic['source'] = nodes[l][j]
                                dic['target'] = nodes[l][j+k+1]
                                dic['value'] = 1
                                links.append(dic)

                for p in range(m):
                    length1 = len (nodes)
                    length2 = len(nodes[p])
                    for j in range( length1 - p -1 ):
                        if random.random() < pgroup:
                            length3 = len(nodes[p+j+1])
                            for k in range( length2 ):
                                for l in range(length3):
                                    if random.random() < pbridge:
                                        dic = {}
                                        dic['source'] = nodes[p][k]
                                        dic['target'] = nodes[p+j+1][l]
                                        dic['value'] = 1
                                        links.append(dic)


                for p in range(m):
                    links.sort(key=itemgetter('source'))

                current = 0
                for p in range(total):
                    for j in range(total - p - 1):
                        if current == len(links):
                            break
                        elif links[current]['source'] == p and links[current]['target'] == p+j+1:
                            current += 1
                        else:
                            if random.random() < pout:
                                dic = {}
                                dic['source'] = p
                                dic['target'] = p+j+1
                                dic['value'] = 1
                                links.append( dic )
                                current += 1

                nodes_for_write = []
                length = len(nodes)
                for p in range(length):
                    lengthG = len(nodes[p])
                    for j in range(lengthG):
                        dic = {}
                        dic['name'] = nodes[p][j]
                        dic['group'] = p
                        nodes_for_write.append(dic)

                list = [ name, m, len(link), len(nodes)]

    with open('../data/' +'totalOfOriginData.csv', 'w') as f:
		writer = csv.writer(f)
        for row in list:
		    writer.writerow(row)



if __name__ == '__main__':
    makeData()
