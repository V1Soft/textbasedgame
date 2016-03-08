import argparse

import obj

worldEntities = []

player = obj.Player('nil', 100, 100, 10)

# Weapons:
weapons = [obj.Weapon('stick', 5, 'sword', 0, 'Whack to your heart\'s content.'), obj.Weapon('knife', 10, 'sword', 50, 'Ouch.'), obj.Weapon('gun', 50, 'projectile', 100, '3expensive5me'), obj.Weapon('cane', 6, 'sword', 5, 'The hidden power of old people everywhere'), obj.Weapon('fist', 3, 'melee', 0, 'Ah...the sweetness of stealing a body part from your enemies...'), obj.Weapon('sword', 40, 'sword', 80, 'Can slice even the most tough butter!')]
def getWeapon(name):
    for weapon in weapons:
        if weapon.name == name:
            return weapon
    print('Weapon ' + name + ' not found.')

# Special weapons that baddies don't have:
specialWeapons = [obj.Weapon('grenade', 10, 'bomb', 5, 'Throw it in your opponent\'s face!')]
def getSpecialWeapon(name):
    for specialWeapon in specialWeapons:
        if specialWeapon.name == name:
            return specialWeapon
    print('Weapon '+ name +' not found.')

# Foods:
foods = [obj.Food('potato', 2, 2, 'Doesn\'t heal much, but it\'s nice and cheap.'), obj.Food('bread', 5, 5, 'Much more substantial food.'), obj.Food('health potion', 80, 60, 'Will heal you right up--but it comes with a price.')]
def getFood(name):
    for food in foods:
        if food.name == name:
            return food
    print('Food ' + name + ' not found.')

# Set up enemies
enemies = [obj.Enemy('assassin', 100, 10, "pet"), obj.Enemy('baby', 100, 1, "pet"), obj.Enemy('old lady', 100, 2, 'tickle')]
def getEnemy(name):
    for enemy in enemies:
        if enemy.name == name:
            return enemy
    print('Enemy ' +  + ' not found.')

# Set up helpers
helpers = [obj.Helper('old lady'), obj.Helper('Gandalf'), obj.Helper('angel')]
helperItems = [getFood('potato'), getFood('bread'), getFood('health potion')]
def getHelper(name):
    for helper in helpers:
        if helper.name == name:
            return helper
    print('Helper ' + name + ' not found.')

# Set up memory characters
you = obj.Enemy('You', player.health, player.power, None)

# Vendors:
vendors = [obj.Vendor('food merchant', '\nHello! Welcome to my food store.', [getFood('bread'), getFood('potato')]), obj.Vendor('weapon trader', '\nI sell things to help you more efficiently kill people.', [getWeapon('gun'), getWeapon('knife'), getSpecialWeapon('grenade')])]
def getVendor(name):
    for vendor in vendors:
        if vendor.name == name:
            return vendor
    print('Vendor ' + name + ' not found.')


# Locations
locations = [obj.Location('Main', 'Where it all begins.', None), obj.Location('Inventory', 'Your Inventory.', None), obj.Location('Market', 'The Market.', None), obj.Location('Interact', 'Interact with your Surroundings.', None)]
def getLocation(name):
    for location in locations:
        if location.name == name:
            return location
    print('Location ' + name + ' not found')

# Help messages
helpMsgs = [obj.HelpMsg('Main', ['help--show this message', 'goto--goto <location>, ex. goto inventory', 'quit--quit game', 'reset--reset progress']), obj.HelpMsg('Inventory', ['help--show this message', 'list <food/money/weapons/health>--list wanted information', 'eat <food>--eat food and restore health', 'exit--leave inventory']), obj.HelpMsg('Market', ['help--show this message', '<item>--buy item', 'money--print available money', 'info <item>--give info on item', 'exit--leave the store'])]
def getHelpMsg(name):
    for helpMsg in helpMsgs:
        if helpMsg.name == name:
            return helpMsg
    print('Help Message ' + name + ' not found.')

