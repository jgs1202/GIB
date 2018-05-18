# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import json
from operator import itemgetter


def read():
    data = json.load(open('../data/result.json'))
    return data


def main():
    data = read()
    listF, edgesF = [], []
    listS, edgesS = [], []
    listT, edgesT = [], []
    listC, edgesC = [], []
    for datum in data:
        group, pgroup, pout, layout = datum['groupSize'], datum['pgroup'], datum['pout'], datum['type']
        if layout == 'STGIB':
            listS.append([group, pgroup, pout, layout])
            edgesS.append(datum['edgeCross'])
        elif layout == 'TRGIB':
            listT.append([group, pgroup, pout, layout])
            edgesT.append(datum['edgeCross'])
        elif layout == 'FDGIB':
            listF.append([group, pgroup, pout, layout])
            edgesF.append(datum['edgeCross'])
        elif layout == 'Chatu':
            listC.append([group, pgroup, pout, layout])
            edgesC.append(datum['edgeCross'])

    # print(listS, edgesS)
    zippedS = sorted(zip(listS, edgesS), reverse=True)
    listS, edgesS = zip(*zippedS)
    zippedT = sorted(zip(listT, edgesT), reverse=True)
    listT, edgesT = zip(*zippedT)
    zippedC = sorted(zip(listC, edgesC), reverse=True)
    listC, edgesC = zip(*zippedC)
    zippedF = sorted(zip(listF, edgesF), reverse=True)
    listF, edgesF = zip(*zippedF)
    namesS = ['(' + str(i[0]) + ', ' + str(i[1]) + ', ' + str(i[2]) + ')' for i in listS]
    # namesT = ['(' + str(i[0]) + ', ' + str(i[1]) + ', ' + str(i[2]) + ') ' + i[3] for i in listT]
    # namesC = ['(' + str(i[0]) + ', ' + str(i[1]) + ', ' + str(i[2]) + ') ' + i[3] for i in listC]
    # namesF = ['(' + str(i[0]) + ', ' + str(i[1]) + ', ' + str(i[2]) + ') ' + i[3] for i in listF]

    xx = np.arange(len(namesS)) + 1
    col1 = '#ffa0a0'  # color of dam height
    col2 = '#a0a0ff'  # color of waterway length
    col3 = '#ABFF7F'
    col4 = '#FFEF85'
    fsz = 3
    fig = plt.figure(figsize=(10, 10), facecolor='w', dpi=150)
    plt.rcParams["font.size"] = fsz

    plt.subplot(211)
    plt.yticks(xx, namesS) 
    plt.xlim(0, 25000)
    plt.ylim(0, len(xx) + 1)
    plt.ylabel('Site name')
    plt.ylabel('number')
    plt.grid(color='#999999', linestyle='--')

    # plt.barh([0], [0], color=col1, align='center', label='Dam height (m)')  # 凡例作成のためのダミー
    
    plt.barh(xx - 0.3, edgesS, height=0.20, color=col1, align='center', label='ST-GIB')
    plt.barh(xx - 0.1, edgesC, height=0.20, color=col2, align='center', label='CD-GIB')
    plt.barh(xx + 0.1, edgesF, height=0.20, color=col3, align='center', label='FD-GIB')
    plt.barh(xx + 0.3, edgesT, height=0.20, color=col4, align='center', label='TR-GIB')


    plt.legend(shadow=True, loc='upper right')
    plt.title('Case: 1800MW x 8hr', loc='left', fontsize=fsz - 1)

    plt.show(fig)
    a = input()

if __name__ == '__main__':
    main()