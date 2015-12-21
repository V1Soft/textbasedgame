#!/usr/bin/python3
import os
import shelve
print("Welcome to textbasedgame!\nThis game is released under the GPL.\nCopyright V1Soft 2015")
shelf = shelve.open('savefile')
shelf['firstTime'] = True
shelf.close()
os.system("python3 main.py")
