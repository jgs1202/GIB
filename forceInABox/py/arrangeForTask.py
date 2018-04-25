import os
import json
from setAnswer import calc

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

    order = 0
    num = 0

    for i in inputPath:
        for dir in os.listdir(i):
            if dir != '.DS_Store':
                for file in os.listdir(i + dir):
                    print(dir, file)
                    order = order % 4
                    data = json.load( open(i + dir + '/' + file, 'r') )
                    data = calc(data)
                    data['type'] = i[8:13]
                    f = open( outputPath[order] + str(num) + '.json', 'w')
                    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
                    order += 1
                    if order > 3:
                        num += 1

def main():
    arrange()

if __name__ == '__main__':
    main()
