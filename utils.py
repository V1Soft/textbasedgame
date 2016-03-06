import inspect
import os
import curses
import shelve
import random
import time

import obj
import locations
import entities

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

def choose(prompt='', choices=[], prefix='', default=True):
    i = 1
    print(prompt)
    if default:
        for choice in choices:
            if i == len(choices) - 1:
                print(str(i) + '. ' + choice + ' or')
            else:
                print(str(i) + '. ' + choice)
            i += 1
        while True:
            if prefix:
                descision = input(prefix + ' : ')
            else:
                descision = input(': ')
            try:
                if int(descision) <= len(choices):
                    return choices[int(descision)-1]
                else:
                    print('Invalid Choice.')                    
            except ValueError:
                if descision in choices:
                    return descision
                else:
                    print('Invalid Choice.')
    else:
        for choice in choices:
            if i == len(choices) - 1:
                print(str(i) + '. ' + choice[0] + ' (' + choice[1] + ') or')
            else:
                print(str(i) + '. ' + choice[0] + ' (' + choice[1] + ')')
            i += 1
        if prefix:
            descision = input(prefix + ' : ')
        else:
            descision = input(': ')
            try:
                return choices[int(descision)-1][1].upper()
            except ValueError:
                return descision.upper()

def getBestInventoryWeapon():
    bestItemPower = 0
    bestItem = None
    for item in entities.player.inventory:
        if isinstance(item, obj.Weapon):
            weapPwr = item.power
            if weapPwr > bestItemPower:
                bestItemPower = weapPwr
                bestItem = item
    return bestItemPower, bestItem

def fight(person, weapon):
    entities.player.location.entity = person
    time.sleep(0.5)
    print('The ' + str(entities.player.location.entity.name) + ' pulls out a(n) ' + str(weapon.name) + ' threateningly.')
    time.sleep(1)
    if isinstance(weapon, obj.Food):  # Code no longer relevant
        print("...So you took the " + str(weapon.name) + " and ate it")
        entities.player.health += weapon.hp
        if entities.player.location.entity == entities.you:
            entities.player.location.entity.health += weapon.hp
        print("The " + str(entities.player.location.entity.name) + " ran away")
        commandLine()
    for choice in ['auto', 'act', 'item', 'retreat']:
        print(choice)
    while entities.player.health > 1 and entities.player.location.entity.health > 1:
        print('\nYour Health [ ', end='')
        i = 0
        while i != entities.player.health / 10:
            print('#', end='')
            i += 1
        print(' ]\n\n', end='')
        command = input('Interact : ').split(' ')
        if command[0] == "1" or command[0].upper() == "AUTO":
            break
        elif command[0] == "2" or command[0].upper() == "ACT":
            print("You " + str(entities.player.location.entity.acts) + " the " + str(entities.player.location.entity.name) + ".")
            if entities.player.location.entity.acts == "pet":
                print("The " + str(entities.player.location.entity.name) + " runs away")
                textbasedgame.commandLine()
            else:
                print("...But it didn't work")
                break
        elif command[0] == '3' or command[0].upper() == 'ITEM':
            for item in entities.player.inventory:
                if item in weapons or item in entities.specialWeapons:
                    print(item.name)
            if command[1] == 'eat':
                for item in entities.player.inventory:
                    if item.name == command[2]:
                        if isinstance(item, obj.Food):
                            entities.player.inventory.remove(item)
                            entities.player.health += item.hp
                            if entities.player.location.entity == entities.you:
                                entities.player.location.entity.health += item.hp
                            print('%s points added to health!' % item.hp)
                            break
                        else:
                            print("You cannot eat that")
                            break
            elif command[1] == 'use':
                for item in entities.player.inventory:
                    if item.name == command[2]:
                        if item.itemtype == 'bomb':
                            print("The " + item.name + " exploded")
                            print("The %s took %s damage!" % (entities.player.location.entity.name, item.power))
                            entities.player.location.entity.health -= item.power
                            entities.player.inventory.remove(item)
                            break
                        else:
                            print("The %s took %s damage!" % (entities.player.location.entity.name, item.power))
                            entities.player.location.entity.health -= item.power
                            # hero.inventory.remove(item)
                            break
            elif command[1] == 'throw':
                for item in entities.player.inventory:
                    if item.name == command[2]:
                        entities.player.inventory.remove(item)
                        print("You threw away the %s" % item.name)
                        break
                break
            else:
                print("Item command not found.")
        elif command[0] == "4" or command[0].upper() == "RETREAT":
            print("You ran away.")
            entities.player.location.entity = None
            return
    while True:
        entities.player.hit(weapon.power + entities.player.location.entity.power)  # Remove health from player
        entities.player.location.entity.health -= getBestInventoryWeapon()[0] + entities.player.power  # Remove health of opponent
        if entities.player.health - (weapon.power + entities.player.location.entity.power) < 1 and entities.player.location.entity.health - (getBestInventoryWeapon()[0] + entities.player.power) < 1:
            # In case of draw
            time.sleep(0.2)
            print('You somehow managed to escape with %s health remaining.' % entities.player.health)
            entities.worldEntities.append(entities.player.location.entity)
            entities.player.location.entity = None
            break

        elif entities.player.health < 1:
            # In case of loss
            time.sleep(0.2)
            print('You\'re dead!')
            for item in entities.player.inventory:
                if random.randint(1, 2) == 1 and item != stick:
                    entities.player.inventory.remove(item)
#                    player.location.entity.inventory.append(removedItems)
                    print(str(item) + ' dropped from inventory.')
            droppedCoins = random.randint(0, int(entities.player.money / 2))
            entities.player.spend(droppedCoins)
            time.sleep(0.2)
            print('You dropped %s coins on your death.' % droppedCoins)
            entities.player.location.entity.money += droppedCoins
            worldEntities.append(entities.player.location.entity)
            entities.player.location.entity = None
            break
        elif entities.player.location.entity.health < 1:
            # In case of win
            print('The ' + str(entities.player.location.entity.name) + ' has been defeated!')
            powerToAdd = entities.player.location.entity.power / 4
            entities.player.gain(powerToAdd)
            time.sleep(0.2)
            print('Your power level is now ' + str(entities.player.power))
            if random.randint(1, 2) == 1:
                for item in entities.player.location.entity.inventory:
                    entities.player.inventory.append(item)
                    entities.player.location.entity.inventory.remove(item)
                time.sleep(0.2)
                print('%s added to inventory.' % weapon.name)
            coinsToAdd = entities.player.location.entity.power * 5 + random.randint(-4, 4)  # Dropped coins is opponent pwr * 5 + randint
            entitis.player.receive(coinsToAdd)
            time.sleep(0.2)
            print('Opponent dropped %s coins' % coinsToAdd)
            entities.player.location.entity = None
            break

def saveInfo(username, name, info):
    saveFile = shelve.open(fileDir + '/saves/%s.save' % username)
    saveFile[name] = info
    saveFile.close()

def loadInfo(username, wantedInfo):
    saveFile = shelve.open(fileDir + '/saves/%s.save' % username)
    info = saveFile[wantedInfo]
    return info

def goToVendor(vendor):
    global previousVendor, previousCommand
    previousVendor = vendor
    previousCommand = None
    entities.player.location = entities.getLocation('Market')
    entities.player.location.entity = vendor
    print('%s\nItems for sale:' % vendor.message)
    vendor.say(vendor.goods)
    while True:
        command = input('Market > %s : ' % vendor.name).split(' ')
        thingToBuy = None
        buying = False
        if command[0] != '.':
            previousCommand = command
        else:
            command = previousCommand
        for good in vendor.goods:
            if good.name == command[0]:
                thingToBuy = good
                buying = True
                break
        if buying:
            entities.player.inventory.append(thingToBuy)
            entities.player.spend(thingToBuy.cost)
            print('%s purchased for %s money.' % (thingToBuy.name, thingToBuy.cost))
        elif command[0].upper() == 'INFO':
            thingToGetInfoOn = command[1]
            itemInShop = False
            for item in vendor.goods:
                if item.name == thingToGetInfoOn:
                    itemInShop = True
                    break
            if not itemInShop:
                print('Item not found.')
            else:
                if isinstance(item, obj.Weapon):
                    print('Power: %s' % item.power)
                elif isinstance(item, obj.Food):
                    print('Healing power: %s' % item.hp)
                print('Description: ' + item.description)
        elif command[0].upper() == 'EXIT':
            print('You left the store.')
            entities.player.location.entity = entities.getLocation('Main')
            return
        elif command[0].upper() == 'HELP':
            storeHelp.prtMsg()
        elif command[0].upper() == 'MONEY':
            print(entities.player.money + ' coins')
        else:
            print('Command not found.')

def execute(command):
    if command[0] == '?' or command[0].upper() == 'HELP':
        print('Possible commands:')
        entities.getHelpMsg('Main').printMsg()
    elif command[0].upper() == 'GOTO':
        if command[1].upper() == 'INTERACT':
            locations.personInteraction()
        elif command[1].upper() == 'MARKET':
            print('Going to market...')
            locations.market()
        elif command[1].upper() == 'INVENTORY':
            print('Entering Inventory...')
            locations.inventory()
        elif command[1].upper() == 'MEMORY':
            locations.memory()
        else:
            print('Location not found.')
    else:
        print('Command not found. Type "help" or "?" for help.')

# Get current file path
fileDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
