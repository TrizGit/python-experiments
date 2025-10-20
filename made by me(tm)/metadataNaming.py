# Sorting out your music easily.
# Though, it only works when you have filenames that looks like this: no. (#).mp3
# You need to have mutagen installed.
# Works well with fileRenaming.py

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import os, time, random

def checkLength(text:str):
    if len(text) >= 11:
        return text[5:6+(len(text)-11)]

filepath = 'F:\\confidential evidance\\musicPL'
files = [f'no. ({i + 1}).mp3' for i in range(len(os.listdir(filepath)) - 3)]

start = time.time()

for cur_file in files:
    file = MP3(filepath + '\\' + cur_file, ID3=EasyID3)
    try:
        file['album'] = ['songs and stuff']
        file['tracknumber'] = [checkLength(cur_file)]
        file.save()
        print(f'Saving... ({file["title"][0]} // {file["artist"][0]} // {file["tracknumber"][0]})')
    except Exception as e:
        print(f'Saving... ({file["title"][0]} // {file["artist"][0]} // {file["tracknumber"][0]})')
        time.sleep(random.random() / 5)
        print(f'\n> Can\'t save metadata! Is it currently in use? ({file["title"][0]} // {file["artist"][0]} // {file["tracknumber"][0]})\n')

end = time.time()

time.sleep(0.5)
print(f'\nSaved!\nTook {round(end - start, 3)} seconds.\n\nleaving in 5 seconds...')
time.sleep(5)