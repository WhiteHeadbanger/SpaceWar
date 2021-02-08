import random
import pygame as pg
import os, time
from error_handling import OutOfEnergy, OutOfLimitsScan, OutOfFuel, MovementRangeExceeded, NoModuleActive
import utility
import sw_classes
import color
import config



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
        return [[self.__space_color__ for sector in range(16)] for sector in range(16)]

    # El metodo spawn_objects recibe por argumento una lista de instancias (args es una lista) y luego las ubica en el tablero. 
    # Cambia el color del tablero (space_color) al color del objeto.
    def spawn_objects(self, *args):
        for arg in args:
            posx, posy = arg.__Pos__
            self.__space__[posy][posx] = arg.__color__

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

    def fill_board_color(self, x, y, *obj):
        if obj: 
            self.__space__[y][x] = obj[0].__color__ 
        else: 
            self.__space__[y][x] = self.__space_color__
    
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
                            self.fill_board_color(x, y, st[2])
                            st[2].__Pos__ = (x, y) #store new ship positions
                            # Si la nueva posición de la nave es igual a la posición de un blackhole..
                            if st[2].__Pos__ in other_objects:
                                # La vida de la nave cambia a 0 y se destruye.
                                st[2].__hp__ = 0
                        if from_posx == x and from_posy == y:
                            self.fill_board_color(x, y)
            elif st[0] == "attack":
                st[1].__hp__ -= st[2].__damage__

            # Print el nuevo tablero
            self.create_space()
            
        for i in range(len(instruction_stack)):
            print("Ship position {}: {} - Energy left: {} - HP left: {}".format(instruction_stack[i][2].__color__, instruction_stack[i][2].get_current_pos(), instruction_stack[i][2].__energy__, instruction_stack[i][2].__hp__))
        
"""
class Ship(Entity):

    shipColor = ('🟪', '🟨', '🟧', '🟦', '🟩', '🟫')

    def __init__(self):
        super().__init__()
        self.__color__ = random.choice(Ship.shipColor)
        
    def move(self, to_pos: tuple):
        current_pos_x, current_pos_y = self.get_current_pos()
        target_pos_x, target_pos_y = to_pos
        if abs(target_pos_x - current_pos_x) > 1 or abs(target_pos_y - current_pos_y) > 1:
            raise MovementRangeExceeded()
        if self.__fuel__ < 1:
            raise OutOfFuel()
        Space.stack.append(("move", to_pos, self))
        self.__fuel__ -= 1

    

    def scan_ships(self):
        #returns a list containing all the ships in space
        
        if self.__energy__ < 1:
            raise OutOfEnergy()
        self.__energy__ -= 1
        ships = [x for x in Entity.listOfEntities if x.get_type() == "Ship"]
        return ships  # object list

    
    

    def attack(self, target):
        if self.__energy__ < 2:
            raise OutOfEnergy()
        Space.stack.append(("attack", target, self))
        self.__energy__ -= 2

    
"""

def game():

    pg.init()
    screen = config.SCREEN
    space = sw_classes.Space()
    power_shipA = sw_classes.Powerplant()
    shield_shipA = sw_classes.Shield()
    fueltank_shipA = sw_classes.Fueltank()
    battery_shipA = sw_classes.Battery()
    power_shipB = sw_classes.Powerplant()
    shield_shipB = sw_classes.Shield()
    fueltank_shipB = sw_classes.Fueltank()
    battery_shipB = sw_classes.Battery()
    ship1 = sw_classes.Ship(color.RED, power_shipA, shield_shipA, fueltank_shipA, battery_shipA)
    ship2 = sw_classes.Ship(color.BLUE, power_shipB, shield_shipB, fueltank_shipB, battery_shipB)

    timer_id = pg.USEREVENT + 1
    pg.time.set_timer(timer_id, 1000)
    
    x1 = 1
    x2 = 18
    while True:
        
        if ship1.get_spawn_state() == False and ship2.get_spawn_state() == False:
            screen.fillColor(color.WHITE)
            space.exist(screen._screen)
            ship1.spawn(screen._screen, 0, 0)
            ship2.spawn(screen._screen, 19, 19)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == timer_id:
                screen.fillColor(color.WHITE)
                space.exist(screen._screen)
                
                ship1.move((x1, 0))
                ship2.move((x2, 19))
                x1 += 1
                x2 -= 1
                
        pg.display.update()
        
    """
    # Se instancia el tablero
    board = Space()
    # Se instancian los modulos
    
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
    """

if __name__ == '__main__':
    game()



