# -*- coding: utf-8 -*-

import os
import sys
import subprocess

argvs = sys.argv
if len(argvs) != 3:
    print('lack of argvs')
    sys.exit()

main = []
if argvs[2] == 'all':
    main.append('../../' + argvs[1] + '/data/STGIB/temp/')
    main.append('../../' + argvs[1] + '/data/Chaturvedi/temp/')
    main.append('../../' + argvs[1] + '/data/TRGIB/temp/')
    main.append('../../' + argvs[1] + '/data/FDGIB/temp/')
else:
    main.append('../../' + argvs[1] + '/data/' + argvs[2] + '/temp/')

inp = input('Are you really run this program? This can damage your data. (y/n) :')
if inp == 'y':
    for dir in main:
        try:
            for file in os.listdir(dir):
                    if (file[-5:] == '.json'):
                        cmd = 'cargo run --release --example gib -- -f ' + dir + '/' + file + ' > '+ dir + '/' + file[:-5] + '-image.svg'
                            # subprocess.call( cmd.strip().split(' ') )
                        os.system(cmd)
                        print(dir, file)
        except:
            pass
else:
    pass
