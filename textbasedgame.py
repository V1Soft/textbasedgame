#!/usr/bin/python3

import time, random, sys, shelve
from obj import *

def choosePerson(wantedInfo): # Choose person to interact with
    assert wantedInfo == 'person' or wantedInfo == 'item', 'Bad argument.'
    person = random.choice(people)
    if isinstance(person, Enemy):
        item = random.choice(weapons)
    elif isinstance(person, Helper):
        item = random.choice(helperItems)
    if wantedInfo == 'person':
        return person

    elif wantedInfo == 'item':
        return item


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
    newPerson = choosePerson('person')
    npi = choosePerson('item')
    print('You see a(n) ' + str(newPerson.name) + ' in the distance. Do you choose to approach (y/n)?')
    time.sleep(2)
    while True:
        if input().upper() == 'Y':
            if isinstance(newPerson, Enemy):
                fight(newPerson, npi)
            else:
                time.sleep(0.5)
                print('The %s smiles and holds a(n) %s out in her hand.' %(newPerson.name, npi.name))
                inventory.append(npi)
                time.sleep(0.2)
                print(npi.name + ' added to your inventory!')
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
    def goToVendor(vendor):
        print(vendor.message)
        print('Type an item\'s name to purchase it.')
        print('Type "info <item>" for more information on an item.')
        print('Type "exit" to leave the store.')
        print('Items for sale:')
        vendor.say(vendor.goods)
        while True:
                command = input(': ')
                commandRun = False
                thingToBuy = None
                for good in vendor.goods:
                    if good.name == command:
                        thingToBuy = good
                        break
                if thingToBuy == None:
                    print('Item not found.')
                else:
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
                        print('Healing power: %s' %(item.hp))
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
    global saveFile, inventory
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
                    saveFile['firstTime'] = True
                else:
                    print('Cancelled.')
            elif command.startswith('eat'):
                foodToEat = command[4:] # Get food out of command string
                for item in inventory:
                    if item.name == foodToEat:
                        inventory.remove(item)
                        hero.health += item.hp
                        print('%s points added to health!' %(item.hp))
                        failed = False
					
                if failed != False:
                    print('Food not in inventory.')
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
    global inventory
    inventory = [stick, potato]
    hero.health = 100
    hero.money = 100
    hero.power = float(5)
    print('New game set up. Welcome!')
    saveFile['firstTime'] = False
    commandLine()
    

def loadGame():
    global inventory
    inventory = saveFile['inventory']
    hero.health = saveFile['health']
    hero.money = saveFile['money']
    hero.power = saveFile['heroPower']
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
                    'reset--reset progress', 'eat <food>--consume food and restore health']

hero = Player('nil', 100, 100, 9000)                       

assassin = Enemy('assassin', 100, 10)
oldLady = Helper('old lady')
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
healthPotion = Food('health potion', 20, 50)

weapons = [knife, gun, cane, fist, sword]
helperItems = [potato, bread, healthPotion]
peopleHelpers = []                               

foodMerchant = Vendor('food merchant', 'Hello! Welcome to my food store.')
foodMerchant.goods = {bread: bread, potato: potato} # dict so index can be accessed by name
vendors = [foodMerchant]            
                                                 
saveFile = shelve.open('savefile')

if len(sys.argv) < 2:
    play()
elif sys.argv[1] == 'reset':
    newGame()
elif sys.argv[1] == 'continue':
    loadGame()

commandLine()
