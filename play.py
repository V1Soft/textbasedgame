#!/usr/bin/python3

import os, shelve

print('Welcome to textbasedgame!')
print('This game is released under the GPL.')
print('Copyright V1Soft 2015')

print('Do you want to 1. continue from a previous save or 2. start over?')
choice = input()
if choice.startswith('2'):
    # shelf = shelve.open('savefile')
    # shelf['firstTime'] = True
    # shelf.close()
    os.system("python3 main.py reset")
else:
    os.system("python3 main.py continue")
