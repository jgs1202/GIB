import os
import json
from setAnswer import calc
import random

def arrange():
    inputPath = []
    inputPath.append('../data/Chaturvedi/comp/')
    inputPath.append('../data/STGIB/comp/')
    inputPath.append('../data/FDGIB/comp/')
    inputPath.append('../data/TRGIB/comp/')

    outputPath = []
    outputPath.append('../data/experiment/task1/')
    outputPath.append('../data/experiment/task2/')
    outputPath.append('../data/experiment/task3/')
    outputPath.append('../data/experiment/task4/')

    for output in outputPath:
        if os.path.exists(output) != True:
            os.mkdir(output)

    order = 0
    total = 0
    outData = [[] for i in range(4)]

    for i in inputPath:
        num = 0
        for dir in os.listdir(i):
            if dir != '.DS_Store':
                # for file in os.listdir(i + dir):
                #     print(dir, file)
                order = order % 4
                data = json.load(open(i + dir, 'r'))
                data = calc(data)
                data['type'] = i[8:13]
                outData[order].append(data)
                # f = open( outputPath[order] + str(num) + '.json',  'w')
                # json.dumppytho(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
                order += 1
                num += 1
            if num == 120:
                print(num)
                break
    print(len(outData[0]))
    for num in range(4):
        orders = [i for i in range(120)]
        if num == 1 or num == 4:
            random.shuffle(orders)
        else:
            early = []
            later = []
            unit = 0
            for i in range(4):
                early.extend(orders[unit:unit + 15])
                later.extend(orders[unit + 15:unit + 30])
                unit += 30
            random.shuffle(early)
            random.shuffle(later)
            orders = early
            orders.extend(later)
        # print(len(orders))
        for i in range(120):
            f = open(outputPath[num] + str(orders[i]) + '.json', 'w')
            outData[num][i]['file'] = str(orders[i]) + '.json'
            json.dump(outData[num][i], f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
            f.close()




def main():
    arrange()

if __name__ == '__main__':
    main()
