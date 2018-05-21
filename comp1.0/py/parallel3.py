# -*- coding: utf-8 -*-

from pandas.tools.plotting import parallel_coordinates
import pandas as pd
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import json
# import matplotlib


def read():
    # data1 = json.load(open('../../comp1.0/data/result.json'))
    data2 = json.load(open('../../comp0.3/data/result.json'))
    # data = data1.extend(data2)
    return data2


def mkframe(data):
    combs = []
    for datum in data:
        group, pgroup, pout = datum['groupSize'], datum['pgroup'], datum['pout']
        list = [group, pgroup, pout]
        if list not in combs:
            combs.append(list)
    df = [[0, 0, 0, 0, 0] for i in range(len(combs))]
    for datum in data:
        for i in range(len(combs)):
            if datum['groupSize']==combs[i][0] and datum['pgroup']==combs[i][1] and datum['pout']==combs[i][2]:
                if datum['type'] == 'STGIB':
                    df[i][0] = datum['edgeCross']
                elif datum['type'] == 'Chatu':
                    df[i][1] = datum['edgeCross']
                elif datum['type'] == 'FDGIB':
                    df[i][2] = datum['edgeCross']
                elif datum['type'] == 'TRGIB':
                    df[i][3] = datum['edgeCross']
                    df[i][4] = datum['groupSize']
    names = ['ST-GIB', 'CD-GIB', 'FD-GIB', 'TR-GIB', 'The number of groups']
    df = pd.DataFrame(df, columns=names)
    df.head()
    return df


def main():
    df = mkframe(read())
    data = [
        go.Parcoords(
            line=dict(color=df['The number of groups'],
                colorscale=[[0, '#D7C16B'], [0.5, '#23D8C3'], [1, '#F3F10F']]
            ),
            dimensions=list([
                dict(range=[0, 25000],
                    # constraintrange=[4, 8],
                    # name=df['The number of groups'],
                    label='ST-GIB', values=df['ST-GIB']),
                dict(range=[0, 25000],
                    # name=df['The number of groups'],
                    label='CD-GIB', values=df['CD-GIB']),
                dict(range=[0, 25000],
                    # name=df['The number of groups'],
                    label='FD-GIB', values=df['FD-GIB']),
                dict(range=[0, 25000],
                    # name=df['The number of groups'],
                    label='TR-GIB', values=df['TR-GIB'])
            ])
        )
    ]



    layout = go.Layout(
        showlegend=True
        # plot_bgcolor='#E5E5E5',
        # paper_bgcolor='#E5E5E5'
    )
    # plt.figure()
    # parallel_coordinates(data, 'The number of groups')
    # plt.show()

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig)


if __name__ == '__main__':
    main()
