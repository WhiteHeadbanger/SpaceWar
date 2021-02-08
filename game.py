import random
import pygame as pg
import os, time
from error_handling import OutOfEnergy, OutOfLimitsScan, OutOfFuel, MovementRangeExceeded, NoModuleActive
import sw_classes
import color
import config
import shipA, shipB
        
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
    shipA.main(ship1)
    shipB.main(ship2)

    timer_id = pg.USEREVENT + 1
    pg.time.set_timer(timer_id, 1000)
    
    x1 = 1
    x2 = 18

    def execute_action(screen, ship):
        error = "Hubo un error"
        if not ship.stack:
            pass
        try:
            if ship.stack[0][0] == "move":
                ship.spawn(screen, ship.stack[0][1], ship.stack[0][2])
                ship.stack.pop(0)
        except IndexError:
            print(error)

    while True:
        
        if not ship1.get_spawn_state() and not ship2.get_spawn_state():
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
                execute_action(screen._screen, ship1)
                execute_action(screen._screen, ship2)
                
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



