# -*- coding: utf-8 -*-

import os
import sys
import json
import pandas as pd
import pandas.tools.plotting as plotting
import matplotlib.pyplot as plt

def custom_round(number, ndigits=0):
    if type(number) == int:#整数ならそのまま返す
        return number
    # print(type(number))
    d_point = len(str(number).split('.')[1])#小数点以下が何桁あるか定義
    if ndigits >= d_point:#求める小数点以下の値が引数より大きい場合はそのまま返す
        return number
    c = (10 ** d_point) * 2
    #小数点以下の桁数分元の数に0を足して整数にして2倍するための値(0.01ならcは200)
    return round((number * c + 1) / c, ndigits)
    #元の数に0を足して整数にして2倍して1を足して2で割る。元の数が0.01なら0.015にしてroundを行う

def main():
	data = json.load(open('../data/result.json', 'r'))
	indices = []
	for datum in data:
		if datum['type'] == 'STGIB':
			indices.append([datum['groupSize'], datum['pgroup'], datum['pout']])
	output = [ {} for i in range(len(indices))]
	for index in range(len(indices)):
		output[index]['name'] = str(indices[index][0]) + ', ' + str(indices[index][1]) + ', ' + str(indices[index][2])
		output[index]['data'] = []
	for datum in data:
		for index in range(len(indices)):
			if datum['groupSize']==indices[index][0] and datum['pgroup']==indices[index][1] and datum['pout']==indices[index][2]:
				dic = {}
				dic['layout'] = datum['type']
				dic['edgeCross'] = custom_round(datum['edgeCross'], 0)
				dic['meanAspect'] = custom_round(datum['meanAspect'], 3)
				dic['meanSpaceWasted'] = custom_round(datum['meanSpaceWasted'], 3)
				dic['devEdgeCross'] = custom_round(datum['devEdgeCross'], 0)
				dic['devAspect'] = custom_round(datum['devAspect'], 3)
				dic['devSpaceWasted'] = custom_round(datum['devSpaceWasted'], 3)
				output[index]['data'].append(dic)

	for out in output:
		print(out['data'])
		columns = ( 'edge crossing (SD)', 'mean aspect ratio (SD)', 'mean space efficiency (SD)')
		rows = ['STGIB', 'CDGIB', 'FDGIB', 'TRGIB']
		tableData = [[] for i in range(4)]
		for i in out['data']:
			if i['layout'] == 'STGIB':
				tableData[0].extend( [ (str(i['edgeCross'])+' (' +str(i['devEdgeCross']) +')'), (str(i['meanAspect'])+' ('+str(i['devAspect']) +')'), (str(i['meanSpaceWasted'])+' ('+str(i['devSpaceWasted']) +')')] )
			elif i['layout'] == 'Chatu':
				tableData[1].extend( [ (str(i['edgeCross'])+' (' +str(i['devEdgeCross']) +')'), (str(i['meanAspect'])+' ('+str(i['devAspect']) +')'), (str(i['meanSpaceWasted'])+' ('+str(i['devSpaceWasted']) +')')] )
			elif i['layout'] == 'FDGIB':
				tableData[2].extend( [ (str(i['edgeCross'])+' (' +str(i['devEdgeCross']) +')'), (str(i['meanAspect'])+' ('+str(i['devAspect']) +')'), (str(i['meanSpaceWasted'])+' ('+str(i['devSpaceWasted']) +')')] )
			elif i['layout'] == 'TRGIB':
				tableData[3].extend( [ (str(i['edgeCross'])+' (' +str(i['devEdgeCross']) +')'), (str(i['meanAspect'])+' ('+str(i['devAspect']) +')'), (str(i['meanSpaceWasted'])+' ('+str(i['devSpaceWasted']) +')')] )
		print(tableData)
		# plt.table(cellText = tableData, rowLabels=rows, colLabels=columns)
		fig, ax = plt.subplots(1,1)
		plotting.table(ax, pd.DataFrame(tableData),rowLabels=rows, colLabels=columns,  loc='center')
		plt.title(out["name"])
		ax.axis('off')
		plt.savefig('../data/tables/' + out['name'] + '.png')
		# sys.exit()




if __name__ == '__main__':
	main()