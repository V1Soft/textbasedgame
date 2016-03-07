# Player Class
class Player(object):
    def __init__(self, name, health, money, power):
        self.name = name
        self.health = health
        self.money = money
        self.power = power
        #self.language = None
        self.inventory = []
        self.location = None

    # Decrease Health
    def hit(self, amount):
        if amount > self.health:
            return ValueError
        self.health -= amount
        return self.health

    # Decrease Money
    def spend(self, amount):
        if amount > self.money:
            raise RuntimeError
        self.money -= amount
        return self.money

    # Increase Money
    def receive(self, amount):
        self.money += amount
        return self.money

    # Increase Power
    def gain(self, amount):
        self.power += amount
        return self.power

# Weapon Class
class Weapon(object):
    def __init__(self, name, power, itemtype, cost, description):
        self.name = name
        self.power = power
        self.cost = cost
        self.description = description
        self.itemtype = itemtype

# Enemy Class
class Enemy(object):
    def __init__(self, name, health, power, acts):
        self.name = name
        self.power = power
        self.health = health
        self.money = 0
        self.inventory = []
        self.acts = acts


    # def addToInventory(item):
    #     self.inventory.append(item)

# Helper Class
class Helper(object):
    def __init__(self, name):
        self.name = name

# Vendor Class
class Vendor(object):
    def __init__(self, name, message, goods):
        self.name = name
        self.message = message
        self.goods = goods

    # Print Goods
    def say(self, thing):
        for item in thing:
            print(item.name + ': ' + str(item.cost) + ' money')
        return item

# Food Class
class Food(object):
    def __init__(self, name, hp, cost, description):
        self.name = name
        self.hp = hp
        self.cost = cost
        self.description = description

# Location Class
class Location(object):
    def __init__(self, name, description, entity): # Save Location in Battle
        self.name = name
        self.description = description
        self.entity = entity

# Help Message Class
class HelpMsg(object):
    def __init__(self, name, commands):
        assert type(commands) == list, 'Commands must be in a list'
        self.name = name
        self.commands = commands

    # Print Message
    def printMsg(self):
        for command in self.commands:
            print('\t' + command)

# This file should not be executed
if __name__ == '__main__':
    print('Go away.')
