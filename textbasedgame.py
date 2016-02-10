#!/usr/bin/python3

import argparse
import inspect
import os
import random
import sys
import shelve
import time

from obj import *
from languages import *
from entities import *


def confirm(prompt='', default=True):
    if default:
        answer = input(prompt + ' (Y/n) ')
        if answer.lower() == 'y' or answer.lower() == 'yes' or answer == '':
            return True
        elif answer.lower() == 'n' or answer.lower() == 'no':
            return False
        else:
            return False
    else:
        answer = input(prompt + ' (y/N)')
        if answer.lower() == 'y' or answer.lower() == 'yes':
            return True
        elif answer.lower() == 'n' or answer.lower() == 'no':
            return False
        else:
            return False


def getBestInventoryWeapon():
    bestItemPower = 0
    for item in player.inventory:
        if isinstance(item, Weapon):
            weapPwr = item.power
            if weapPwr > bestItemPower:
                bestItemPower = weapPwr
    return bestItemPower, item

def personInteraction():
    global entities
    player.location = locationInteract
    personType = random.randint(1, 3)
    if personType == 1:
        person = [random.choice(enemies), random.choice(weapons)]
        if confirm('You see a mean-looking person in the distance. Do you choose to approach?'):
            fight(person[0], person[1])
        else:
            print('You run away in fear.')
    elif personType == 2:
        if entities:
            person = random.choice(entities)
            person.inventory.append(random.choice(weapons))
            if confirm('You see a familiar, mean-looking person in the distance. Do you choose to approach?'):
                fight(person, person.inventory[0])
            else:
                print('You run away in fear.')
        else:
            person = random.choice(enemies)
            person.inventory.append(random.choice(weapons))
            if confirm('You see a mean-looking person in the distance. Do you choose to approach?'):
                fight(person, person.inventory[0])
            else:
                print('You run away in fear.')
    else:
        person = [random.choice(helpers), random.choice(helperItems)]
        if confirm('You see a kind-looking person in the distance. Do you choose to approach?'):
            print('The person is a(n) ' + person[0].name + '!')
            if person[0] == oldLady:
                fight(badOldLady, cane)
                return
            time.sleep(0.5)
            print('The %s smiles and holds a(n) %s out in her hand.' %(person[0].name, person[1].name))
            player.inventory.append(person[1])
            time.sleep(0.2)
            print(person[1].name + ' added to your inventory!')
        else:
            print('You walk away')
    time.sleep(2)

def fight(person, weapon):
    global entities
    player.location.name = locationInteract.name
    player.location.description = locationInteract.description
    player.location.entity = person
    time.sleep(0.5)
    print('The ' + str(player.location.entity.name) + ' pulls out a(n) ' + str(weapon.name) + ' threateningly.')
    time.sleep(1)
    if isinstance(weapon, Food): # Code no longer relevant
        print("...So you took the " + str(weapon.name) + " and ate it")
        player.health += weapon.hp
        print("The " + str(player.location.entity.name) + " ran away")
        commandLine()
    for choice in ['auto', 'act', 'item', 'retreat']:
        print(choice)
    while player.health > 1 and player.location.entity.health > 1:
        command = input('Interact : ').split(" ")
        if command[0] == "1" or command[0].upper() == "AUTO":
            break
        elif command[0] == "2" or command[0].upper() == "ACT":
            print("You " +  str(player.location.entity.acts) + " the " + str(player.location.entity.name) + ".")
            if player.location.entity.acts == "pet":
                print("The " + str(player.location.entity.name) + " runs away")
                commandLine()
            else:
                print("...But it didn't work")
                break
        elif command[0] == '3' or command[0].upper() == 'ITEM':
            for item in player.inventory:
                if item in weapons or item in specialWeapons:
                    print(item.name)
            if command[1] == 'eat':
                failed = False
                for item in player.inventory:
                    if item.name == command[2]:
                        if isinstance(item, Food):
                            player.inventory.remove(item)
                            player.health += item.hp
                            print('%s points added to health!' %(item.hp))
                            failed = False
                            break
                        else:
                            print("You cannot eat that")
                            break
                        break
            elif command[1] == 'use':
                for item in player.inventory:
                    if item.name == command[2]:
                        if item.itemtype == 'bomb':
                            print("The " + item.name + " exploded")
                            print("The %s took %s damage!" %(player.location.entity.name, item.power))
                            player.location.entity.health -= item.power
                            player.inventory.remove(item)
                            break
                        else:
                            print("The %s took %s damage!" %(player.location.entity.name, item.power))
                            player.location.entity.health -= item.power
                            #hero.inventory.remove(item)
                            break
            elif command[1] == 'throw':
                for item in player.inventory:
                    if item.name == command[2]:
                        player.inventory.remove(item)
                        print("You threw away the %s" %(item.name))
                        break
                break
            else:
                print("Item command not found.")
        elif command[0] == "4" or command[0].upper() == "RETREAT":
            print("You ran away.")
            player.location.entity = None
            return
    while True:
        player.hit(weapon.power + player.location.entity.power) # Remove health from player
        player.location.entity.health -= getBestInventoryWeapon()[0] + player.power # Remove health of opponent
        if player.health - (weapon.power + person.power) < 1 and person.health - (getBestInventoryWeapon()[0] + player.power) < 1:
            # In case of draw
            time.sleep(0.2)
            print('You somehow managed to escape with %s health remaining.' %(player.health))
            entities.append(player.location.entity)
            player.location.entity = None
            break

        elif player.health < 1:
            # In case of loss
            time.sleep(0.2)
            print('You\'re dead!')
            printedItems = 0
            for item in player.inventory:
               if random.randint(1, 2) == 1 and item != stick:
                   player.inventory.remove(item)
                   player.location.entity.inventory.append(removedItems)
                   print(str(item) + ' dropped from inventory.')
            droppedCoins = random.randint(0, int(player.money / 2))
            player.spend(droppedCoins)
            time.sleep(0.2)
            print('You dropped %s coins on your death.' %(droppedCoins))
            player.location.entity.money += droppedCoins
            entities.append(player.location.entity)
            player.location.entity = None
            break
        elif person.health < 1:
            # In case of win
            print('The ' + str(player.location.entity.name) + ' has been defeated!')
            powerToAdd = player.location.entity.power / 4
            player.gain(powerToAdd)
            time.sleep(0.2)
            print('Your power level is now ' + str(player.power))
            if random.randint(1, 2) == 1:
                for item in person.inventory:
                    player.inventory.append(item)
                    player.location.entity.inventory.remove(item)
                time.sleep(0.2)
                print('%s added to inventory.' %(weapon.name))
            coinsToAdd = person.power * 5 + random.randint(-4, 4) # Dropped coins is opponent pwr * 5 + randint
            player.receive(coinsToAdd)
            time.sleep(0.2)
            print('Opponent dropped %s coins' %(coinsToAdd))
            player.location.entity = None
            break

def saveInfo(username, name, info):
    saveFile = shelve.open(fileDir + '/saves/%s.save' % username)
    saveFile[name] = info
    saveFile.close()

def loadInfo(username, wantedInfo):
    saveFile = shelve.open(fileDir + '/saves/%s.save' % username)
    info = saveFile[wantedInfo]
    return info

def market():
    player.location.name = locationMarket.name
    player.location.description = locationMarket.description
    print('''
+-----------------------------------------------------+
| Welcome to the Market!                              |
| Type an item\'s name to purchase it.                 |
| Type "info <item>" for more information on an item. |
| Type "exit" to leave the store.                     |
+-----------------------------------------------------+
''')
    print('\nVendors:')
    for vendor in vendors:
        print('\t%s' %(vendor.name))
        print('\nPlease type the vendor you want to visit.')
        isVendor = False
        while not isVendor:
            command = input('\nMarket : ')
            for vendor in vendors:
                if vendor.name == command:
                    vendorToVisit = vendor
                    isVendor = True
                    break
                elif command == 'exit':
                    print('You left the store.')
                    return
                else:
                    print('Vendor not found.')
                    break
        goToVendor(vendorToVisit)

def goToVendor(vendor):
    player.location.name = locationMarket.name
    player.location.description = locationMarket.description
    player.location.entity = vendor
    print('%s\nItems for sale:' %(vendor.message))
    vendor.say(vendor.goods)
    while True:
        command = input('\nMarket > %s : ' %(vendor.name))
        commandRun = False
        thingToBuy = None
        for good in vendor.goods:
            if good.name == command:
                thingToBuy = good
                break
        if thingToBuy == None and not command.startswith('info') and command != 'exit':
            print('Item not found.')
        elif not command.startswith('info') and command != 'exit':
            player.spend(vendor.goods[thingToBuy].cost)
            player.inventory.append(thingToBuy)
            print('%s purchased for %s money.' %(thingToBuy.name, vendor.goods[thingToBuy].cost))
        if command.startswith('info'):
            thingToGetInfoOn = command[5:]
            for item in vendor.goods:
                if item.name == thingToGetInfoOn:
                    itemInShop = True
                    break
            if not itemInShop:
                print('Item not found.')
            else:
                if isinstance(item, Weapon):
                    print('Power: %s' %(item.power))
                elif isinstance(item, Food):
                    print('Healing power: %s' %(item.hp))
                print('Description: ' + item.description)
        elif command == 'exit':
            print('You left the store.')
            player.location.entity = None
            return

def inventory():
    player.location.name = locationInventory.name
    player.location.description = locationInventory.description
    while True:
        command = input('Inventory : ').split(" ")
        if command[0] == '.':
            exec(previousCommand)

        elif command[0] == '?' or command[0].upper() == 'HELP':
            print()

        elif command[0].upper() == 'LIST':
            if len(command) > 1:
                if command[1].upper() == 'WEAPONS':
                    for item in player.inventory:
                        if isinstance(item, Weapon):
                            print(item.name + ': Has ' + str(item.power) + ' power')
                elif command[1].upper() == 'FOODS':
                    for item in player.inventory:
                       if isinstance(item, Food):
                           print(item.name + ': Restores ' + str(item.hp) + ' health')
                elif command[1].upper() == 'HEALTH':
                    print(player.health)
                elif command[1].upper() == 'MONEY':
                    print(player.money)
                else:
                    for item in player.inventory:
                        if isinstance(item, Weapon):
                            print(item.name + ': Has ' + str(item.power) + ' power')
                        elif isinstance(item, Food):
                            print(item.name + ': Restores ' + str(item.hp) + ' health')
                        else:
                            print(item.name)

        elif command[0].upper() == 'EAT':
            failed = False
            for item in player.inventory:
                if item.name.upper() == command[1].upper():
                    if isinstance(item, Food):
                        player.inventory.remove(item)
                        player.health += item.hp
                        print('%s points added to health!' %(item.hp))
                        failed = False
                        break
            if failed != False:
                print('Food not in Inventory.')

        elif command[0].upper() == 'EXIT':
            print('You left your Inventory.')
            break

        else:
            print('Inventory command "' + command[0] + '" not found. Type "help" for help.')

def get(weapon):
    player.inventory.append(weapon)

def exec(command):
    command = command.split(" ")
    if command[0] == '?' or command[0].upper() == 'HELP':
        print('Possible commands:')
        for command in possibleCommands:
            print(command)
    elif command[0].upper() == 'GOTO':
        if command[1].upper() == 'INTERACT':
            personInteraction()
        elif command[1].upper() == 'MARKET':
            print('Going to market...')
            market()
        elif command[1].upper() == 'INVENTORY':
            print('Entering Inventory...')
            inventory()
        else:
            print('Location not found.')
    elif command[0].upper() == 'QUIT':
        if confirm('Are you sure you want to quit? Your progress will be saved.', True):
            quitGame()
        else:
            print('Cancelled.')

    elif command[0].upper() == 'RESET':
        if confirm('Are you sure you want to reset all data?', False):
            newGame()
        else:
            print('Cancelled.')

    else:
        print('Command not found. Type "help" for help.')

def devMode():
    global entities, previousCommand
    player.language = Language('en')
    print('Type "help" for help.')
    while True:
        try:
            player.inventory = [stick, gun, cane, fist, sword, knife, grenade, potato, bread, healthPotion]
            command = input(': ')
            if command == '.':
                if previousCommand != None:
                    exec(previousCommand)
                else:
                    print('No previous command set')
            elif command.startswith('get'):
                weapon = command[4:]
                get(weapon)
            else:
                exec(command)
                previousCommand = command

        except KeyboardInterrupt or EOFError:
            quitGame()

def commandLine():
    global entities
    print('Type "help" for help.')
    while True:
        try:
            command = input(': ')
            if command == '.':
                if previousCommand != None:
                    exec(previousCommand)
                else:
                    print('No previous command set')
            else:
                exec(command)
                previousCommand = command

        except KeyboardInterrupt or EOFError:
            quitGame()

def quitGame():
        print('Saving progress...')
        saveInfo(usr, 'previousCommand', player.previousCommand)
        saveInfo(usr, 'entities', entities)
        saveInfo(usr, 'player.' + player.name, player)
#        saveInfo('firstTime', False)
        print('Progress saved.')
        sys.exit()

def newGame():
    global player, entities
    entities = []
    player = Player(input('What is your desired username? : '), 100, 100, float(5))
    player.inventory = [stick, potato]
    player.location = locationMain
    print('What is your desired language?')
    #print('¿Qué idioma tú quieres?') # Broken
    for language in languages:
        print(language)
    lang = input(': ')
    if lang in languages:
        player.language = Language(lang)
        print(player.language.langwelcome)
    else:
        print('Incorrect language given. Defaulting to English.')
        player.language = Language('en')
        print(player.language.langwelcome)
#    saveInfo('firstTime', False)
    commandLine()

def loadGame():
    global player, entities, usr
    try:
        print('List of users:')
        users = []
        for file in os.listdir(fileDir + '/saves'):
            if file.endswith('.save'):
                print(file[:-5])
                users.append(file[:-5])
        usr = input('What is your username? : ')
        if usr not in users:
            print('User not found. Creating new user...')
            newGame()
        entities = loadInfo(usr, 'entities')
        player = loadInfo(usr, 'player.' + usr)
        print('Game save loaded.')
        try:
            if player.location.name == 'Inventory':
                inventory()
            elif player.location.name == 'Market':
                goToVendor(player.location.entity)
            elif player.location.name == 'Interact':
                #fight(player.location.entity, getBestInventoryWeapon()[1])
                inventory()
        except KeyboardInterrupt or EOFError:
            quitGame()
        commandLine()
    except KeyError:
        print('Savefile does not exist or is broken. Creating new savefile...')
        newGame()

def play():
    try:
        while True:
            print('''
+----------------------------------------------+
| Welcome to textbasedgame!                    |
| This game is released under the GPL.         |
| Copyright V1Soft 2016                        |
+----------------------------------------------+

Do you want to:
1. Start a new game (new)
2. Continue from a previous save (continue)
3. Start textbasedgame in cheat (cheats) or
4. Exit the game (quit)
            ''')
            choice = input(': ')
            if choice == 'new' or choice == '1':
                    newGame()
            elif choice == 'continue' or choice == '2':
                loadGame()
            elif choice == 'cheats' or choice == '3':
                global player, entities
                entities = []
                player.inventory = [stick, potato]
                player.health = 100
                player.money = 100
                player.power = float(5)
                print('New game set up. Welcome!')
#                saveInfo('firstTime', False)
                devMode()
            elif choice == 'quit' or choice == '4':
                sys.exit(0)
            else:
                while True:
                    if confirm('Invalid option. Do you want to quit?'):
                        sys.exit(0)
                    else:
                        break
    except EOFError or KeyboardInterrupt:
        sys.exit(0)

# Get current file path
fileDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

possibleCommands = ['help -- show this message',
                    'goto -- goto <location>, ex. goto inventory',
                    'quit--quit game',
                    'reset--reset progress']


if args.reset:
    newGame()
elif args.load_game:
    loadGame()
elif args.dev_mode:
    devMode()
else:
    play()
