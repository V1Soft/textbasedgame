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

if __name__ == '__main__':
    print('wrong one, buddy')
