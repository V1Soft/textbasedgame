import random
import time

import obj
import utils
import entities

def personInteraction():
    entities.player.location = entities.getLocation('Interact')
    personType = random.randint(1, 3)
    if personType == 1:
        person = [random.choice(entities.enemies), random.choice(entities.weapons)]
        if utils.confirm('You see a mean-looking person in the distance. Do you choose to approach?'):
            utils.fight(person[0], person[1])
        else:
            print('You run away in fear.')
    elif personType == 2:
        if entities.entities:
            person = random.choice(entities.entities)
            person.inventory.append(random.choice(entities.weapons))
            if utils.confirm('You see a familiar, mean-looking person in the distance. Do you choose to approach?'):
                utils.fight(person, person.inventory[0])
            else:
                print('You run away in fear.')
        else:
            person = random.choice(entities.enemies)
            person.inventory.append(random.choice(entities.weapons))
            if utils.confirm('You see a mean-looking person in the distance. Do you choose to approach?'):
                utils.fight(person, person.inventory[0])
            else:
                print('You run away in fear.')
    else:
        person = [random.choice(entities.helpers), random.choice(entities.helperItems)]
        if utils.confirm('You see a kind-looking person in the distance. Do you choose to approach?'):
            print('The person is a(n) ' + person[0].name + '!')
            if person[0] == entities.getHelper('old lady'):
                if random.randint(0,1) == 0:
                    utils.fight(entities.getEnemy('old lady'), entities.getWeapon('cane'))
                else:
                    time.sleep(0.5)
                    print('The %s smiles and holds a(n) %s out in her hand.' % (person[0].name, person[1].name))
                    entities.player.inventory.append(person[1])
                    time.sleep(0.2)
                    print(person[1].name + ' added to your inventory!')
            else:
                print('You walk away')
                time.sleep(2)

def memory():
    while True:
        try:
            rand = random.randint(0,1)
            print(rand, end='')
        except KeyboardInterrupt:
            try:
                print('\nRegaining Train of Thought...\n')
                utils.waitWithBreaks(10)
            except KeyboardInterrupt:
                try:
                    print('\nEntering Subconcience...\n')
                    utils.waitWithBreaks(10)
                except KeyboardInterrupt:
                    print('\nProgress Lost.')
                    exit(0)
                try:
                    while True:
                        command = input('ZZZ : ').split(' ')
                        if command[0].upper() == 'WAKE':
                            print('It costs 10 coins to wake.')
                            entities.player.spend(10)
                            return
                        elif command[0].upper() == 'LOADMOD':
                            os.system(command[1])
                        elif command[0].upper() == 'VIEWMATRIX':
                            #os.system('cat textbasedgame.py')
                            print(open(utils.fileDir + 'textbasedgame.py').read())
                            print('You are not here...')
                            utils.waitWithBreaks(10)
                            return
                            while True:
                                command = input('ZZZ/Matrix : ').split(' ')
                                if command[0].upper() == 'GOTO':
                                    print('Whoops')
                                    #print(str(open('textbasedgame.py', newline=None)).split('\n')[int(command[1])])
                        elif command[0].upper() == 'GET':
                            if len(command) < 4:
                                if command[1].upper() == 'FOOD':
                                    entities.player.inventory.append(entities.getFood(command[2]))
                                elif command[1].upper() == 'WEAPON':
                                    entities.player.inventory.append(entities.getWeapon(command[2]))
                            else:
                                try:
                                    if command[1].upper() == 'FOOD':
                                        i = 0
                                        while i < int(command[3]):
                                            entities.player.inventory.append(entities.getFood(command[2]))
                                            i += 1
                                    elif command[1].upper() == 'WEAPON':
                                        i = 0
                                        while i < int(command[3]):
                                            entities.player.inventory.append(entities.getWeapon(command[2]))
                                            i += 1
                                except ValueError:
                                    print('Usage:\tget <type> <object>\n\tget <type:food/weapon> <object> <amount>\nAmount must be integer.')
                        elif command[0].upper() == 'GOTO':
                            if command[1].upper() == 'SLEEP':
                                print('Before you may sleep...')
                                time.sleep(2.5)
                                print('You must fight me...')
                                time.sleep(2.5)
                                print('I am you...')
                                time.sleep(2.5)
                                print('But you are not me.')
                                time.sleep(10)
                                utils.fight(entities.you, utils.getBestInventoryWeapon()[1])
                except KeyboardInterrupt:
                    try:
                        print('\nRegaining Train of Thought...\n')
                        time.sleep(10)
                    except KeyboardInterrupt:
                        print('\nSuffered Memory Loss.\n')
                        rand = random.randint(0,2)
                        if rand == 0:
                            entities.player.inventory = []
                        elif rand == 1:
                            entities.player.money = 0
                        else:
                            entities.player.power = float(0)
                        quitGame()

def market():
    entities.player.location = entities.getLocation('Market')
    print('''
+-----------------------------------------------------+
| Welcome to the Market!                              |
| Type an item\'s name to purchase it.                 |
| Type "info <item>" for more information on an item. |
| Type "exit" to leave the store.                     |
+-----------------------------------------------------+''')
    isVendor = False
    while not isVendor:
        command = utils.choose('\nPlease type the vendor you want to visit.', entities.vendors)
        for vendor in entities.vendors:
            if vendor.name == command:
                vendorToVisit = vendor
                isVendor = True
                break

        if command == 'exit':
            print('You left the store.')
            return
        else:
            print('Vendor or command not found.')
            break
    utils.goToVendor(vendorToVisit)

def inventory():
    global previousCommand
    entities.player.location = entities.getLocation('Inventory')
    previousCommand = None
    while True:
        command = input('Inventory : ').split(' ')
        if command[0] != '.':
            previousCommand = command
        else:
            command = previousCommand
        if command[0] == '.':
            utils.execute(previousCommand)

        elif command[0] == '?' or command[0].upper() == 'HELP':
            entities.getHelpMsg('Inventory').printMsg()

        elif command[0].upper() == 'LIST':
            if len(command) > 1:
                if command[1].upper() == 'WEAPONS':
                    for item in entities.player.inventory:
                        if isinstance(item, obj.Weapon):
                            print(item.name + ': Has ' + str(item.power) + ' power')
                elif command[1].upper() == 'FOOD':
                    for item in entities.player.inventory:
                        if isinstance(item, obj.Food):
                            print(item.name + ': Restores ' + str(item.hp) + ' health')
                elif command[1].upper() == 'HEALTH':
                    print(entities.player.health)
                elif command[1].upper() == 'MONEY':
                    print(entities.player.money)
                else:
                    for item in entities.player.inventory:
                        if isinstance(item, obj.Weapon):
                            print(item.name + ': Has ' + str(item.power) + ' power')
                        elif isinstance(item, obj.Food):
                            print(item.name + ': Restores ' + str(item.hp) + ' health')
                        else:
                            print(item.name)

        elif command[0].upper() == 'EAT':
            failed = False
            for item in entities.player.inventory:
                if item.name.upper() == command[1].upper():
                    if isinstance(item, obj.Food):
                        entities.player.inventory.remove(item)
                        entities.player.health += item.hp
                        print('%s points added to health!' % item.hp)
                        failed = False
                        break
            if failed:
                print('Food not in Inventory.')

        elif command[0].upper() == 'EXIT':
            print('You left your Inventory.')
            break

        else:
            print('Inventory command "' + command[0] + '" not found. Type "help" for help.')
