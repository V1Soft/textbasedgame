#!/usr/bin/python3

import time, random, sys, shelve

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
        weapPwr = weaponPower[weapon]
        if weapPwr > bestItemPower:
            bestItemPower = weapPwr
    return bestItemPower


def personInteraction():
    newPerson = choosePerson('person')
    npi = choosePerson('item')
    print('You see a(n) ' + newPerson + ' in the distance. Do you choose to approach (y/n)?')
    time.sleep(2)
    while True:
        if input() == 'y':
            fight(newPerson, npi)
            break

        else:
            print()
            break


def fight(person, weapon):
    global playerPower, inventory, coins, health
    personHealth = 100
    time.sleep(0.5)
    print('The ' + person + ' pulls out a(n) ' + weapon + ' threateningly.')
    time.sleep(1)
    while True:
        health -= weaponPower[weapon] + peoplePower[person] # Remove health from player
        personHealth -= getBestInventoryWeapon() + playerPower # Remove health of opponent
        if health - (weaponPower[weapon] + peoplePower[person]) < 1 and personHealth - (getBestInventoryWeapon() + playerPower) < 1:
            # In case of draw
            time.sleep(0.2)
            print('You somehow managed to escape with %s health remaining.' %(health))
            break

        elif health < 1:
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
                   print(item + ' dropped from inventory.')

                else:
                   print(item + ', ', end='')

            droppedCoins = random.randint(0, int(coins / 2))
            coins -= droppedCoins
            time.sleep(0.2)
            print('You dropped %s coins on your death.' %(droppedCoins))
            break
        elif personHealth < 1:
            # In case of win
            print('The ' + person + ' has been defeated!')
            powerToAdd = peoplePower[person] / 4
            playerPower += powerToAdd
            time.sleep(0.2)
            print('Your power level is now ' + str(playerPower))
            if random.randint(1, 2) == 1:
                inventory.append(weapon)
                time.sleep(0.2)
                print('%s added to inventory.' %(weapon))
            coinsToAdd = peoplePower[person] * 5 + random.randint(-4, 4) # Dropped coins is opponent pwr * 5 + randint
            coins += coinsToAdd
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
                print(coins)

            elif command == 'inventory':
                for item in inventory:
                    print(item)

            elif command == 'health':
                print(health)
            
            elif command == 'quit':
                print('Are you sure you want to quit? Your progress will be saved.')
                if input() == 'y':
                    quitGame()
                else:
                    print('Cancelled.')
         
            elif command == 'reset':
                saveFile['firstTime'] = True
            else:
                print('Command not found. Type "help" for help.')
            if saveFile['firstTime']:
                inventory = [stick]
                health = 100
                coins = 100
                playerPower = float(5)
                print('New game set up. Welcome!')
                saveFile['firstTime'] = False
        except KeyboardInterrupt:
            quitGame()

def quitGame():
        print('Saving progress...')
        saveFile['inventory'] = inventory
        saveFile['health'] = health
        saveFile['playerPower'] = playerPower
        saveFile['coins'] = coins
        saveFile['firstTime'] = False
        print('Progress saved.')
        sys.exit()
        
        
possibleCommands = ['help--show this message', 'interact--find another person to interact with',
                    'money--show amount of money', 'inventory--list inventory items', 'health--show health', 'quit--quit game',
                    'reset--reset progress']

assassin = "assassin"
oldLady = "old lady"
baby = "baby"

people = [oldLady, baby, assassin]
peoplePower = {oldLady: 1, baby: 1, assassin: 10}

knife = 'knife'
gun = 'gun'
cane = 'cane'
fist = 'fist'
sword = 'sword'
stick = 'stick'

weapons = [knife, gun, cane, fist, sword]
peopleHelpers = []
weaponPower = {stick: 5, gun: 50, cane: 6, fist: 3, sword: 40, knife: 10}

saveFile = shelve.open('savefile')

if not saveFile['firstTime']:
    inventory = saveFile['inventory']
    health = saveFile['health']
    coins = saveFile['coins']
    playerPower = saveFile['playerPower']
    print('Previous game save loaded.')

commandLine()
