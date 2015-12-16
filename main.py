import time, random, sys

def choosePerson(wantedInfo):
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
    print()
    print('The ' + person + ' pulls out a(n) ' + weapon + ' threateningly.')
    time.sleep(1)
    if getBestInventoryWeapon() + playerPower > getWeaponPower(weapon) + peoplePower[person]:
        print('The ' + person + ' has been defeated!')
    elif getBestInventoryWeapon() == weaponPower[weapon]:
        print('Draw!')
    else:
        print('You\'re dead!')

assassin = "assassin"
oldlady = "old lady"
baby = "baby"

people = [oldlady, baby, assassin]
peoplePower = {oldlady: 1, baby: 1, assassin: 10}

knife = 'knife'
gun = 'gun'
cane = 'cane'
fist = 'fist'
sword = 'sword'

weapons = [knife, gun, cane, fist, sword]
peopleHelpers = []
weaponPower = {stick: 5, gun: 50, cane: 6, fist: 3, sword: 40, knife: 10}
inventory = [stick]
health = 100
coins = 100
playerPower = 5


personInteraction()
