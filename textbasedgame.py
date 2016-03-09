#!/usr/bin/python3

import argparse
import inspect
import os
import sys

try:
    import readline 
except ImportError: # readline doesn't work on iOS
    readline = False

import obj
import utils
import locations
import languages
import entities

def commandLine():
    while True:
        try:
            command = input(': ').split(' ')
            if command[0].upper() == 'WHO':
                print('You are: ' + usr)
            elif command[0].upper() == 'QUIT':
                if utils.confirm('Are you sure you want to quit?'):
                    quitGame()
            elif command[0].upper() == 'RESET':
                if utils.confirm('Are you sure you want to reset?'):
                    newGame()
            else:
                utils.execute(command)
                entities.player.previousCommand = command
        except KeyboardInterrupt:
            quitGame()

def quitGame():
    print('\nSaving progress...')
    utils.saveInfo(usr, 'player.' + entities.player.name, entities.player)
    utils.saveInfo(usr, 'worldEntities', entities.worldEntities)
    try:
        utils.saveInfo(usr, 'previousVendor', previousVendor)
    except NameError:
        utils.saveInfo(usr, 'previousVendor', None)
    print('Progress saved.')
    sys.exit(0)

def newGame(name=None):
    global usr, usrFile
    entities.worldEntities = []
    if name != None:
        usr = name
    else:
        try:
            usr = input('What is your desired username? : ')
            usrFile = usr + '.save' # Add extension
        except KeyboardInterrupt:
            play()
    entities.player = obj.Player(usr, 100, 100, float(5))
    entities.player.inventory = [entities.getWeapon('stick'), entities.getFood('potato')]
    entities.player.location = entities.getLocation('Main')
    print('New game set up. Welcome.')
    commandLine()

def loadGame(name=None):
    global usr, usrFile, previousVendor
    users = []
    for file in os.listdir(utils.fileDir + '/saves'):
        if file.endswith('.save') or file.endswith('.db'): 
            users.append(file.split('.')[0])
    try:
        usr = utils.choose('List of users:', users, 'What is your username?')
        usrFile = usr + '.save'
    except KeyboardInterrupt:
        play()
    try:
        entities.worldEntities = utils.loadInfo(usr, 'worldEntities')
        entities.player = utils.loadInfo(usr, 'player.' + usr)
        previousVendor = utils.loadInfo(usr, 'previousVendor')
    except KeyError:
        print('Savefile is broken. Creating new savefile...')
        newGame(usr)
    print('Game save loaded.')
    try:
        if entities.player.location == entities.getLocation('Inventory'):
            locations.inventory()
        elif entities.player.location == entities.getLocation('Market'):
            utils.goToVendor(previousVendor)
        elif entities.player.location == entities.getLocation('Interact'):
            utils.fight(entities.player.location.entity, entities.player.location.entity.weapon)
            inventory()
        else:
            commandLine()
    except KeyboardInterrupt or EOFError:
        sys.exit(1)

def play():
    while True:
        try:
            print('''
+----------------------------------------------+
| Welcome to textbasedgame!                    |
| This game is released under the GPL.         |
| Copyright V1Soft 2016                        |
+----------------------------------------------+''')
            choice = utils.choose('\nDo you want to:', [['Start a new game', 'new'], ['Continue from a previous save', 'continue'], ['Exit the game', 'quit']], '', False)
            if choice == 'NEW':
                newGame()
            elif choice == 'CONTINUE':
                loadGame()
            elif choice == 'QUIT':
                sys.exit(0)
            else:
                while True:
                    if utils.confirm('Invalid option. Do you want to quit?'):
                        sys.exit(0)
                    else:
                        break
        except KeyboardInterrupt or EOFError:
            sys.exit(0)

# Arguments
argparser = argparse.ArgumentParser(description='A currently unnamed text-based game')
argparser.add_argument('-n', '--new', help='New game', action='store_true')
argparser.add_argument('-l', '--load-game', help='Load existing game', action='store_true')
args = argparser.parse_args()
if args.new:
    newGame()
elif args.load_game:
    loadGame()
else:
    play()
