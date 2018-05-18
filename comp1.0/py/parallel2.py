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
    df = []
    for datum in data:
        if datum['type'] == 'STGIB':
            layout = 0
        elif datum['type'] == 'Chatu':
            layout = 1
        elif datum['type'] == 'FDGIB':
            layout = 2
        elif datum['type'] == 'TRGIB':
            layout = 3
        list = [datum['edgeCross'], datum['meanSpaceWasted'], datum['meanAspect'], layout]
        df.append(list)
    names = ['Edge crossing', 'Screen space wasted', 'Mean aspect ratio', 'Layout']
    df = pd.DataFrame(df, columns=names)
    df.head()
    return df

def main():
    df = mkframe(read())
    col1 = '#ffa0a0'  # color of dam height
    col2 = '#a0a0ff'  # color of waterway length
    col3 = '#ABFF7F'
    col3 = 'rgb(200, 0, 0)'
    col4 = '#FFEF85'

    data = [
        go.Parcoords(
            line=dict(color=df['Layout'],
                colorscale=[[0.5, col1], [0.5, col2], [0.5, col3], [0.5, col4]]
            ),
            dimensions=list([
                dict(range=[0, 25000],
                    # constraintrange=[4, 8],
                    # name=df['The number of groups'],
                    label='Edge crossing', values=df['Edge crossing']),
                dict(range=[0, 1],
                    # name=df['The number of groups'],
                    label='Screen space wasted', values=df['Screen space wasted']),
                dict(range=[1, 4],
                    # name=df['The number of groups'],
                    label='Mean aspect ratio', values=df['Mean aspect ratio'])
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
