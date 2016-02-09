#!/usr/bin/python3

import random
import sys
import shelve
import time

from obj import *
from entities import *


# Util. Functions
def yesorno(x=''):
    if x == '':
        user = input(x)
        if user.lower() == 'y' or user.lower() == 'yes':
            return 'yes'
        elif user.lower() == 'n' or user.lower() == 'no':
            return 'no'
        else:
            print("Lel")
    else:
        user = input()
        if user.lower() == 'y' or 'yes':
            return 'yes'
        elif user.lower() == 'n' or user.lower() == 'no':
            return 'no'
        else:
            print("lel")


def choosePerson():  # Choose person to interact with
    personType = random.randint(1, 2)
    if personType == 1:
        person = random.choice(enemies)
    else:
        person = random.choice(helpers)

    if person in enemies:
        item = random.choice(weapons)
    else:
        item = random.choice(helperItems)

    return [person, item]


def getBestInventoryWeapon():
    bestItemPower = 0
    for item in inventory:
        if isinstance(item, Weapon):
            weapPwr = item.power
            if weapPwr > bestItemPower:
                bestItemPower = weapPwr
    return bestItemPower


def worldHandler():
    hero.turn += 1
    if hero.turn >= 10 and hero.turn <= 15:
        World.temp = 20
        print("It's getting colder. The current temp is %s." % (World.temp))
    elif hero.turn >= 15 and hero.turn <= 20:
        World.temp = 15
        print("The sun is setting. The current temp is %s." % (World.temp))
    elif hero.turn >= 20 and hero.turn <= 30:
        World.temp = 10
        print("It's night. The current temp is %s." % (World.temp))
    else:
        World.temp = 37
        print("It's daytime! The current temp is %s." % (World.temp))


# Funcs. for gameplay
def personInteraction():
    global inventory
    chosenThings = choosePerson()
    newPerson = chosenThings[0]  # Get person from chosenThings list
    npi = chosenThings[1]
    if isinstance(newPerson, Helper):
        print('You see a kind-looking person in the distance. Do you choose to approach (y/n)?')
    else:
        print('You see a mean-looking person in the distance. Do you choose to approach (y/n)?')
    time.sleep(2)
    while True:
        if yesorno() == 'yes':
            print('The person is a(n) ' + newPerson.name + '!')
            if isinstance(newPerson, Helper):
                if newPerson == oldLady:
                    fight(badOldLady, cane)
                    return
                time.sleep(0.5)
                print('The %s smiles and holds a(n) %s out in her hand.' % (newPerson.name, npi.name))
                inventory.append(npi)
                time.sleep(0.2)
                print(npi.name + ' added to your inventory!')
            else:
                fight(newPerson, npi)
            break

        else:
            print('You run away from the %s in fear.' % (newPerson.name))
            break


def fight(person, weapon):
    global playerPower, inventory, money, health
    personHealth = 100
    time.sleep(0.5)
    print('The ' + str(person.name)+ ' pulls out a(n) ' + str(weapon.name) + ' threateningly.')
    time.sleep(1)
    if isinstance(weapon, Food):  # Code no longer relevant
        print("...So you took the " + str(weapon.name) + " and ate it")
        hero.health += weapon.hp
        print("The " + str(person.name) + " ran away")
        commandLine()
    for choice in interactoptions:
        print(choice)
    while True:
        command = input(": ")
        if command == "1" or command.upper() == "FIGHT":
            break
        elif command == "2" or command.upper() == "ACT":
            print("You " + str(person.acts) + " the " + str(person.name) + ".")
            if random.randint(0, 100) % 2 == 0:
                print("The " + str(person.name) + " runs away")
                commandLine()
            else:
                print("...But it didn't work")
                break
        elif command == "3" or command.upper() == "ITEM":
            for item in inventory:
                if item in weapons or item in specialWeapons:
                    print(item.name)
            command = input("What do you want to use?: ")
            if command.startswith('eat'):
                # failed = False
                foodToEat = command[4:]  # Get food out of command string
                for item in inventory:
                    if item.name == foodToEat:
                        if isinstance(item, Food):
                            inventory.remove(item)
                            hero.health += item.hp
                            print('%s points added to health!' % (item.hp))
                            # failed = False
                            break
                        else:
                            print("You cannot eat that")
                            break
                        break
            elif command.startswith('use'):
                touse = command[4:]
                for item in inventory:
                    if item.name == touse:
                        if item.itemtype == 'bomb':
                            print("The " + item.name + " exploded")
                            print("The %s took %s damage!" % (person.name, item.power))
                            person.health -= item.power
                            inventory.remove(item)
                            break
            elif command.startswith('throw'):
                tothrow = command[6:]
                for item in inventory:
                    if item.name == tothrow:
                        inventory.remove(item)
                        print("You threw away the %s" % (item.name))
                        break
                break
            else:
                print("It does not seem you have that item")
                break
        elif command == "4" or command.upper() == "SPARE":
            print("You ran away")
            commandLine()
    while True:
        hero.hit(weapon.power + person.power)  # Remove health from player
        personHealth -= getBestInventoryWeapon() + hero.power  # Remove health of opponent
        if hero.health - (weapon.power + person.power) < 1 and person.health - (getBestInventoryWeapon() + hero.power) < 1:
            # In case of draw
            time.sleep(0.2)
            print('You somehow managed to escape with %s health remaining.' % (hero.health))
            break

        elif hero.health < 1:
            # In case of loss
            time.sleep(0.2)
            print('You\'re dead!')
            removedItems = []
            for item in inventory:
                if random.randint(1, 2) == 1 and item != stick:
                    inventory.remove(item)
                    removedItems.append(item)

            printedItems = 0
            for item in removedItems:
                printedItems += 1
                time.sleep(0.2)
                if printedItems == len(removedItems):
                    print(str(item) + ' dropped from inventory.')

                else:
                    print(item + ', ', end='')

            droppedCoins = random.randint(0, int(hero.money / 2))
            hero.spend(droppedCoins)
            time.sleep(0.2)
            print('You dropped %s coins on your death.' % (droppedCoins))
            break
        elif personHealth < 1:
            # In case of win
            print('The ' + str(person.name) + ' has been defeated!')
            powerToAdd = person.power / 4
            hero.gain(powerToAdd)
            hero.lv += 1
            time.sleep(0.2)
            print('Your power level is now ' + str(hero.power))
            if random.randint(1, 2) == 1:
                inventory.append(weapon)
                time.sleep(0.2)
                print('%s added to inventory.' % (weapon.name))
            coinsToAdd = person.power * 5 + random.randint(-4, 4)  # Dropped coins is opponent pwr * 5 + randint
            hero.receive(coinsToAdd)
            time.sleep(0.2)
            print('Opponent dropped %s coins' % (coinsToAdd))
            break


def saveInfo(name, info):
    saveFile = shelve.open('savefile')
    saveFile[name] = info
    saveFile.close()


def loadInfo(wantedInfo):
    saveFile = shelve.open('savefile')
    info = saveFile[wantedInfo]
    return info


def market():
    def goToVendor(vendor):
        print(vendor.message)
        print('Type an item\'s name to purchase it.')
        print('Type "info <item>" for more information on an item.')
        print('Type "exit" to leave the store.')
        print('Items for sale:')
        vendor.say(vendor.goods)
        while True:
                command = input(': ')
                # commandRun = False
                thingToBuy = None
                for good in vendor.goods:
                    if good.name == command:
                        thingToBuy = good
                        break
                if thingToBuy is None and not command.startswith('info') and command is not 'exit':
                    print('Item not found.')
                elif not command.startswith('info') and command != 'exit':
                    hero.spend(vendor.goods[thingToBuy].cost)
                    inventory.append(thingToBuy)
                    print('%s purchased for %s money.' % (thingToBuy.name, vendor.goods[thingToBuy].cost))

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
                            print('Power: %s' % (item.power))
                        elif isinstance(item, Food):
                            print('Healing power: %s' % (item.hp))
                        print('Description: ' + item.description)
                elif command == 'exit':
                    print('You left the store.')
                    return

    print('Vendors:')
    for vendor in vendors:
        print(vendor.name)

    print('Please type the vendor you want to visit.')
    isVendor = False
    while not isVendor:
        command = input()
        for vendor in vendors:
            if vendor.name == command:
                vendorToVisit = vendor
                isVendor = True
            else:
                print('Vendor not found.')

    goToVendor(vendorToVisit)


def commandLine():
    global inventory
    print('Type "help" for help.')
    while True:
        try:
            worldHandler()
            command = input(': ')
            if command == 'help':
                print('Possible commands:')
                for command in possibleCommands:
                    print(command)

            elif command == 'interact':
                personInteraction()

            elif command == 'money':
                print(hero.money)

            elif command == 'market':
                market()

            elif command == 'inventory':
                for item in inventory:
                    if isinstance(item, Weapon):
                        print(item.name + ': ' + str(item.power) + ' power')
                    elif isinstance(item, Food):
                        print(item.name + ': Restores ' + str(item.hp) + ' health')
                    else:
                        print(item.name)

            elif command == 'health':
                print(hero.health)

            elif command == 'quit':
                print('Are you sure you want to quit? Your progress will be saved.')
                choice = input()
                if choice == 'y' or choice == 'yes':
                    quitGame()
                else:
                    print('Cancelled.')

            elif command == 'reset':
                print('Are you sure you want to reset all data?')
                choice = input()
                if choice == 'y' or choice == 'yes':
                    saveInfo('firstTime', True)
                else:
                    print('Cancelled.')
            elif command.startswith('eat'):
                failed = False
                foodToEat = command[4:]  # Get food out of command string
                for item in inventory:
                    if item.name == foodToEat:
                        if isinstance(item, Food):
                            inventory.remove(item)
                            hero.health += item.hp
                            print('%s points added to health!' % (item.hp))
                            failed = False
                            break

                if failed is not False:
                    print('Food not in inventory.')
            elif command == 'temp':
                print(World.temp)

            else:
                print('Command not found. Type "help" for help.')

        except KeyboardInterrupt or EOFError:
            quitGame()


def quitGame():
        print('Saving progress...')
        saveInfo('inventory', inventory)
        saveInfo('health', hero.health)
        saveInfo('heroPower', hero.power)
        saveInfo('money', hero.money)
        saveInfo('firstTime', False)
        print('Progress saved.')
        sys.exit()


def newGame():
    global inventory
    inventory = [stick, potato]
    hero.health = 100
    hero.money = 100
    hero.power = float(5)
    print('New game set up. Welcome!')
    saveInfo('firstTime', False)
    commandLine()


def loadGame():
    global inventory
    try:
        inventory = loadInfo('inventory')
        hero.health = loadInfo('health')
        hero.money = loadInfo('money')
        hero.power = loadInfo('heroPower')
        print('Previous game save loaded.')
        commandLine()
    except KeyError:
        print('Savefile does not exist. Creating new savefile...')
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
2. Continue from a previous save (continue) or
3. Exit the game (quit)
            ''')
            choice = input(': ')
            if choice == 'new' or choice == '1':
                print('Are you sure you want to reset all data?')
                choice = input(': ')
                if choice.upper() == 'Y' or choice == 'yes':
                    newGame()
                else:
                    print('Cancelled.')
            elif choice == 'continue' or choice == '2':
                loadGame()
            elif choice == 'quit' or choice == '3':
                sys.exit(0)
            else:
                while True:
                    choice = input('Invalid option: Do you want to quit (Y/n)')
                    if choice.upper() == 'Y' or choice == 'yes':
                        sys.exit(0)
                    else:
                        break
    except EOFError or KeyboardInterrupt:
        sys.exit(0)


possibleCommands = ['help--show this message',
                    'interact--find another person to interact with',
                    'money--show amount of money',
                    'market--go to the market',
                    'inventory--list inventory items',
                    'health--show health',
                    'quit--quit game',
                    'reset--reset progress',
                    'eat <food>--consume food and restore health'
                    'temp--get current temperature']

interactoptions = ['fight', 'act', 'item', 'spare']

hero = Player('nil', 100, 100, 9000)

if args.reset:
    newGame()
elif args.load_game:
    loadGame()
else:
    play()
