import os
import json
from setAnswer import calc

def arrange():
    pathes = []
    pathes.append('../data/FDGIB/comp/')
    # pathes.append('../data/TRGIB/comp/')
    # pathes.append('../data/Chaturvedi/comp/')
    # pathes.append('../data/STGIB/comp/')

    for output in pathes:
        if os.path.exists(output) != True:
            os.mkdir(output)

    count = 0
    num = 0

    for path in pathes:
        while count < 1600:
            if os.path.exists(path + str(num) + '.json'):
                count += 1
            else:
                print(num)
            num += 1
            if count != 0 and count % 50 == 0:
                num = 60 * (floor( num / 60) + 1)

    

def main():
    arrange()

if __name__ == '__main__':
    main()
