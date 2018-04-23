import random
from operator import itemgetter
import json
import os
import sys

def makeData():
    eachNum = 10

    mset = [12, 15, 18]
    nmin = 10
    nmax = 30
    pin = 0.2
    pbridge = 0.05
    pgroupset = [0, 0.05, 0.1, 0.2]
    poutset = [0, 0.0005, 0.001]

    total = len(mset) * len(pgroupset) * len(poutset)

    for i in range(total):
        for each in range(eachNum):
            verify = False
            while verify == False:
                if each == 0:
                    m = mset[ int( i /( len(pgroupset) * len(poutset)) ) ]
                    pout = poutset[ i % len(poutset) ]
                    pgroup = pgroupset[ (int( i / len(poutset) )) % len(pgroupset) ]
                    print(m, pgroup, pout)

                if pgroup != 0 or pout != 0:

                    nodes = []
                    for i in range(m):
                        nodes.append([])

                    num = 0
                    for i in range(m):
                        rand = random.randint(nmin, nmax)
                        for j in range(rand):
                            nodes[i].append(num)
                            num += 1

                    links = []
                    total = 0
                    for i in range(m):
                        # links.append([])
                        length = len (nodes[i])
                        total += len(nodes[i])
                        for j in range( length ):
                            for k in range( length - j - 1):
                                if random.random() < pin:
                                    dic = {}
                                    dic['source'] = nodes[i][j]
                                    dic['target'] = nodes[i][j+k+1]
                                    dic['value'] = 1
                                    links.append(dic)

                    # print(nodes)

                    for i in range(m):
                        length1 = len (nodes)
                        length2 = len(nodes[i])
                        for j in range( length1 - i -1 ):
                            if random.random() < pgroup:
                                length3 = len(nodes[i+j+1])
                                for k in range( length2 ):
                                    for l in range(length3):
                                        if random.random() < pbridge:
                                            dic = {}
                                            dic['source'] = nodes[i][k]
                                            dic['target'] = nodes[i+j+1][l]
                                            dic['value'] = 1
                                            links.append(dic)


                    for i in range(m):
                        links.sort(key=itemgetter('source'))

                    # print(links)
                    # print(len(links))

                    current = 0
                    for i in range(total):
                        for j in range(total - i - 1):
                            if current == len(links):
                                break
                            elif links[current]['source'] == i and links[current]['target'] == i+j+1:
                                current += 1
                            else:
                                if random.random() < pout:
                                    dic = {}
                                    dic['source'] = i
                                    dic['target'] = i+j+1
                                    dic['value'] = 1
                                    links.append( dic )
                                    current += 1

                    # print(len(nodes))

                    nodes_for_write = []
                    length = len(nodes)
                    for i in range(length):
                        lengthG = len(nodes[i])
                        for j in range(lengthG):
                            dic = {}
                            dic['index'] = nodes[i][j]
                            dic['group'] = i
                            nodes_for_write.append(dic)

                    data = {}
                    data['groupSize'] = m
                    data['pgroup'] = pgroup
                    data['pout'] = pout
                    data['nodes'] = nodes_for_write
                    data['links'] = links
                    data['file'] = str(each) +'.json'
                    data['dir'] = str(m) + '-' + str(pgroup) + '-' + str(pout)

                    calc(data, m)


                    try:
                        dir =  os.listdir('../data/origin/' + str(m) + '-' + str(pgroup) + '-' + str(pout))
                    except:
                        os.mkdir('../data/origin/' + str(m) + '-' + str(pgroup) + '-' + str(pout))

                    if len(data['mostConnected']) == 1:
                        verify = True
                        print(each)
                        f = open('../data/origin/' + str(m) + '-' + str(pgroup) + '-' + str(pout) + '/' + str(each) + '.json', 'w')
                        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

                    else:
                        print('minus')
                # f = open('../data/links.json', 'w')
                # json.dump(links, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

def calc(data, m):
    max = 0
    for i in data['nodes']:
        if i['group'] > max:
            max = i['group']
    boxNum = max + 1
    linkNum = []
    for i in range(boxNum):
        linkNum.append([])
        for j in range(boxNum - i):
            linkNum[i].append(0)
    # print(linkNum)

    links = data['links']
    # print(len(links))
    for i in links:
        # print(i)
        source = data['nodes'][i['source']]['group']
        target = data['nodes'][i['target']]['group']
        if source != target:

            if source < target:
                if linkNum[source][target-source]  == 0:
                    linkNum[source][target-source] = 1
                else:
                    linkNum[source][target-source] += 1
            else:
                if linkNum[target][source-target]  == 0:
                    linkNum[target][source-target] = 1
                else:
                    linkNum[target][source-target] += 1

    max = linkNum[0][0]
    most = []
    for i in range(len(linkNum)):
        for j in range(len(linkNum[i])):
            if linkNum[i][j] > max:
                most = [[i, i+j]]
                max = linkNum[i][j]
            elif linkNum[i][j] == max:
                most.append([i,i+j])

    # print(most)
    data['mostConnected'] = most

    linkGroup = [ [i, 0] for i in range(m) ]
    nodeGroup = [ [i, 0] for i in range(m) ]
    for i in data['nodes']:
        nodeGroup[i['group']][1] += 1
    for i in data['links']:
        srcGroup = data['nodes'][i['source']]['group']
        tarGroup = data['nodes'][i['target']]['group']
        if srcGroup == tarGroup:
            linkGroup[srcGroup][1] += 1
    linkGroup.sort(key=itemgetter(1), reverse=True)
    nodeGroup.sort(key=itemgetter(1), reverse=True)
    data['nodeMax'] = nodeGroup[2][0]
    data['nodeMin'] = nodeGroup[-3][0]
    data['linkMax'] = linkGroup[2][0]
    data['linkMin'] = linkGroup[-3][0]

if __name__ == '__main__':
    makeData()
