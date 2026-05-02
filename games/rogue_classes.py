class Entity:
    def __init__(self, name, x, y, char, hp, damage):
        self.name = name
        self.x, self.y = x, y
        self.char = char
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.level = 1
    
class Item:
    def __init__(self, name, x, y, char, power):
        self.name = name
        self.x, self.y = x, y
        self.char = char
        self.power = power