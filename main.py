import time, random, sys

def choosePerson(wantedInfo): # Choose person to interact with
    assert wantedInfo == 'person' or wantedInfo == 'item', 'Bad argument.'
    person = random.choice(people)
    item = random.choice(weapons)
    if wantedInfo == 'person':
        return person
    elif wantedInfo == 'item':
        return item


def getWeaponPower(item):
    return weaponPower[item]


def getBestInventoryWeapon():
    bestItemPower = 0
    for item in inventory:
        if getWeaponPower(item) > bestItemPower:
            bestItemPower = getWeaponPower(item)
    return bestItemPower


def personInteraction():
    newPerson = choosePerson('person')
    npi = choosePerson('item')
    print('You see a(n) ' + newPerson + ' in the distance. Do you choose to approach (y/n)?')
    time.sleep(2)
    if input() == 'y':
        fight(newPerson, npi)
    else:
        print()


def fight(person, weapon):
    global playerPower, inventory, coins, health
    personHealth = 100
    print('The ' + person + ' pulls out a(n) ' + weapon + ' threateningly.')
    time.sleep(1)

    while True:
        health -= getWeaponPower(weapon) + peoplePower[person] # Remove health from player
        personHealth -= getBestInventoryWeapon() + playerPower # Remove health of opponent
        if health < 1 and personHealth < 1:
            # In case of draw
            print('Draw!')
            break
        elif health < 1:
            # In case of loss
            print('You\'re dead!')
            removedItems = []
            for item in inventory:
               if random.randint(1, 2) == 1 and item != stick:
                   inventory.remove(item)
                   removedItems.append(item)
            printedItems = 0
            for item in removedItems:
                printedItems += 1
                if printedItems == len(removedItems):
                   print(item + ' dropped from inventory.')
                else:
                   print(item + ', ', end='')
            droppedCoins = random.randint(0, int(coins / 2))
            coins -= droppedCoins
            print('You dropped %s coins on your death.' %(droppedCoins))
            break
        elif personHealth < 1:
            # In case of win
            print('The ' + person + ' has been defeated!')
            powerToAdd = peoplePower[person] / 4
            playerPower += powerToAdd
            print('Your power level is now ' + str(playerPower))
            if random.randint(1, 2) == 1:
                inventory.append(weapon)
                print('%s added to inventory.' %(weapon))
            break





def commandLine():
    print('type "help" for help')
    while True:
        command = input('>> ')
        if command == 'help':
            print('Possible commands:')
            print('help--show this message\n'
                  'interact--find another person to interact with\n'
                  'money--show amount of money\n'
                  'inventory--list inventory items\n'
                  'health--show health')
        elif command == 'interact':
            personInteraction()
        elif command == 'money':
            print(coins)
        elif command == 'inventory':
            for item in inventory:
                print(item)
        elif command == 'health':
            print(health)

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
inventory = [stick]
health = 100
coins = 100
playerPower = 5

commandLine()