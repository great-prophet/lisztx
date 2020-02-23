import os
import sys

try:
    directory = sys.argv[1]
except:
    print('must specify directory')
    exit()

outputFormat = ".mp3"

allFiles = os.listdir(directory)

files = [x for x in allFiles if x.find(".opus") > -1 or x.find(".m4a") > -1]

for file in files:
    name = file[:file.rfind(".")]
    os.system("ffmpeg -n -i \"" + directory + file + "\" \"" + directory + name + outputFormat + "\"&")
