#!/usr/bin/python3

import argparse
import random 
import sys
import shelve
import time

from obj import *

def choosePerson(): # Choose person to interact with
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


def personInteraction():
    global inventory
    chosenThings = choosePerson()
    
    newPerson = chosenThings[0] # Get person from chosenThings list
    npi = chosenThings[1]
    if isinstance(newPerson, Helper):
        command = input('You see a kind-looking person in the distance. Do you choose to approach? (y/n) : ')
    else:
        command = input('You see a mean-looking person in the distance. Do you choose to approach? (y/n) : ')
    time.sleep(2)
    while True:
        if command.upper() == 'Y':
            print('The person is a(n) ' + newPerson.name + '!')
            if isinstance(newPerson, Helper):
                if newPerson == oldLady:
                    fight(badOldLady, cane)
                    return
                time.sleep(0.5)
                print('The %s smiles and holds a(n) %s out in her hand.' %(newPerson.name, npi.name))
                inventory.append(npi)
                time.sleep(0.2)
                print(npi.name + ' added to your inventory!')
            else:
                fight(newPerson, npi)
            break

        else:
            print('You run away from the %s in fear.' %(newPerson.name))
            break


def fight(person, weapon):
    global playerPower, inventory, money, health
    personHealth = 100
    time.sleep(0.5)
    print('The ' + str(person.name)+ ' pulls out a(n) ' + str(weapon.name) + ' threateningly.')
    time.sleep(1)
    if isinstance(weapon, Food): # Code no longer relevant
        print("...So you took the " + str(weapon.name) + " and ate it")
        hero.health += weapon.hp
        print("The " + str(person.name) + " ran away")
        commandLine()
    for choice in interactoptions:
        print(choice)
    while hero.health > 1 and person.health > 1:
        command = input('Interact : ').split(" ")
        if command[0] == "1" or command[0].upper() == "FIGHT":
            continue
        elif command[0] == "2" or command[0].upper() == "ACT":
            print("You " +  str(person.acts) + " the " + str(person.name) + ".")
            if person.acts == "pet":
                print("The " + str(person.name) + " runs away")
                commandLine()
            else:
                print("...But it didn't work")
                break
        elif command[0] == '3' or command[0].upper() == 'ITEM':
            for item in inventory:
                if item in weapons or item in specialWeapons:
                    print(item.name)
            if command[1] == 'eat':
                failed = False
                for item in inventory:
                    if item.name == command[2]:
                        if isinstance(item, Food):
                            inventory.remove(item)
                            hero.health += item.hp
                            print('%s points added to health!' %(item.hp))
                            failed = False
                            break
                        else:
                            print("You cannot eat that")
                            break
                        break
            elif command[1] == 'use':
                for item in inventory:
                    if item.name == command[2]:
                        if item.itemtype == 'bomb':
                            print("The " + item.name + " exploded")
                            print("The %s took %s damage!" %(person.name, item.power))
                            person.health -= item.power
                            inventory.remove(item)
                            break
                        else:
                            print("The %s took %s damage!" %(person.name, item.power))
                            person.health -= item.power
                            #inventory.remove(item)
                            break
            elif command[1] == 'throw':
                for item in inventory:
                    if item.name == command[2]:
                        inventory.remove(item)
                        print("You threw away the %s" %(item.name))
                        break
                break
            else:
                print("It does not seem you have that item")
        elif command[0] == "4" or command[0].upper() == "SPARE":
            print("You ran away")
            commandLine()
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
                    hero.spend(vendor.goods[thingToBuy].cost)
                    inventory.append(thingToBuy)
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
                    return
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

def get(weapon):
    inventory.append(weapon)

def devMode():
    global inventory
    print('Type "help" for help.')
    while True:
        try:
            inventory = [stick, gun, cane, fist, sword, knife, grenade, potato, bread, healthPotion]
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
                choice = input('Are you sure you want to quit? Your progress will be saved. (y/n) : ')
                if choice == 'y' or choice == 'yes':
                    quitGame()
                else:
                    print('Cancelled.')
         
            elif command == 'reset':
                choice = input('Are you sure you want to reset all data? (y/n) : ')
                if choice == 'y' or choice == 'yes':
                    saveInfo('firstTime', True)
                else:
                    print('Cancelled.')
            elif command.startswith('eat'):
                failed = False
                foodToEat = command[4:] # Get food out of command string
                for item in inventory:
                    if item.name == foodToEat:
                        if isinstance(item, Food):
                            inventory.remove(item)
                            hero.health += item.hp
                            print('%s points added to health!' %(item.hp))
                            failed = False
                            break
					
                if failed != False:
                    print('Food not in inventory.')
            elif command.startswith('get'):
                weapon = command[4:]
                get(weapon)
            else:
                print('Command not found. Type "help" for help.')

        except KeyboardInterrupt or EOFError:
            quitGame()


def commandLine():
    global inventory
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
                choice = input('Are you sure you want to quit? Your progress will be saved. (y/n) : ')
                if choice == 'y' or choice == 'yes':
                    quitGame()
                else:
                    print('Cancelled.')
         
            elif command == 'reset':
                choice = input('Are you sure you want to reset all data? (y/n) : ')
                if choice == 'y' or choice == 'yes':
                    saveInfo('firstTime', True)
                else:
                    print('Cancelled.')
            elif command.startswith('eat'):
                failed = False
                foodToEat = command[4:] # Get food out of command string
                for item in inventory:
                    if item.name == foodToEat:
                        if isinstance(item, Food):
                            inventory.remove(item)
                            hero.health += item.hp
                            print('%s points added to health!' %(item.hp))
                            failed = False
                            break
					
                if failed != False:
                    print('Food not in inventory.')
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
2. Continue from a previous save (continue)
3. Start Textbasedgame in Developer mode (cheats) or
4. Exit the game (quit)
            ''')
            choice = input(': ')
            if choice == 'new' or choice == '1':
                choice = input('Are you sure you want to reset all data? (y/n) : ')
                if choice.upper() == 'Y' or choice == 'yes':
                    newGame()
                else:
                    print('Cancelled.')
            elif choice == 'continue' or choice == '2':
                loadGame()
            elif choice == 'cheats' or choice == '3':
                global inventory
                inventory = [stick, potato]
                hero.health = 100
                hero.money = 100
                hero.power = float(5)
                print('New game set up. Welcome!')
                saveInfo('firstTime', False)
                devMode()
            elif choice == 'quit' or choice == '4':
                sys.exit(0)
            else:
                while True:
                    choice = input('Invalid option: Do you want to quit (y/n) : ')
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
                    'eat <food>--consume food and restore health']
interactoptions = ['fight', 'act', 'item', 'spare']

hero = Player('nil', 100, 100, 9000)                       

# Set up enemies
assassin = Enemy('assassin', 100, 10, "pet")
baby = Enemy('baby', 100, 1, "pet")
badOldLady = Enemy('old lady', 100, 2, 'tickle')
enemies = [assassin, baby]

# Set up helpers
oldLady = Helper('old lady')
gandalf = Helper('Gandalf')
angel = Helper('angel')
helpers = [oldLady, gandalf, angel]

stick = Weapon('stick', 5, 'sword', 0, 'Whack to your heart\'s content.') 
gun = Weapon('gun', 50, 'projectile', 100, '3expensive5me')  
cane = Weapon('cane', 6, 'sword', 5, 'The hidden power of old people everywhere')  
fist = Weapon('fist', 3, 'melee', 0, 'Ah...the sweetness of stealing a body part from your enemies...')  
sword = Weapon('sword', 40, 'sword', 80, 'Can slice even the most tough butter!')
knife = Weapon('knife', 10, 'sword', 50, 'Ouch.')

# Special weapons that baddies don't have:
grenade = Weapon('grenade', 10, 'bomb', 5, 'Throw it in your opponent\'s face!')

potato = Food('potato', 2, 2, 'Doesn\'t heal much, but it\'s nice and cheap.')
bread = Food('bread', 5, 5, 'Much more substantial food.')
healthPotion = Food('health potion', 80, 60, 'Will heal you right up--but it comes with a price.')

weapons = [knife, gun, cane, fist, sword]
helperItems = [potato, bread, healthPotion]
specialWeapons = [grenade]
peopleHelpers = [oldLady]

foodMerchant = Vendor('food merchant', '\nHello! Welcome to my food store.')
foodMerchant.goods = {bread: bread, potato: potato} # dict so index can be accessed by name
weaponTrader = Vendor('weapon trader', '\nI sell things to help you more efficiently kill people.')
weaponTrader.goods = {gun: gun, knife: knife, grenade: grenade}
vendors = [foodMerchant, weaponTrader]

argparser = argparse.ArgumentParser(description='A currently unnamed text-based game')
argparser.add_argument('-r', '--reset', help='Reset game', action='store_true')
argparser.add_argument('-l', '--load-game', help='Load existing game', action='store_true')
argparser.add_argument('-d', '--dev-mode', help='Start textbasedgame in Developer mode', action='store_true')
args = argparser.parse_args()

if args.reset:
    newGame()
elif args.load_game:
    loadGame()
elif args.dev_mode:
    devMode()
else:
    play()
