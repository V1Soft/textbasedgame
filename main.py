#!/usr/bin/python3

import time, random, sys, shelve
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
        if input() == 'y':
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
        # hero.health -= weapon.power + person.power # Remove health from player
        hero.hit(weapon.power + person.power)
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

            elif command == 'inventory':
                for item in inventory:
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
        saveFile['playerPower'] = hero.power
        saveFile['coins'] = hero.money 
        saveFile['firstTime'] = False
        print('Progress saved.')
        sys.exit()
        
        
possibleCommands = ['help--show this message', 'interact--find another person to interact with',
                    'money--show amount of money', 'inventory--list inventory items', 'health--show health', 'quit--quit game',
                    'reset--reset progress']

hero = Player('nil', 100, 100, 9000)                       

assassin = Enemy('assassin', 10)
oldLady = Enemy('oldLady', 1)
baby = Enemy('baby', 1)

people = [oldLady, baby, assassin]
stick = Weapon('stick', 5) 
gun = Weapon('gun', 50)  
cane = Weapon('cane', 6)  
fist = Weapon('fist', 3)  
sword = Weapon('sword', 40)
knife = Weapon('knife', 10)

weapons = [knife, gun, cane, fist, sword] 
peopleHelpers = []                               
inventory = [stick]                              
                                                 
saveFile = shelve.open('savefile')
if len(sys.argv) < 2:
    print('arg error')
    sys.exit()
if sys.argv[1] == 'reset':
    inventory = [stick]
    health = 100
    coins = 100
    playerPower = float(5)
    print('New game set up. Welcome!')
    saveFile['firstTime'] = False
else:
    inventory = saveFile['inventory']
    health = saveFile['health']
    coins = saveFile['coins']
    playerPower = saveFile['playerPower']
    print('Previous game save loaded.')

commandLine()
