#!/usr/bin/python3

import inspect
import os
import readline

import obj
import utils
import locations
import languages
import entities

def play():
    while True:
        try:
            print('''
+----------------------------------------------+
| Welcome to textbasedgame!                    |
| This game is released under the GPL.         |
| Copyright V1Soft 2016                        |
+----------------------------------------------+''')
            choice = utils.choose('\nDo you want to:', ['new', 'continue', 'quit'], '', False)
            if choice[0].upper() == 'NEW':
                utils.newGame()
            elif choice[0].upper() == 'CONTINUE':
                utils.loadGame()
            elif choice[0].upper() == 'QUIT':
                exit(0)
            else:
                while True:
                    if utils.confirm('Invalid option. Do you want to quit?'):
                        exit(0)
                    else:
                        break
        except KeyboardInterrupt or EOFError:
            exit(0)

if entities.args.reset:
    utils.newGame()
    commandLine()
elif entities.args.load_game:
    utils.loadGame()
else:
    play()
