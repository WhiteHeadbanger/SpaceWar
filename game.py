import random
import pygame as pg
import os, time
from error_handling import OutOfEnergy, OutOfLimitsScan, OutOfFuel, MovementRangeExceeded, NoModuleActive
import sw_classes
import color
import config
import shipA, shipB
        

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
        


if __name__ == '__main__':
    game()



