import json
import os

# directory = os.getcwd()

directory = "backup/"
succFormat = ".mp3"  # succ = successor
rootFormats = [".opus", ".m4a"]

allFiles = os.listdir(directory)

converted = [x.replace(succFormat, "") for x in allFiles if x.find(succFormat) > -1]

totalReaped = 0

for file in converted:
    for ext in rootFormats:
        if directory + file + ext in allFiles:
            os.system("rm \"" + directory + file + ext + "\"")
            totalReaped += 1

print("Reaped " + str(totalReaped) + " files")