# -*- coding: utf-8 -*-
import random
from operator import itemgetter
import json
import os
import sys
import numpy as np


def makeData():
    eachNum = 500
    # mset = [8, 11, 14, 17]
    m = 11
    pinset = [0.1, 0.2, 0.25, 0.3, 0.35]
    pinset = [0.286, 0.287]
    # pin = [0.1]
    pbridge = 0.05
    pgroup = 0
    pout = 0
    total = len(pinset)
    name = 0
    output = []

    # pin *= thre
    # pbridge *= thre

    for i in range(total):
        print('step = ' + str(i))
        for each in range(eachNum):
            if each == 0:
                pin = pinset[i]
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

            data = {}
            data['groupSize'] = m
            data['pin'] = pin
            data['pgroup'] = pgroup
            data['pout'] = pout
            data['linkSize'] = len(links)
            data['nodeSize'] = len(nodes_for_write)
            data['file'] = str(name) +'.json'
            data['dir'] = str(m) + '-' + str(pgroup) + '-' + str(pout)
            output.append(data)

    out = []
    datum = {}
    print(len(output))
    for i in range(len(output)):
        if i % eachNum == 0:
            print(output[i]['pgroup'], output[i]['pout'])
            try:
                datum['groupSize'] /= eachNum
                datum['linkSize'] /= eachNum
                datum['nodeSize'] /= eachNum
                out.append(datum)
                datum = {}
            except:
                pass
            datum['groupSize'] = output[i]['groupSize']
            datum['pin'] = output[i]['pin']
            datum['pgroup'] = output[i]['pgroup']
            datum['pout'] = output[i]['pout']
            datum['linkSize'] = output[i]['linkSize']
            datum['nodeSize'] = output[i]['nodeSize']
        else:
            datum['groupSize'] += output[i]['groupSize']
            datum['linkSize'] += output[i]['linkSize']
            datum['nodeSize'] += output[i]['nodeSize']
    datum['groupSize'] /= eachNum
    datum['linkSize'] /= eachNum
    datum['nodeSize'] /= eachNum
    out.append(datum)
    print(out)

    outjson = {'data': out}
    f = open('../data/pin2.json', 'w')
    json.dump(outjson, f, ensure_ascii=False, indent=4, sort_keys=True, separators= (',', ': '))


if __name__ == '__main__':
    makeData()
    cmds = [ 'python STGIB.py', 'python Chaturvedi.py', 'python groupWeight.py']
    for i in cmds:
        cmd = i
    os.system(cmd)
