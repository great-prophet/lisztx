import json
import os
import sys
import shutil
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TDRC
from PIL import Image

try:
    directory = sys.argv[1]
    outputPath = sys.argv[2]
except:
    print('must specify directory and output')
    exit()


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

    playlistAlbum = playlist + " - " + album
    albumPath = outputPath + playlist + "/" + playlistAlbum + "/"

    os.makedirs(albumPath, exist_ok=True)
    shutil.copy(title + ".mp3", albumPath)

    # copy playlistAlbum art if not exist

    if playlistAlbum + ".jpg" not in os.listdir(albumPath):
        shutil.copy(title + ".jpg", albumPath)
        os.rename(albumPath + title + ".jpg", albumPath + playlistAlbum + ".jpg")

        # crop cover art

        cover = Image.open(directory + albumPath + playlistAlbum + ".jpg")
        width, height = cover.size
        cover = cover.crop(((width - height) / 2, 0, width - (width - height) / 2, height))
        cover.save(directory + albumPath + playlistAlbum + ".jpg")

    print(title)
