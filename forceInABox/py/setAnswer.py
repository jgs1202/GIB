import json
import os
import sys

def calc(data):
    boxNum = data['groupSize']
    linkNum = []
    for i in range(boxNum):
        linkNum.append([])
        for j in range(boxNum - i):
            linkNum[i].append(0)

####################### link outside most ##########################
    links = data['links']
    linkNum = [ 0 for i in range(boxNum)]
    for i in links:
        source = data['nodes'][i['source']]['group']
        target = data['nodes'][i['target']]['group']
        if source != target:
            linkNum[source] += 1
            linkNum[target] += 1
    maxNum = max(linkNum)
    linkOutMost = []
    for i in range(boxNum):
        if linkNum[i] == maxNum:
            linkOutMost.append(i)
    # print(linkNum, linkOutMost)
    data['linkOutMost'] = linkOutMost

    return data

def main():
    main = '../data/origin/'
    for dir in os.listdir(main):
        if (dir != '.DS_Store'):
            # try:
            for file in os.listdir(main + dir):
                # print(file)
                # dir = "18-0.0005-0.05"
                if (dir != '.DS_Store'):
                    print(dir, file)
                    f = open(main + dir + '/' + file, 'r')
                    data = json.load(f)
                    f.close()
                    data = calc(data)
                    f = open(main + dir + '/' + file, 'w')
                    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
                    # sys.exit()


if __name__ == '__main__':
    main()
