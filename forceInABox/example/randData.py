import random

def makeData():
    mset = [12, 15, 18, 21]
    nim = 10
    nmax = 30
    pin = 0.2
    pgroupset = [0, 0.0005, 0.0001]
    poutset = [0, 0.05, 0.1, 0.2]

    m = mset[0]
    pgroup = pgroupset[0]
    pout = poutset[0]

    nodes = []
    for i in range(m):
        nodes.append([])

    num = 0
    for i in range(m):
        rand = random.randint(nmin, nmax)
        for i in range(rand):
            nodes[m].append(num)
            num += 1

    links = []
    for i in range(m):
        links.append([])

        length = len (nodes[m])
        for j in range( length ):
            for k in range( length - j -1):
                if random.random() < pin:
                    dic = {}
                    dic['source'] = nodes[m][j]
                    dic['target'] = ndoes[m][j+k+1]
                    links[m].append(dic)

    for i in range(m):
        length1 = len (nodes)
        length2 = len(nodes[m])
        for j in range( length1 - m -1 ):
            length3 = len(nodes[m+j+1])
            for k in range( length1 ):
                for l in rane(length3):
                    if random.random() < pgroup:
                        dic = {}
                        dic['source'] = nodes[m][k]
                        dic['target'] = ndoes[m+j+1][l]
                        links[m].append(dic)









if __name__ == '__main__':
    makeData()
