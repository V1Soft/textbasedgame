from obj import *
import argparse

player = Player('nil', 100, 100, 10)

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

foodMerchant = Vendor('food merchant', '\nHello! Welcome to my food store.')
foodMerchant.goods = {bread: bread, potato: potato}  # dict so index can be accessed by name
weaponTrader = Vendor('weapon trader', '\nI sell things to help you more efficiently kill people.')
weaponTrader.goods = {gun: gun, knife: knife, grenade: grenade}
vendors = [foodMerchant, weaponTrader]

argparser = argparse.ArgumentParser(description='A currently unnamed text-based game')
argparser.add_argument('-r', '--reset', help='Reset game', action='store_true')
argparser.add_argument('-l', '--load-game', help='Load existing game', action='store_true')
argparser.add_argument('-d', '--dev-mode', help='Start textbasedgame in Developer mode', action='store_true')
args = argparser.parse_args()

# Locations

locationMain = Location('Main', 'Where it all begins.', None)
locationInventory = Location('Inventory', 'Your Inventory.', None)
locationMarket = Location('Market', 'The Market.', None)
# locationMarketFood = Location('Food Store', 'Hello! Welcome to my food store.', foodMerchant)
# locationMarketFood = Location('Weapons Shop', 'I sell things to help you more efficiently kill people.', weaponsTrader)
locationInteract = Location('Interact', 'Interact with your Surroundings.', None)

# Help messages

clHelp = HelpMsg(['help--show this message',
                  'goto--goto <location>, ex. goto inventory',
                  'quit--quit game',
                  'reset--reset progress'])
inventoryHelp = HelpMsg(['help--show this message',
                         'list <food/money/weapons/health>--list wanted information',
                         'eat <food>--eat food and restore health',
                         'exit--leave inventory'])
storeHelp = HelpMsg(['help--show this message',
                     '<item>--buy item',
                     'money--print available money',
                     'info <item>--give info on item',
                     'exit--leave the store'])

if __name__ == '__main__':
    print('Go away.')
