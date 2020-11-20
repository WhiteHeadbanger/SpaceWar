import random
import ship1, ship2
import os, time
from error_handling import OutOfEnergy, OutOfLimitsScan, OutOfFuel, MovementRangeExceeded, NoModuleActive
import utility

"""
Ticks are used to execute sentinel instructions, such as Black Holes's/Suns's gravity
"""
TICKS = 0
LAST_TICK = 0

class Space:
    """
    Space is a class declaration for the board itself.

    """

    # Variable de clase, en stack se agregan todas las acciones de las naves
    stack = [] 

    # Inicialización de la clase
    def __init__(self):
        # space_color determina el color del tablero
        self.__space_color__ = "⬜"
        # space determina como se va a ordenar el tablero. Llama al metodo initialize() cuando se instancia la clase.
        self.__space__ = self.initialize()

    def initialize(self):
        space = [[self.__space_color__ for sector in range(16)] for sector in range(16)]
        return space

    # El metodo spawn_objects recibe por argumento una lista de instancias (args es una lista) y luego las ubica en el tablero. 
    # Cambia el color del tablero (space_color) al color del objeto.
    def spawn_objects(self, *args):
        for arg in args:
            posx, posy = arg.__Pos__
            for x in range(len(self.__space__)):
                for y in range(len(self.__space__[x])):
                    if posx == x and posy == y:
                        self.__space__[y][x] = arg.__color__

    # Printea el tablero
    def create_space(self):
        for x in range(len(self.__space__)):
            for y in range(len(self.__space__[x])):
                print(self.__space__[x][y], end="")
            print()
        print("\n")

    # check_stack recibe por argumento una lista de instancias que sean objetos estaticos (como agujeros negros).
    # luego llama al metodo order_stack que recibe por argumento el stack de acciones y las ordena 
    def check_stack(self, *args):
        #stack_ordered es una lista de tuplas, ej: [("move", (1, 2), self), ("move", (4, 3), self)]
        stack_ordered = self.order_stack(Space.stack)
        self.update(stack_ordered, args) 

    def order_stack(self, stack):
        stack_aux = utility.utility(stack)
        return stack_aux

    # Metodo de clase. Los metodos de clase solo pueden acceder a variables de clase. Las variables de clase se denotan con "cls" (en contraposición con "self", que es una variable de instancia)
    # el metodo delete_stack limpia el stack de acciones una vez fueron ejecutadas.
    @classmethod
    def delete_stack(cls):
        cls.stack.clear()
    
    # metodo para actualizar el tablero con nuevas posiciones, nuevos colores, etc
    def update(self, instruction_stack: list, *args):
        # args = blackholes, suns, etc
        other_objects = []
        for arg in args:
            for a in arg:
                other_objects.append(a.__Pos__)

        if not instruction_stack:
            return
        for st in instruction_stack:
            if st[0] == "move":
                from_posx, from_posy = st[2].get_current_pos()
                to_posx, to_posy = st[1]
                for x in range(len(self.__space__)):
                    for y in range(len(self.__space__[x])):
                        if to_posx == x and to_posy == y:
                            self.__space__[y][x] = st[2].__color__
                            st[2].__Pos__ = (x, y) #store new ship positions
                            # Si la nueva posición de la nave es igual a la posición de un blackhole..
                            if st[2].__Pos__ in other_objects:
                                # La vida de la nave cambia a 0 y se destruye.
                                st[2].__hp__ = 0
                        if from_posx == x and from_posy == y:
                            self.__space__[y][x] = self.__space_color__
            elif st[0] == "attack":
                st[1].__hp__ -= st[2].__damage__

            # Print el nuevo tablero
            self.create_space()
            
        for i in range(len(instruction_stack)):
            print("Ship position {}: {} - Energy left: {} - HP left: {}".format(instruction_stack[i][2].__color__, instruction_stack[i][2].get_current_pos(), instruction_stack[i][2].__energy__, instruction_stack[i][2].__hp__))
        

# Clase base, todos los objetos heredan de Entity
class Entity:
    
    # Convertir a diccionario {}
    listOfEntities = []

    def __init__(self):
        self.__color__ = ""
        self.__Name__ = ""
        self.__Pos__ = self.spawn()
        self.__type__ = ""
        self.__hp__ = 0

        if self not in Entity.listOfEntities:
            Entity.listOfEntities.append(self)

    def get_name(self):
        return self.__Name__

    def get_current_pos(self):
        return self.__Pos__

    def get_type(self):
        return self.__type__

    def get_hp(self):
        return self.__hp__
    
    def get_target_pos(self, target):
        if isinstance(target, Entity):
            x, y = target.get_current_pos()
            return (x, y)

    def spawn(self):
        x = random.randint(0, 15)
        y = random.randint(0, 15)
        return (x, y)

    def get_color(self):
        return self.__color__


    
# Clase BlackHole. Hereda de Entity    
class BlackHole(Entity):

    prefixes = ['AZ', 'AX', 'JT', 'LT', 'X']
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


    def __init__(self):
        super().__init__()
        self.__Name__ = self.add_name()
        self.__type__ = "Black Hole"
        self.__hp__ = 1000000000000
        self.__color__ = '⚫'
        #self.gravity = self.create_gravity()

    def add_name(self):
        _name = []
        _name.append(random.choice(BlackHole.prefixes))
        _name.append(random.choice(BlackHole.numbers))
        return '-'.join(_name)

    """
    def create_gravity(self):
        posx, posy = self.pos
        gravity_top = (posx, posy - 1)
        gravity_right = (posx + 1, posy)
        gravity_bot = (posx, posy + 1)
        gravity_left = (posx - 1, posy)
        return {"gravity_top":gravity_top, "gravity_right":gravity_right, "gravity_bot":gravity_bot, "gravity_left":gravity_left}

    def activate_gravity(self):
        obj_pos = {}
        for obj in Entity.listOfEntities:
            if obj.type == "Ship":
                obj_pos.update({obj:obj.pos})
        for target, pos in obj_pos.items():
            if pos in self.gravity.values():
                target_pos_x, target_pos_y = pos
                grvt = list(self.gravity.keys())[list(self.gravity.values()).index(pos)]
                if grvt == "gravity_top":
                    target.pos = (target_pos_x, target_pos_y + 1)
                elif grvt == "gravity_right":
                    target.pos = (target_pos_x - 1, target_pos_y)
                elif grvt == "gravity_bot":
                    target.pos = (target_pos_x, target_pos_y - 1)
                elif grvt == "gravity_left":
                    target.pos = (target_pos_x + 1, target_pos_y)
    """

# Clase Ship. Hereda de Entity
class Ship(Entity):

    shipColor = ('🟪', '🟨', '🟧', '🟦', '🟩', '🟫')

    def __init__(self, powerplant, shield, fuel_tank, battery):
        super().__init__()
        self.__color__ = random.choice(Ship.shipColor)
        self.__energy__ = 50
        self.__type__ = "Ship"
        self.__fuel__ = 500
        self.__damage__ = 10
        self.__powerplant__ = powerplant
        self.__shield__ = shield
        self.__fuel_tank__ = fuel_tank
        self.__battery__ = battery
        self.__hp__ = 100


    def get_powerplant_integrity(self):
        return self.__powerplant__.get_hp()

    def get_shield_integrity(self):
        return self.__shield__.get_hp()

    def get_fuel_tank_integrity(self):
        return self.__fuel_tank__.get_hp()

    def get_battery_integrity(self):
        return self.__battery__.get_hp()
    
    def get_energy(self):
        return self.__energy__
        
    def get_fuel(self):
        return self.__fuel__

    def get_damage(self):
        return self.__damage__

    def add_name(self, name: str):
        self.__Name__ = name

    def move(self, to_pos: tuple):
        current_pos_x, current_pos_y = self.get_current_pos()
        target_pos_x, target_pos_y = to_pos
        if abs(target_pos_x - current_pos_x) > 1 or abs(target_pos_y - current_pos_y) > 1:
            raise MovementRangeExceeded()
        if self.__fuel__ < 1:
            raise OutOfFuel()
        Space.stack.append(("move", to_pos, self))
        self.__fuel__ -= 1

    def charge_energy(self):
        print("Charging energy resource. Stand-by for one turn")
        self.__energy__ += 1

    def scan_ships(self):
        """
        returns a list containing all the ships in space
        """
        if self.__energy__ < 1:
            raise OutOfEnergy()
        self.__energy__ -= 1
        ships = [x for x in Entity.listOfEntities if x.get_type() == "Ship"]
        return ships  # object list

    def scan_all(self):
        """
        returns a list containing all the objects in space
        """
        if self.__energy__ < 1:
            raise OutOfEnergy()
        self.__energy__ -= 1
        ships = [x for x in Entity.listOfEntities]
        return ships  # object list

    # Scan a specific ship
    def scan_target(self, target):
        """
        returns a dict containing all the modules a specific ship has
        """
        if self.__energy__ < 1:
            raise OutOfEnergy()
        self.__energy__ -= 1
        return {"powerplant":target.__powerplant__, "shield":target.__shield__, "fuel tank":target.__fuel_tank__, "battery":target.__battery__}
    

    def attack(self, target):
        if self.__energy__ < 2:
            raise OutOfEnergy()
        Space.stack.append(("attack", target, self))
        self.__energy__ -= 2

    def boost_shield(self, value: bool):
        self.__shield__.__boost__ = value
    
    
class Powerplant(Entity):

    def __init__(self):
        super().__init__()
        self.__type__ = "Powerplant"
        self.__hp__ = 100
        self.__active__ = True

    def deactivate(self):
        self.__active__ = False

    def activate(self):
        self.__active__ = True


class Shield(Entity):

    def __init__(self):
        super().__init__()
        self.__type__ = "Shield"
        self.__hp__ = 100
        self.__boost__ = False
        self.__active__ = True
        self.__shield_level__ = 0

    @property
    def boost(self):
        return self.__boost__

    @boost.setter
    def boost(self, value: bool):
        if not self.__active__:
            raise NoModuleActive()
        if self.__boost__:
            raise ValueError("Your shield is already boosted")
        self.__boost__ = value
        activate_boost(self)

    def activate_boost(self):
        self.__shield_level__ += 50


    def deactivate(self):
        self.__active__ = False

    def activate(self):
        self.__active__ = True

class Fueltank(Entity):

    def __init__(self):
        super().__init__()
        self.__type__ = "Fuel Tank"
        self.__hp__ = 100
        self.__active__ = True

    def deactivate(self):
        self.__active__ = False

    def activate(self):
        self.__active__ = True

class Battery(Entity):

    def __init__(self):
        super().__init__()
        self.__type__ = "Battery"
        self.__hp__ = 100
        self.__active__ = True

    def deactivate(self):
        self.__active__ = False

    def activate(self):
        self.__active__ = True


    

# Intancias y llamados a funciones de librerías importadas.
def game():
    # Se instancia el tablero
    board = Space()
    # Se instancian los modulos
    power_shipA = Powerplant()
    shield_shipA = Shield()
    fueltank_shipA = Fueltank()
    battery_shipA = Battery()
    power_shipB = Powerplant()
    shield_shipB = Shield()
    fueltank_shipB = Fueltank()
    battery_shipB = Battery() 
    # Se instancian las naves
    shipA = Ship(power_shipA, shield_shipA, fueltank_shipA, battery_shipA)
    shipB = Ship(power_shipB, shield_shipB, fueltank_shipB, battery_shipB)
    # Se instancian los agujeros negros del tablero
    blackHole = BlackHole()
    blackHole2 = BlackHole()
    # Se llama al metodo spawn_objects y como argumento se le pasan las instancias
    board.spawn_objects(shipA, shipB, blackHole, blackHole2)
    # Se llama al metodo create_space para printear el tablero con los objetos spawneados.
    board.create_space()
    # Loop del juego
    while True:
        # Si el HP de alguna de las dos naves cae a 0 o por debajo de 0, el juego termina
        ship1_hp = shipA.get_hp()
        ship2_hp = shipB.get_hp()
        if ship1_hp <= 0 or ship2_hp <= 0:
            break
        # Se llama a la función "main" de la librería "ship1", y se pasa como argumento la instancia de la primer nave "shipA"
        ship1.main(shipA)
        # Se llama a la función "main" de la librería "ship2", y se pasa como argumento la instancia de la primer nave "shipB"
        ship2.main(shipB)
        # Una vez que se ejecutaron los scripts de las dos naves, se checkea el stack y se actualiza el tablero
        board.check_stack(blackHole, blackHole2)
        # Una vez que se actualizó el tablero, se limpia el stack
        Space.delete_stack()
        #blackHole.activate_gravity()
        #blackHole2.activate_gravity()
        
    # Si la vida de alguno de los dos es 0 o menor, se printea el nombre del ganador y su color.
    if shipA.get_hp() <= 0:
        print("Winner ship: {} - Name: {}".format(shipB.get_color(), shipB.get_name()))
    elif shipB.get_hp() <= 0:
        print("Winner ship: {} - Name: {}".format(shipA.get_color(), shipA.get_name()))
        
# Esto es como poner game() al final del programa.
# Podes leer mas de esto aca: https://stackoverflow.com/a/419185/8915356
if __name__ == '__main__':
    game()



