import json
import os
import shutil
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TDRC

# directory = os.getcwd()

directory = "backup/"

extensions = [".info.json", ".jpg", ".mp3"]

allFiles = os.listdir(directory)

files = [x.replace(".info.json", "") for x in allFiles if x.find(".info.json") > -1]

for name in files:

    #rename files

    data = json.load(open(directory + name + ".info.json", 'r'))

    playlist = data["uploader"].replace(" - Topic", "")
    title = data["track"].replace("/", "-")
    album = data["album"].replace("/", "-")
    artist = data["artist"].replace("/", "-")
    year = str(data["release_year"])

    for ext in extensions:
        os.rename(directory + name + ext, directory + title + ext)


    # write mp3 metadata

    tags = ID3(directory + title + ".mp3")

    tags["TIT2"] = TIT2(encoding=3, text=title)
    tags["TALB"] = TALB(encoding=3, text=album)
    tags["TPE1"] = TPE1(encoding=3, text=artist)
    # tags["TCOM"] = TCOM(encoding=3, text="Composer")
    # tags["TCON"] = TCON(encoding=3, text="Genre")
    tags["TDRC"] = TDRC(encoding=3, text=year)
    # tags["TRCK"] = TRCK(encoding=3, text="track_number")

    tags.save(directory + title + ".mp3")


    # move mp3 to album

    albumPath = playlist + "/" + album + "/"

    os.makedirs(directory + albumPath, exist_ok=True)
    shutil.copy(directory + title + ".mp3", directory + albumPath)


    # copy album art if not exist

    if album + ".jpg" not in os.listdir(directory + albumPath):
        shutil.copy(directory + title + ".jpg", directory + albumPath)
        os.rename(directory + albumPath + title + ".jpg", directory + albumPath + album + ".jpg")

    print(title)
