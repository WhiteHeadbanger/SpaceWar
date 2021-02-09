import time
import random
from error_handling import OutOfEnergy, OutOfFuel

"""
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
    ship.add_name("Ship B")
    
    try:
        ship.move((choose_movement(ship.get_current_pos())))
    except OutOfFuel:
        pass
    time.sleep(1)
    
    try:
       ship_scan = ship.scan_all()
    except OutOfEnergy:
        ship.charge_energy()
    time.sleep(1)

    current_pos_x, current_pos_y = ship.get_current_pos()
    
    for scan in ship_scan:
        if scan.get_type() == "Black Hole" and scan.get_name() != ship.get_name():
            target_ship_pos_x, target_ship_pos_y = ship.get_target_pos(scan)
            target = scan
    
    difference_x = target_ship_pos_x - current_pos_x
    difference_y = target_ship_pos_y - current_pos_y

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
"""

def main(ship):
    x = 18
    for i in range(1, 18):
        ship.move((x, 19))
        x -= 1
    for i in range(0, 19):
        ship.move((19, i))