# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import json


def read():
    data = json.load(open('../data/result.json'))
    return data


def main():
    data = read()
    list, edges = [], []
    for datum in data:
        group, pgroup, pout = datum['groupSize'], datum['pgroup'], datum['pout']
        list.append([group, pgroup, pout])
        edges.append(datum['edgeCross'])

    names = ['(' + str(i[0]) + ', ' + str(i[1]) + ', ' + str(i[2]) + ')' for i in list]
    xx = np.arange(len(names)) + 1
    col1 = '#ffa0a0'# color of dam height
    col2 = '#a0a0ff'# color of waterway length
    fsz = 12
    fig = plt.figure(figsize=(7, 7), facecolor='w')
    plt.rcParams["font.size"] = fsz

    plt.subplot(211)
    plt.xticks(xx, names)
    plt.xlim(0, len(xx) + 1)
    # (1-a) 左軸グラフの描画
    plt.ylim(0, 20000)
    plt.xlabel('Site name')
    plt.ylabel('Dam height (m)')
    plt.grid(color='#999999', linestyle='--')
    plt.barh(xx - 0.2, edges, width=0.4, color=col1, align='center', label='Dam height (m)')

    # (1-b) 右軸グラフの描画
    plt.twinx()
    plt.ylim(0, 20000)
    # plt.ylabel('Waterway length (m)')
    plt.barh([0], [0], width=0.0, color=col1, align='center', label='Dam height (m)') # 凡例作成のためのダミー
    plt.barh(xx + 0.2, edges, width=0.4, color=col2, align='center', label='Waterway length (m)')
    plt.legend(shadow=True, loc='upper right')
    plt.title('Case: 1800MW x 8hr',loc='left',fontsize=fsz-1)

    plt.show()
    a = input()

if __name__ == '__main__':
    main()