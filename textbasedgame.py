#!/usr/bin/python3

import time, random, sys, shelve, inspect
from obj import *

def choosePerson(wantedInfo): # Choose person to interact with
    assert wantedInfo == 'person' or wantedInfo == 'item', 'Bad argument.'
    person = random.choice(people)
    item = random.choice(weapons)
    if wantedInfo == 'person':
        return person

    elif wantedInfo == 'item':
        return item


def getBestInventoryWeapon():
    bestItemPower = 0
    for weapon in inventory:
        weapPwr = weapon.power
        if weapPwr > bestItemPower:
            bestItemPower = weapPwr
    return bestItemPower


def personInteraction():
    newPerson = choosePerson('person')
    npi = choosePerson('item')
    print('You see a(n) ' + str(newPerson.name) + ' in the distance. Do you choose to approach (y/n)?')
    time.sleep(2)
    while True:
        if input().upper() == 'Y':
            fight(newPerson, npi)
            break

        else:
            print()
            break


def fight(person, weapon):
    global playerPower, inventory, money, health
    personHealth = 100
    time.sleep(0.5)
    print('The ' + str(person.name)+ ' pulls out a(n) ' + str(weapon.name) + ' threateningly.')
    time.sleep(1)
    while True:
        hero.hit(weapon.power + person.power) # Remove health from player
        personHealth -= getBestInventoryWeapon() + hero.power # Remove health of opponent
        if hero.health - (weapon.power + person.power) < 1 and person.health - (getBestInventoryWeapon() + hero.power) < 1:
            # In case of draw
            time.sleep(0.2)
            print('You somehow managed to escape with %s health remaining.' %(hero.health))
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
            print('You dropped %s coins on your death.' %(droppedCoins))
            break
        elif personHealth < 1:
            # In case of win
            print('The ' + str(person.name) + ' has been defeated!')
            powerToAdd = person.power / 4
            hero.gain(powerToAdd)
            time.sleep(0.2)
            print('Your power level is now ' + str(hero.power))
            if random.randint(1, 2) == 1:
                inventory.append(weapon)
                time.sleep(0.2)
                print('%s added to inventory.' %(weapon.name))
            coinsToAdd = person.power * 5 + random.randint(-4, 4) # Dropped coins is opponent pwr * 5 + randint
            hero.receive(coinsToAdd)
            time.sleep(0.2)
            print('Opponent dropped %s coins' %(coinsToAdd))

            break

def store():
    keeper = Vendor('foodMerchant', 'Hello! Welcome to my food store.')
    print('Wares:')
    keeper.goods = [bread, potato]
    print(keeper.message)
    keeper.say(keeper.goods)
    print('Type an item\'s name to purchase it.')
#    print('Type "info item" for more information on an item.')
    command = input(': ')
    if input != '' or input != 'nothing':
        if command in keeper.goods:
            hero.spend(keeper.goods[command])
            inventory.append(command)
            print('%s purchased for %s money.' %(command, keeper.goods[command]))
            store()
#        elif 'info' in command:
#			thingToGetInfoOn = command[5:]
#			for item in keeper.goods:
#				if item.name == thingToGetInfoOn:
#					itemInShop = True
#					break
#			if not itemInShop:
#				print('Item not found.')
#				store()
#			else:
#				print('Power: )
        else:
            print("Command not found.")
    else:
        commandLine()

def commandLine():
    global saveFile, playerPower, coins, health, inventory
    print('Type "help" for help.')
    while True:
        try:
            command = input(': ')
            if command == 'help':
                print('Possible commands:')
                for command in possibleCommands:
                    print(command)

            elif command == 'interact':
                personInteraction()

            elif command == 'money':
                print(hero.money)

            elif command == 'store':
                store()

            elif command == 'inventory':
                for item in inventory:
                    if isinstance(item, Weapon):
                        print(item.name + ': ' + str(item.power) + ' power')
                    else:
                        print(item)

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
                    saveFile['firstTime'] = True
                else:
                    print('Cancelled.')
            else:
                print('Command not found. Type "help" for help.')

        except KeyboardInterrupt or EOFError:
            quitGame()

def quitGame():
        print('Saving progress...')
        saveFile['inventory'] = inventory
        saveFile['health'] = hero.health
        saveFile['heroPower'] = hero.power
        saveFile['money'] = hero.money 
        saveFile['firstTime'] = False
        print('Progress saved.')
        sys.exit()
        
        
def newGame():
    inventory = [stick]
    health = 100
    coins = 100
    playerPower = float(5)
    print('New game set up. Welcome!')
    saveFile['firstTime'] = False
    commandLine()
    

def loadGame():
    inventory = saveFile['inventory']
    health = saveFile['health']
    coins = saveFile['money']
    playerPower = saveFile['heroPower']
    print('Previous game save loaded.')
    commandLine()
    

def play():
    try:
        while True:
            print('+----------------------------------------------+\n| Welcome to textbasedgame!                    |\n| This game is released under the GPL.         |\n| Copyright V1Soft 2015                        |\n+----------------------------------------------+\n\nDo you want to:\n1. Start a new game (new)\n2. Continue from a previous save (continue) or\n3. Exit the game (quit)')
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
                    choice = input('Invalid option: Do you want to quit (Y/n) ')
                    if choice.upper() == 'Y' or choice == 'yes':
                        sys.exit(0)
                    else:
                        break
    except EOFError or KeyboardInterrupt:
        sys.exit(0)
        
        
possibleCommands = ['help--show this message', 'interact--find another person to interact with',
                    'money--show amount of money', 'store--go to the market', 'inventory--list inventory items', 'health--show health', 'quit--quit game',
                    'reset--reset progress']

hero = Player('nil', 100, 100, 9000)                       

assassin = Enemy('assassin', 100, 10)
oldLady = Enemy('Old Lady', 100, 1)
baby = Enemy('baby', 100, 1)

people = [oldLady, baby, assassin]
stick = Weapon('stick', 5, 0) 
gun = Weapon('gun', 50, 100)  
cane = Weapon('cane', 6, 5)  
fist = Weapon('fist', 3, 0)  
sword = Weapon('sword', 40, 80)
knife = Weapon('knife', 10, 50)

potato = Food('potato', 2, 2)
bread = Food('bread', 5, 5)

weapons = [knife, gun, cane, fist, sword] 
peopleHelpers = []                               
inventory = [stick]                              
                                                 
saveFile = shelve.open('savefile')

if len(sys.argv) < 2:
    play()
elif sys.argv[1] == 'reset':
    newGame()
elif sys.argv[1] == 'continue':
    loadGame()

commandLine()
