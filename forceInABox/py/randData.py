import random
from operator import itemgetter
import json
import os

def makeData():
    eachNum = 20

    mset = [12, 15, 18, 21]
    nmin = 10
    nmax = 30
    pin = 0.2
    pgroupset = [0, 0.0005, 0.0001]
    poutset = [0, 0.05, 0.1, 0.2]

    total = len(mset) * len(pgroupset) * len(poutset)
    print(total)

    for i in range(total):
        for each in range(eachNum):

            if each == 0:
                m = mset[ int( i /( len(pgroupset) * len(poutset)) ) ]
                pout = poutset[ i % len(poutset) ]
                pgroup = pgroupset[ (int( i / len(poutset) )) % len(pgroupset) ]
                print(m, pgroup, pout)

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
                    length3 = len(nodes[i+j+1])
                    for k in range( length2 ):
                        for l in range(length3):
                            if random.random() < pgroup:
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
            data['nodes'] = nodes_for_write
            data['links'] = links

            try:
                dir =  os.listdir('../data/origin/' + str(m) + '-' + str(pgroup) + '-' + str(pout))
            except:
                os.mkdir('../data/origin/' + str(m) + '-' + str(pgroup) + '-' + str(pout))

            f = open('../data/origin/' + str(m) + '-' + str(pgroup) + '-' + str(pout) + '/' + str(each) + '.json', 'w')
            json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
            # f = open('../data/links.json', 'w')
            # json.dump(links, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    makeData()
