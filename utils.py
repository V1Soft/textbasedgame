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
    for choice in choices:
        print(str(i) + '. ' + choice)
        i += 1
    while True:
        descision = parse(prefix)
        try:
            if len(descision) > 0:
                if int(descision[0]) <= len(choices):
                    return [choices[int(descision[0])-1]]
                else:
                    print('Invalid Choice.')
        except ValueError:
            if descision[0] in choices:
                return descision
            else:
                if not getSpellCheck(descision[0], choices) == 0.0:
                    if confirm('Did you mean: ' + getSpellCheck(descision[0], choices), True):
                        fixedCommand = [getSpellCheck(descision[0], choices)]
                        for cmd in descision[1:]:
                            fixedCommand.append(cmd)
                        return fixedCommand
                else:
                    print('Invalid Choice.')

def listItems(prompt='', listedItems=[], objType=None):
    i = 0
    if objType is not None:
        for listedItem in listedItems:
            if isinstance(listedItem, objType):
                if isinstance(listedItem, obj.Weapon):
                    print(listedItem.name + ': Has ' + str(listedItem.power) + ' power')
                elif isinstance(listedItem, obj.Food):
                    print(listedItem.name + ': Restores ' + str(listedItem.hp) + ' health')
                else:
                    print(objType.name)
    else:
        for listedItem in listedItems:
            if isinstance(listedItem, obj.Weapon):
                print(listedItem.name + ': Has ' + str(listedItem.power) + ' power')
            elif isinstance(listedItem, obj.Food):
                print(listedItem.name + ': Restores ' + str(listedItem.hp) + ' health')
            else:
                print(str(i) + '. ' + listedItem)

def spellCheck(word, preset):
    similar = 0
    used = []
    if word == preset:
        return preset
    else:
        for char in preset or char.upper() in preset:
            if char in word or char.upper() in word and char not in used:
                similar += 1
            used.append(char)
        return (similar / len(preset)) * 100

def getSpellCheck(word, presets):
    greaterPreset = ''
    for preset in presets:
        if greaterPreset:
            if spellCheck(word, preset) > spellCheck(greaterPreset, preset):
                greaterPreset = preset
        else:
            greaterPreset = preset
    return greaterPreset

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
    while entities.player.health > 1 and entities.player.location.entity.health > 1:
        print('\nYour Health [ ', end='')
        i = 0
        while i != entities.player.health:
            print('#', end='')
            i += 1
        print(' ]\n\n', end='')
        interactExecute(parse('Interact'))
        if entities.player.location.entity == None:
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

def interactExecute(command):
        if command[0].upper() == 'HELP':
            listItems(prompt='Interact Commands:', listedItems=['help', 'auto', 'act', 'item', 'retreat'])
        elif command[0].upper() == 'AUTO':
            return
        elif command[0].upper() == 'ACT':
            print("You " + str(entities.player.location.entity.acts) + " the " + str(entities.player.location.entity.name) + ".")
            if entities.player.location.entity.acts == "pet":
                print("The " + str(entities.player.location.entity.name) + " runs away")
                return
            else:
                print("...But it didn't work")
                return
        elif command[0].upper() == 'ITEM':
            if len(command) == 3:
                listItems('Weapons:', entities.player.inventory, obj.Weapon)
                if command[1].upper() == 'EAT':
                    for item in entities.player.inventory:
                        if item.name == command[2]:
                            if isinstance(item, obj.Food):
                                entities.player.inventory.remove(item)
                                entities.player.health += item.hp
                                if entities.player.location.entity == entities.you:
                                    entities.player.location.entity.health += item.hp
                                print('%s points added to health!' % item.hp)
                                return
                            else:
                                print("You cannot eat that")
                                return
                elif command[1].upper() == 'USE':
                    for item in entities.player.inventory:
                        if item.name == command[2]:
                            if item.itemtype == 'bomb':
                                print("The " + item.name + " exploded")
                                print("The %s took %s damage!" % (entities.player.location.entity.name, item.power))
                                entities.player.location.entity.health -= item.power
                                entities.player.inventory.remove(item)
                                return
                            else:
                                print("The %s took %s damage!" % (entities.player.location.entity.name, item.power))
                                entities.player.location.entity.health -= item.power
                                # hero.inventory.remove(item)
                                return
                elif command[1].upper == 'THROW':
                    for item in entities.player.inventory:
                        if item.name == command[2]:
                            entities.player.inventory.remove(item)
                            print("You threw away the %s" % item.name)
                            return
                    return
                else:
                    print("Item command not found.")
            else:
                print('"item" requires 3 arguments. Maximum 4.')
        elif command[0].upper() == 'RETREAT':
            print('It cost 10 coins to retreat.')
            entities.player.spend(10)
            print("You ran away.")
            entities.player.location.entity = None
            return
        else:
            if not getSpellCheck(command[0], ['help', 'auto', 'act', 'item', 'retreat']) == 0.0:
                if confirm('Did you mean: ' + getSpellCheck(command[0], ['help', 'auto', 'act', 'item', 'retreat']), True):
                    fixedCommand = [getSpellCheck(command[0], ['help', 'auto', 'act', 'item', 'retreat'])]
                    for cmd in command[1:]:
                        fixedCommand.append(cmd)
                    interactExecute(fixedCommand)
            else:
                print('Interact Command: ' + command[0] + ' not found.')
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
            if len(command) == 2:
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
            else:
                print('Usage: info <item>')
        elif command[0].upper() == 'EXIT':
            print('You left the store.')
            entities.player.location.entity = entities.getLocation('Main')
            return
        elif command[0].upper() == 'HELP':
            entities.getHelpMsg('Market').printMsg()
        elif command[0].upper() == 'MONEY':
            print(entities.player.money + ' coins')
        else:
            print('Command not found.')

def parse(prefix=''):
    src = input(prefix + ' : ')
    parsedScript = []
    word = ''
    prevChar = ''
    inQuote = False
    inString = False
    for char in src:
        if char == ' ':
            if word:
                parsedScript.append(word)
                word = ''
        elif char == '\'' and not prevChar == '\\':
            inQuote = not inQuote
        elif char == '\"' and not prevChar == '\\':
            inString = not inString
        else:
            prevChar = char
            word += char
    if word:
        parsedScript.append(word)
    return parsedScript

def quitGame():
    print('\nSaving progress...')
    saveInfo(entities.player.name, 'player.' + entities.player.name, entities.player)
    saveInfo(entities.player.name, 'worldEntities', entities.worldEntities)
    try:
        saveInfo(entities.player.name, 'previousVendor', previousVendor)
    except NameError:
        saveInfo(entities.player.name, 'previousVendor', None)
    print('Progress saved.')
    exit(0)

def newGame():
    global usr
    usr = ''
    entities.worldEntities = []
    while not usr:
        try:
            usr = input('What is your desired username? : ')
        except KeyboardInterrupt:
            return
    entities.player = obj.Player(usr, 100, 100, float(5))
    entities.player.inventory = [entities.getWeapon('stick'), entities.getFood('potato')]
    entities.player.location = entities.getLocation('Main')
    print('New Game set up. Welcome.')
    locations.commandLine()

def loadGame():
    global usr, previousVendor
    try:
        users = []
        for file in os.listdir(fileDir + '/saves'):
            if (file.endswith('.save') or file.endswith('.save.dat')): 
                users.append(file.split('.')[0])
        try:
            usr = choose('List of users:', users, 'What is your username?')
        except KeyboardInterrupt:
            return
        entities.worldEntities = loadInfo(usr, 'worldEntities')
        entities.player = loadInfo(usr, 'player.' + usr)
        previousVendor = loadInfo(usr, 'previousVendor')
        print('Game save loaded.')
        try:
            if entities.player.location == entities.getLocation('Inventory'):
                locations.inventory()
            elif entities.player.location == entities.getLocation('Market'):
                utils.goToVendor(previousVendor)
            elif entities.player.location == entities.getLocation('Interact'):
                fight(entities.player.location.entity, entities.player.location.entity.weapon)
                #inventory()
        except KeyboardInterrupt or EOFError:
            quitGame()
        return
    except KeyError:
        print('Savefile does not exist or is broken. Creating new savefile...')
        newGame()

def execute(command):
    if command[0] == '?' or command[0].upper() == 'HELP':
        print('Possible commands:')
        entities.getHelpMsg('Main').printMsg()
    elif command[0].upper() == 'WHO':
        print('You are: ' + entities.player.name)
    elif command[0].upper() == 'QUIT':
        if confirm('Are you sure you want to quit?'):
            quitGame()
    elif command[0].upper() == 'RESET':
        if confirm('Are you sure you want to reset?'):
            newGame()
    elif command[0].upper() == 'GOTO':
        if len(command) == 2:
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
            print('Usage: goto <location>')
    else:
        if not getSpellCheck(command[0], ['help', 'who', 'quit', 'reset', 'goto']) == 0.0:
            if confirm('Did you mean: ' + getSpellCheck(command[0], ['help', 'who', 'quit', 'reset', 'goto']), True):
                fixedCommand = [getSpellCheck(command[0],  ['help', 'who', 'quit', 'reset', 'goto'])]
                for cmd in command[1:]:
                    fixedCommand.append(cmd)
                execute(fixedCommand)
        else:
            print('Command not found. Type "help" or "?" for help.')

# Get current file path
fileDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
