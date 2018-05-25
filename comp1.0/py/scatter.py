# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import json
import numpy as np

def read():
    data1 = json.load(open('../../comp1.0/data/result.json'))
    data2 = json.load(open('../../comp0.3/data/result.json'))
    data1.extend(data2)
    return data1


def mkframe(data):
    combs = []
    for datum in data:
        group, pgroup, pout = datum['groupSize'], datum['pgroup'], datum['pout']
        list = [group, pgroup, pout]
        if list not in combs:
            combs.append(list)
    xs = [ [[] for i in range(4)] for j in range(4)]
    ys = [[[] for i in range(4)]for j in range(4)]
    for datum in data:
        index = (4 - datum['groupSize'] % 4) % 4
        # print(datum['groupSize'], index)
        if datum['type'] == 'STGIB':
            xs[index][0].append(datum['linkSize'])
            ys[index][0].append(datum['edgeCross'])
        elif datum['type'] == 'Chatu':
            xs[index][1].append(datum['linkSize'])
            ys[index][1].append(datum['edgeCross'])
        elif datum['type'] == 'FDGIB':
            xs[index][2].append(datum['linkSize'])
            ys[index][2].append(datum['edgeCross'])
        elif datum['type'] == 'TRGIB':
            xs[index][3].append(datum['linkSize'])
            ys[index][3].append(datum['edgeCross'])
    return [xs, ys]


def main():
    data = mkframe(read())
    xs, ys = data[0], data[1]
    # print(xs)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(xs[0][0], ys[0][0], c='#e590a2', edgecolor='black', linewidth='1')
    ax.scatter(xs[0][1], ys[0][1], c='#DFE0F6', edgecolor='black', linewidth='1')
    ax.scatter(xs[0][2], ys[0][2], c='#D6FEED', edgecolor='black', linewidth='1')
    ax.scatter(xs[0][3], ys[0][3], c='#F9EFC0', edgecolor='black', linewidth='1')
    ax.scatter(xs[1][0], ys[1][0], c='#F19cAA', edgecolor='black', linewidth='1')
    ax.scatter(xs[1][1], ys[1][1], c='#A3A7E5', edgecolor='black', linewidth='1')
    ax.scatter(xs[1][2], ys[1][2], c='#70FFC1', edgecolor='black', linewidth='1')
    ax.scatter(xs[1][3], ys[1][3], c='#F9E381', edgecolor='black', linewidth='1')
    ax.scatter(xs[2][0], ys[2][0], c='#EB6F84', edgecolor='black', linewidth='1')
    ax.scatter(xs[2][1], ys[2][1], c='#676FD4', edgecolor='black', linewidth='1')
    ax.scatter(xs[2][2], ys[2][2], c='#00EF87', edgecolor='black', linewidth='1')
    ax.scatter(xs[2][3], ys[2][3], c='#F9DD5C', edgecolor='black', linewidth='1')
    ax.scatter(xs[3][0], ys[3][0], c='#E22C4A', edgecolor='black', linewidth='1')
    ax.scatter(xs[3][1], ys[3][1], c='#353FBC', edgecolor='black', linewidth='1')
    ax.scatter(xs[3][2], ys[3][2], c='#00A45D', edgecolor='black', linewidth='1')
    ax.scatter(xs[3][3], ys[3][3], c='#F9CD04', edgecolor='black', linewidth='1')

    ax.set_title('second scatter plot')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    fig.show()

    a = input()


if __name__ == '__main__':
    main()
