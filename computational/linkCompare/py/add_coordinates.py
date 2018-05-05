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
main = []
output = []
layout = []
if argvs[1] == 'all':
    main.append('../data/STGIB/temp/')
    main.append('../data/Chaturvedi/temp/')
    main.append('../data/TRGIB/temp/')
    main.append('../data/FDGIB/temp/')
    output.append('../data/STGIB/comp/')
    output.append('../data/Chaturvedi/comp/')
    output.append('../data/TRGIB/comp/')
    output.append('../data/FDGIB/comp/')
    layout.append('STGIB')
    layout.append('Chaturvedi')
    layout.append('TRGIB')
    layout.append('FDGIB')
else:
    main.append('../data/' + argvs[1] + '/temp/')
    output.append('../data/' + argvs[1] +'/comp/')
    layout.append(argvs[1])

inp = input('Are you really run this program? This can damage your data. (y/n) :')
if inp == 'y':
    for dir in range(len(main)):
        for file in os.listdir(main[dir]):
        # for dataNum in range(10):
            if file[-5:] == '.json':
                print(main[dir], file)
                minus = False
                f = open(main[dir] + file[:-5] + '-nodes.txt')
                txt = f.read()
                reader = open(main[dir] + file)
                global data
                data = json.load(reader)

                length = len(data['nodes'])
                list = [i for i in range(length)]
                sentence = ''
                num = 0
                name = 0
                # print(main[dir], num)
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
                                # dic['name'] = name
                                sentence = ''
                                num = 0
                                list[name] = dic
                                name += 1
                            else:
                                print(error)
                if minus:
                    print('break')

                else:
                    for i in range(length):
                        # print(i, list[data['nodes'][int(i)]['name']])
                        data['nodes'][i]['cx'] = list[data['nodes'][i]['name']]['cx']
                        data['nodes'][i]['cy'] = list[data['nodes'][i]['name']]['cy']
                    data['layout'] = layout[dir]

                    try:
                        current = os.listdir(output[dir])
                    except:
                        os.mkdir(output[dir])
                    f = open(output[dir] + file , 'w')
                    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        # for dir in os.listdir(main):
        #     if dir != '.DS_Store':
        #         print(dir)
                # if dir != '12-0-0.0005':
                # for file in os.listdir(main + dir):
                # # for dataNum in range(10):
                #     if file[-5:] == '.json':
                #         minus = False
                #         f = open(main + dir + '/' + file[:-5] + '-nodes.txt')
                #         txt = f.read()
                #         reader = open(main + dir + '/' + file)
                #         global data
                #         data = json.load(reader)
                #
                #         length = len(data['nodes'])
                #         list = [i for i in range(length)]
                #         sentence = ''
                #         num = 0
                #         name = 0
                #         # print(dir, num)
                #         for i in txt:
                #             try:
                #                 i = int(i)
                #             except:
                #                 pass
                #             if type(i) == int:
                #                 sentence += (str(int(i)))
                #             else:
                #                 if i == '.':
                #                     sentence = sentence + '.'
                #                 elif i == '-':
                #                     minus = True
                #                     break
                #                 else:
                #                     if num == 0:
                #                         global dic
                #                         dic = {}
                #                         dic['cx'] = float(sentence)
                #                         sentence = ''
                #                         num += 1
                #                     elif num == 1:
                #                         dic['cy'] = float(sentence)
                #                         # dic['name'] = name
                #                         sentence = ''
                #                         num = 0
                #                         list[name] = dic
                #                         name += 1
                #                     else:
                #                         print(error)
                #         if minus:
                #             print('break')
                #
                #         else:
                #             for i in range(length):
                #                 data['nodes'][i]['cx'] = list[data['nodes'][i]['name']]['cx']
                #                 data['nodes'][i]['cy'] = list[data['nodes'][i]['name']]['cy']
                #             data['layout'] = argvs[1]
                #
                #             try:
                #                 current = os.listdir(output + dir)
                #             except:
                #                 os.mkdir(output + dir)
                #             f = open(output + dir + '/' + file , 'w')
                #             json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
else:
    pass
