import pygame as pg
import color
import config
import random
from error_handling import *

class Space(pg.sprite.Sprite):

    SpaceMap = []

    def __init__(self):
        super().__init__()
        self.xslot = 20
        self.yslot = 20
        self.slot = pg.Surface((self.xslot, self.yslot))
        self.color = color.BLACK

    def exist(self, screen):
        blockSize = 20
        Id = 0 
        for x in range(config.WINDOW_WIDTH // blockSize):
            for y in range(config.WINDOW_HEIGHT // blockSize):
                rect = self.slot.get_rect(topleft = (x * blockSize, y * blockSize))
                pg.draw.rect(screen, self.color, rect, 1)
                Space.SpaceMap.append((Id, x, y, x * blockSize, y * blockSize))
                Id += 1

class Entity:
    
    listOfEntities = []

    def __init__(self):
        self.name = ""
        self.pos = 0
        self.type = ""
        self.hp = 0

        
        if self not in Entity.listOfEntities:
            Entity.listOfEntities.append(self)
        

    def get_name(self):
        return self.name

    def get_current_pos(self):
        return self.pos

    def get_type(self):
        return self.type

    def get_hp(self):
        return self.hp
    
    """
    def get_target_pos(self, target):
        
        if isinstance(target, Entity):
            x, y = target.get_current_pos()
            return (x, y)

    
    def spawn(self):
        x = random.randint(0, 15)
        y = random.randint(0, 15)
        return (x, y)
    """

class Ship(pg.sprite.Sprite, Entity):

    Queue = []

    def __init__(self, color, powerplant, shield, fuel_tank, battery):
        super().__init__()
        self.blocksize = 16
        self.xpos = 0
        self.ypos = 0
        self.color = color
        self.energy = 50
        self.type = "Ship"
        self.fuel = 500
        self.damage = 10
        self.powerplant = powerplant
        self.shield = shield
        self.fuel_tank = fuel_tank
        self.battery = battery
        self.hp = 100
        self.spawned = False
        self.stack = []

    def get_spawn_state(self):
        return self.spawned

    def get_powerplant_integrity(self):
        return self.powerplant.get_hp()

    def get_shield_integrity(self):
        return self.shield.get_hp()

    def get_fuel_tank_integrity(self):
        return self.fuel_tank.get_hp()

    def get_battery_integrity(self):
        return self.battery.get_hp()
    
    def get_energy(self):
        return self.energy
        
    def get_fuel(self):
        return self.fuel

    def get_damage(self):
        return self.damage

    def get_current_pos(self):
        return (self.xpos, self.ypos)

    def add_name(self, name: str):
        self.name = name
        
    def spawn(self, screen, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        for item in Space.SpaceMap:
            if item[1] == xpos and item[2] == ypos:
                xpos, ypos = item[3], item[4]
        rect = pg.Rect(xpos+2, ypos+2, self.blocksize, self.blocksize)
        pg.draw.rect(screen, self.color, rect)
        if not self.spawned:
            self.spawned = True

    def move(self, target_pos: tuple):
        current_xpos, current_ypos = self.get_current_pos()
        target_xpos, target_ypos = target_pos
        #if abs(target_xpos - current_xpos) > 1 or abs(target_ypos - current_ypos) > 1:
            #raise MovementRangeExceeded()
        #if self.fuel < 1:
            #raise OutOfFuel()
        self.stack.append(("move", target_xpos, target_ypos, self))
        #self.spawn(config.SCREEN._screen, target_xpos, target_ypos)

    def charge_energy(self):
        print("Charging energy resource. Stand-by for one turn")
        self.energy += 1

    def scan_all(self):
        #returns a list containing all the objects in space

        if self.energy < 1:
            raise OutOfEnergy()
        self.energy -= 1
        ships = [x for x in Entity.listOfEntities]
        return ships

    def scan_module(self, target):
        #returns a dict containing all the modules a specific ship has

        if self.energy < 1:
            raise OutOfEnergy()
        self.energy -= 1
        return {"powerplant":target.powerplant, "shield":target.shield, "fuel tank":target.fuel_tank, "battery":target.battery}
    
    def scan_ships(self):
        #returns a list containing all the ships in space
        
        if self.energy < 1:
            raise OutOfEnergy()
        self.energy -= 1
        ships = [x for x in Entity.listOfEntities if x.get_type() == "Ship"]
        return ships
    
    def boost_shield(self, value: bool):
        self.shield.boost = value
    
    def attack(self, target):
        if self.energy < 2:
            raise OutOfEnergy()
        Space.stack.append(("attack", target, self))
        self.energy -= 2



class Powerplant(Entity):

    def __init__(self):
        super().__init__()
        self.type = "Powerplant"
        self.hp = 100
        self.active = True

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True


class Shield(Entity):

    def __init__(self):
        super().__init__()
        self.type = "Shield"
        self.hp = 100
        self.boost = False
        self.active = True
        self.shield_level = 100

    """
    @property
    def boost(self):
        return self.boost

    @boost.setter
    def boost(self, value: bool):
        if not self.active:
            raise NoModuleActive()
        if self.boost:
            raise ValueError("Your shield is already boosted")
        self.boost = value
        activate_boost(self)
    """

    def activate_boost(self):
        self.shield_level += 50

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

class Fueltank(Entity):

    def __init__(self):
        super().__init__()
        self.type = "Fuel Tank"
        self.hp = 100
        self.active = True

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

class Battery(Entity):

    def __init__(self):
        super().__init__()
        self.type = "Battery"
        self.hp = 100
        self.active = True

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

class BlackHole(Entity):

    prefixes = ['AZ', 'AX', 'JT', 'LT', 'X']
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


    def __init__(self):
        super().__init__()
        self.name = self.add_name()
        self.type = "Black Hole"
        self.hp = 1000000000000
        #self.gravity = self.create_gravity()

    def add_name(self):
        name = []
        name.append(random.choice(BlackHole.prefixes))
        name.append(random.choice(BlackHole.numbers))
        return '-'.join(name)

    """
    def create_gravity(self):
        posx, posy = self.pos
        gravity_top = (posx, posy - 1)
        gravity_right = (posx + 1, posy)
        gravity_bot = (posx, posy + 1)
        gravity_left = (posx - 1, posy)
        return {"gravity_top":gravity_top, "gravity_right":gravity_right, "gravity_bot":gravity_bot, "gravity_left":gravity_left}
    """
