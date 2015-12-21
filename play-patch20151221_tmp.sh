#!/bin/bash

echo -e "Welcome to textbasedgame!\nThis game is released under the GPL.\nCopyright V1Soft 2015"
python3 -c "import shelve
shelf = shelve.open('savefile')
shelf['firstTime'] = True
shelf.close()"
python3 main.py
