# -*- coding: utf-8 -*-

import csv
import json
import sys
import os

def test(path, file):
	reader2 = open(path, 'r')
	data= json.load(reader2)
	max = 0
	for i in data['nodes']:
		if i['group'] > max:
			max = i['group']
	boxNum = max + 1
	linkNum = []
	for i in range(boxNum):
		linkNum.append([])
		for j in range(boxNum - i):
			linkNum[i].append(0)

	links = data['links']
	for i in links:
		source = data['nodes'][i['source']]['group']
		target = data['nodes'][i['target']]['group']
		if source != target:

			if source < target:
				if linkNum[source][target-source]  == 0:
					linkNum[source][target-source] = 1
				else:
					linkNum[source][target-source] += 1
			else:
				if linkNum[target][source-target]  == 0:
					linkNum[target][source-target] = 1
				else:
					linkNum[target][source-target] += 1

	max = linkNum[0][0]
	for i in linkNum:
		for j in i:
			if j>max:
				max = j
	length1 = len(linkNum)
	if max != 0:
		for i in range(length1):
			length2 = len(linkNum[i])
			for j in range(length2):
				linkNum[i][j] /= max

	length = boxNum
	Gskew = [ 0.0 for i in range(length)]
	for i in range(length):
		len2 = len(linkNum)
		# print(len2)
		for j in range(len2):
			len3 = len(linkNum[j])
			# print(len3)
			for k in range(len3):
				if j == i:
					Gskew[i] += float(linkNum[j][k])
				elif j < i:
					if k == i-j:
						Gskew[i] += float(linkNum[j][k])

	if os.path.exists('../data//origin-group-link') == False:
		os.mkdir('../data//origin-group-link')
	if os.path.exists('../data//origin-group-link/number') == False:
		os.mkdir('../data//origin-group-link/number')
	if os.path.exists('../data//origin-group-link/weight') == False:
		os.mkdir('../data//origin-group-link/weight')
	with open('../data/origin-group-link/weight/' + file[:-5] +'.csv', 'w') as f:
		writer = csv.writer(f) # 改行コード（\n）を指定しておく
		for i in linkNum:
			writer.writerow(i)

	with open('../data/origin-group-link/number/' + file[:-5] +'.csv', 'w') as f:
		writer = csv.writer(f) # 改行コード（\n）を指定しておく
		writer.writerow(Gskew)

if __name__ == '__main__':
	main = '../data/origin/'
	for file in os.listdir(main):
		if file != '.DS_Store':
			path = main + file
			# print('test')
			test(path, file)
