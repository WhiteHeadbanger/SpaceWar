"""
ESTO VA A TIRAR ERROR CON LOS ULTIMOS CAMBIOS

"""

import time
import random
from error_handling import OutOfEnergy, OutOfFuel

def choose_movement(current_pos: tuple):
    posx, posy = current_pos
    directions = ["north", "east", "south", "west"]
    random_select = random.choice(directions)
    move = ()
    if random_select == "north":
        if posy > 0:
            posy -= 1
    elif random_select == "east":
        if posx < 16:
            posx += 1
    elif random_select == "south":
        if posy < 16:
            posy += 1
    elif random_select == "west":
        if posx > 0:
            posx -= 1
    return posx, posy


def main(ship):
    ship.add_name("Ship A")
    try:
        ship_scan = ship.scanner()
    except OutOfEnergy:
        ship.charge_energy()

    for scan in ship_scan:
        if scan.get_type() == "Ship" and scan.get_name() != ship.get_name():
            target_ship_pos_x, target_ship_pos_y = ship.get_target_pos(scan)
            target = scan

    current_pos_x, current_pos_y = ship.get_current_pos()

    difference_x = target_ship_pos_x - current_pos_x
    difference_y = target_ship_pos_y - current_pos_y

    if abs(difference_x) <= 2 and abs(difference_y) <= 2:
        print("Target is in attack proximity!")
        ship.attack(target)
    else:
        if difference_x < 0:
            try: 
                ship.move((current_pos_x - 1, current_pos_y))
            except OutOfFuel:
                pass
            time.sleep(1)
        elif difference_x > 0:
            try:
                ship.move((current_pos_x + 1, current_pos_y))
            except OutOfFuel:
                pass
            time.sleep(1)
        elif difference_x == 0 and difference_y < 0:
            try:
                ship.move((current_pos_x, current_pos_y - 1))
            except OutOfFuel:
                pass
            time.sleep(1)
        elif difference_x == 0 and difference_y > 0:
            try:
                ship.move((current_pos_x, current_pos_y + 1))
            except OutOfFuel:
                pass
            time.sleep(1)
            


    
