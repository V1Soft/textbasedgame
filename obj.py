class Player(object):
    def __init__(self, health, money, power):
        self.health = health
        self.money = money
        self.power = power

    def hit(self, amount):
        if amount > self.health:
            return ValueError
        self.health -= amount
        return self.health

    def spend(self, amount):
        if amount >  self.money:
            raise RuntimeError
        self.money -= amount
        return self.money
    
class Weapon(object):

    def __init__(self, power):
        self.power = power

if __name__ == '__main__':
    print('wrong one, buddy')
