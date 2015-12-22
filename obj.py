class Player(object):
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
    def __init__(self, name, power):
        self.name = name
        self.power = power

class Enemy(object):
    def __init__(self, name, health,  power):
        self.name = name
        self.power = power
        self.health = health

class Vendor(object):
    goods = {}

    def __init__(self, name):
        self.name = name

    def say(self, thing):
        for item in thing:
            print(item)
        return item

class Food(object):
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

if __name__ == '__main__':
    print('wrong one, buddy')
