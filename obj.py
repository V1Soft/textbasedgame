class Player(object):
    lv = 0
    def __init__(self, name, health, money, power):
        self.name = name
        self.health = health
        self.money = money
        self.power = power

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
        self.acts = acts
        
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

if __name__ == '__main__':
    pass
