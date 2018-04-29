from main import run
import os
import json
from STGIB import ST

if __name__ == '__main__':
    main = '../data/origin/TRGIB/'
    width = 960
    height = 600
    graph = json.load(open('./14.json'))
    out = './re_14.json'
    run(graph, width, height, out)
