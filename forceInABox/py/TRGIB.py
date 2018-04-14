from main import run
import os
import json

if __name__ == '__main__':
    main = '../data/origin/'
    width = 960
    height = 600
    for dir in os.listdir(main):
        if (dir != '.DS_Store'):
            for file in os.listdir(main + dir):
                if (dir != '.DS_Store'):
                    path = main + dir + '/' + file
                    graph = json.load(open(path))
                    out = '../data/TRGIB/temp/' + dir + '/'
                    try:
                        a = os.listdir(out)
                    except:
                        os.mkdir(out)
                    run(graph, width, height, out + file)
