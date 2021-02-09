import time
import random
from error_handling import OutOfEnergy, OutOfFuel



def main(ship):
    ship.add_name("Ship A")
    try:
        ship_scan = ship.scan_ships()
    except OutOfEnergy:
        ship.charge_energy()

    for scan in ship_scan:
        if scan.get_name() != "Ship A":
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
        elif difference_x > 0:
            try:
                ship.move((current_pos_x + 1, current_pos_y))
            except OutOfFuel:
                pass
        elif difference_x == 0 and difference_y < 0:
            try:
                ship.move((current_pos_x, current_pos_y - 1))
            except OutOfFuel:
                pass
        elif difference_x == 0 and difference_y > 0:
            try:
                ship.move((current_pos_x, current_pos_y + 1))
            except OutOfFuel:
                pass

"""
def main(ship):
    for i in range(0, 18):
        ship.move((i, 0))
"""

    
