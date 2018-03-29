# -*- coding: utf-8 -*-

import csv
import json


def test():
	boxes = []
	f = open('data/FDGIB/boxes.csv', 'r')
	reader1 = csv.reader(f)
	for i in reader1:
		boxes.append(i)

	boxNum = len(boxes)
	print(len(boxes))
	linkNum = []
	for i in range(boxNum):
		linkNum.append([])
		for j in range(boxNum - i):
			linkNum[i].append(0)
	print(linkNum)

	reader2 = open('data/FDGIB/data.json', 'r')
	data= json.load(reader2)
	links = data['links']
	# print(links)
	for i in links:
		source = i['source']['group']
		target = i['target']['group']
		if (source != target):
			print('source:'+str(source)+ ', target:' + str(target))
			if source < target:
				if linkNum[source][target-source]  == 0:
					print('empty')
					linkNum[source][target-source] = 1
				else:
					linkNum[source][target-source] += 1
			else:
				if linkNum[target][source-target]  == 0:
					print('empty ')
					linkNum[target][source-target] = 1
				else:
					linkNum[target][source-target] += 1

	max = linkNum[0][0]
	for i in linkNum:
		for j in i:
			if j>max:
				max = j
	length1 = len(linkNum)
	for i in range(length1):
		length2 = len(linkNum[i])
		for j in range(length2):
			linkNum[i][j] /= max
	print(linkNum)

	with open('data/FDGIB/link_boxes.csv', 'w') as f:
		writer = csv.writer(f) # 改行コード（\n）を指定しておく
		for i in linkNum:
			writer.writerow(i)

if __name__ == '__main__':
    test()
