import random
from operator import itemgetter
import json
import os
import sys
import numpy as np

def makeData():
    eachNum = 50
    mset = [12, 15, 18]
    thre = 0.2
    nodeThre = 0.7
    nmin = 10
    nmax = 30
    pin = 0.2
    pbridge = 0.05
    # pgroupset = [ 0, 0.05, 0.1, 0.2]
    pgroup = 0.1
    # poutset = [0, 0.001, 0.002]
    pout = 0.002

    pin = pin * thre
    pbridge = round(pbridge * thre, 4)
    # pgroup = round(pgroup * thre, 3)
    pout = round(pout * thre, 5)


    ############## normal distribution #####################
    muGroup, sigmaGroup = 11.4, 5.4
    muSize, sigmaSize = 52.5, 35.3
    s1 = np.random.normal(muGroup, sigmaGroup, 2)
    s2 = np.random.normal(muSize, sigmaSize, 2)

    # total = len(mset) * len(pgroupset) * len(poutset)
    total = 4

    for i in range(total):
        print('step = ' + str(i))
        for each in range(eachNum):
            verify = False
            while verify == False:
                # if each == 0:
                    # m = mset[ int( i /( len(pgroupset) * len(poutset)) ) ]
                    # pout = poutset[ i % len(poutset) ]
                    # pgroup = pgroupset[ (int( i / len(poutset) )) % len(pgroupset) ]
                m = 0
                while m < 6 or m > 17:
                    m = np.random.normal(11.4, 5.4, 1)
                    m = round(m[0]).astype(np.int32)
                if pgroup == 0 and pout == 0:
                    verify = True
                elif pgroup != 0 or pout != 0:
                    nodes = []
                    for l in range(m):
                        nodes.append([])

                    num = 0
                    for l in range(m):
                        # rand = random.randint(nmin, nmax)
                        rand = np.random.normal(52.5, 35.3, 1)
                        rand = round(rand[0]).astype(np.int32)
                        if rand < 4:
                            rand = 4
                        rand *= nodeThre
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
                        # links.append([])
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

                    # print(nodes)
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

                    # print(links)
                    # print(len(links))

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

                    # print(len(nodes))

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
                    data['pgroup'] = pgroup
                    data['pout'] = pout
                    data['nodes'] = nodes_for_write
                    data['links'] = links
                    data['file'] = str(each) +'.json'
                    data['dir'] = str(m) + '-' + str(pgroup) + '-' + str(pout)

                    calc(data, m)

                    # try:
                    #     dir =  os.listdir('../data/origin/' + str(11.4) + '-' + str(pgroup) + '-' + str(pout))
                    # except:
                    #     os.mkdir('../data/origin/' + str(11.4) + '-' + str(pgroup) + '-' + str(pout))

                    if len(data['mostConnected']) == 1:
                        try:
                            a=data['nodeMax']
                            # print('nodeMax')
                            a=data['nodeMin']
                            # print('nodeMin')
                            a=data['linkMax']
                            # print('linkMax')
                            a=data['linkMin']
                            # print('linkMin')
                            verify = True
                            # print(each)
                            # f = open('../data/origin/' + str(11.4) + '-' + str(pgroup) + '-' + str(pout) + '/' + str(each) + '.json', 'w')
                            f = open('../data/origin/' + output[i] +'/' + str(each) + '.json', 'w')
                            intM = 0
                            for p in range(m+1):
                                if p == m:
                                    intM = p
                            # print( len(data['nodes']), len(data['links']))
                            data['groupSize'] = intM
                            json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
                        except:
                            pass

                    else:
                        pass
                        # print(data['mostConnected'])
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
    if nodeGroup[0][1] > nodeGroup[1][1]:
        data['nodeMax'] = nodeGroup[1][0]
    if nodeGroup[-1][1] < nodeGroup[-2][1]:
        data['nodeMin'] = nodeGroup[-1][0]
    if linkGroup[0][1] > linkGroup[1][1]:
        data['linkMax'] = linkGroup[0][0]
    if linkGroup[-1][1] < linkGroup[-2][1]:
        data['linkMin'] = linkGroup[-1][0]
    # print(linkGroup[0][0], data['linkMax'])
    # sys.exit()

if __name__ == '__main__':
    makeData()
    cmds = [ 'python STGIB.py', 'python Chaturvedi.py']
    for i in cmds:
        cmd = i
    os.system(cmd)
