#!/usr/bin/python3

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
        print('You see a kind-looking person in the distance. Do you choose to approach (y/n)?')
    else:
        print('You see a mean-looking person in the distance. Do you choose to approach (y/n)?')
    time.sleep(2)
    while True:
        if input().upper() == 'Y':
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
    while True:
        command = input(": ")
        if command == "1" or command.upper() == "FIGHT":
            continue
        elif command == "2" or command.upper() == "ACT":
            print("You " +  str(person.acts) + " the " + str(person.name) + ".")
            if person.acts == "pet":
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
                            print("The %s took %s damage!" %(person.name, item.power))
                            person.health -= item.power
                            inventory.remove(item)
                            break
            elif command.startswith('throw'):
                tothrow = command[6:]
                for item in inventory:
                    if item.name == tothrow:
                        inventory.remove(item)
                        print("You threw away the %s" %(item.name))
                        break
                break
            else:
                print("It does not seem you have that item")
                break
        elif command == "4" or command.upper() == "SPARE":
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
                    saveFile['firstTime'] = True
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
        saveFile['inventory'] = inventory
        saveFile['health'] = hero.health
        saveFile['heroPower'] = hero.power
        saveFile['money'] = hero.money 
        saveFile['firstTime'] = False
        saveFile.close()
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
    try:
        inventory = saveFile['inventory']
        hero.health = saveFile['health']
        hero.money = saveFile['money']
        hero.power = saveFile['heroPower']
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
                    choice = input('Invalid option: Do you want to quit (Y/n) ')
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

foodMerchant = Vendor('food merchant', 'Hello! Welcome to my food store.')
foodMerchant.goods = {bread: bread, potato: potato} # dict so index can be accessed by name
weaponTrader = Vendor('weapon trader', 'I sell things to help you more efficiently kill people.')
weaponTrader.goods = {gun: gun, knife: knife, grenade: grenade}
vendors = [foodMerchant, weaponTrader]            
                                                 
saveFile = shelve.open('savefile')

if len(sys.argv) < 2:
    play()
elif sys.argv[1] == 'reset':
    newGame()
elif sys.argv[1] == 'continue':
    loadGame()

commandLine()
