# -*- coding: utf-8 -*-

import os
import json
import sys

argvs = sys.argv
if len(argvs) != 2:
    print('ERROR : You must give 2 arguments.')
    sys.exit()
main = '../data/' + argvs[1] + '/temp/'
output = '../data/' + argvs[1] +'/comp/'


inp = input('Are you really run this program? This can damage your data. (y/n) :')
if inp == 'y':
    for dir in os.listdir(main):
        if dir != '.DS_Store':
            print(dir)
            # if dir != '12-0-0.0005':
            for dataNum in range(10):
                minus = False
                f = open(main + dir + '/' + str(dataNum) + '-nodes.txt')
                txt = f.read()
                reader = open(main + dir + '/' + str(dataNum) + '.json')
                global data
                data = json.load(reader)

                length = len(data['nodes'])
                list = [i for i in range(length)]
                sentence = ''
                num = 0
                index = 0
                # print(dir, num)
                for i in txt:
                    try:
                        i = int(i)
                    except:
                        pass
                    if type(i) == int:
                        sentence += (str(int(i)))
                    else:
                        if i == '.':
                            sentence = sentence + '.'
                        elif i == '-':
                            minus = True
                            break
                        else:
                            if num == 0:
                                global dic
                                dic = {}
                                dic['cx'] = float(sentence)
                                sentence = ''
                                num += 1
                            elif num == 1:
                                dic['cy'] = float(sentence)
                                # dic['index'] = index
                                sentence = ''
                                num = 0
                                list[index] = dic
                                index += 1
                            else:
                                print(error)
                if minus:
                    print('break')

                else:
                    for i in range(length):
                        data['nodes'][i]['cx'] = list[data['nodes'][i]['index']]['cx']
                        data['nodes'][i]['cy'] = list[data['nodes'][i]['index']]['cy']
                    data['layout'] = argvs[1]

                    try:
                        current = os.listdir(output + dir)
                    except:
                        os.mkdir(output + dir)
                    f = open(output + dir + '/' + str(dataNum) + '.json' , 'w')
                    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
else:
    pass
