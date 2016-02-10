class Player(object):
    def __init__(self, name, health, money, power):
        self.name = name
        self.health = health
        self.money = money
        self.power = power
        self.language = None
        self.previousCommand = None
        self.inventory = []
        self.location = None


    def hit(self, amount):
        if amount > self.health:
            return ValueError
        self.health -= amount
        return self.health


    def spend(self, amount):
        if amount > self.money:
            raise RuntimeError
        self.money -= amount
        return self.money


    def receive(self, amount):
        self.money += amount
        return self.money


    def gain(self, amount):
        self.power += amount
        return self.power


class Weapon(object):
    def __init__(self, name, power, itemtype, cost, description):
        self.name = name
        self.power = power
        self.cost = cost
        self.description = description
        self.itemtype = itemtype


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


class Helper(object):
    def __init__(self, name):
        self.name = name


class Vendor(object):
    goods = {}

    def __init__(self, name, message):
        self.name = name
        self.message = message


    def say(self, thing):
        for item in thing:
            print(item.name + ': ' + str(item.cost) + ' money')
        return item


class Food(object):
    def __init__(self, name, hp, cost, description):
        self.name = name
        self.hp = hp
        self.cost = cost
        self.description = description


class Location(object):
    def __init__(self, name, description, entity): # Save Location in Battle
        self.name = name
        self.description = description
        self.entity = entity


class HelpMsg(object):
    def __init__(self, commands):
        assert type(commands) == list, 'Commands must be in a list'
        self.commands = commands


    def prtMsg(self):
        for command in self.commands:
            print(command)


if __name__ == '__main__':
    print()
