import sys,json
import os.path

file_in = open(sys.argv[1], 'r')
obj = json.load(file_in)

for x in list(obj.keys()):
    if not os.path.exists(obj[x][0]):
        del(obj[x])

file_out = open(sys.argv[2], 'w')
json.dump(obj,file_out)
