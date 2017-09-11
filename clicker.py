import win32api
import win32con
import time
import pyscreenshot
import sys

__author__ = 'AdmiralGT'

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

class Building:

    def __init__(self, name, price, reward, x, y):
        self.name = name
        self.price = price
        self.reward = reward
        self.number = 0
        self.x = x
        self.y = y
        self.building = None

    def set_number(self, number):
        self.number = number

    def buy_object(self):
        time.sleep(0.1)
        click(self.x, self.y)
        self.price = self.price * 1.15
        self.number += 1
        return 1

    def get_rate(self):
        return self.reward / self.price

    def __str__(self):
        return 'Building: Name: %s, Price %d, Number %d' % (self.name, self.price, self.number)

class Upgrade:

    def __init__(self, price):
        self.price = price
        self.cursor = False
        self.reward = 0
        self.building = None
        if price < 1000 or (price is 10000) or (price is 50000):
            self.cursor = True
            self.building = 'cursor'
        elif (price is 1000) or (price is 5000):
            self.building = 'grandma'
        elif (price is 11000) or (price is 55000):
            self.building = 'farm'
        elif (price is 120000) or (price is 600000):
            self.building = 'mine'

        self.x = 1380
        self.y = 225

    def buy_object(self):
        time.sleep(0.1)
        click(self.x, self.y)
        if self.cursor:
            return 2
        else:
            return 1

    def __str__(self):
        return 'Upgrade: Price %d' % (self.price)


def get_best_upgrade(buildings, upgrades):
    best_rate = 0
    best_object = buildings['cursor']
    for key in buildings:
        building = buildings[key]
        rate = building.get_rate()
        if rate > best_rate:
            best_rate = rate
            best_object = building

    if upgrades[0] < best_object.price:
        best_object = Upgrade(upgrades[0])
        if (best_object.building is not None) and buildings[best_object.building].number < (upgrades[0] / 100):
            best_object = buildings[best_object.building]
        else:
            upgrades.pop(0)

    return best_object

def reset_game():
    click(550, 150)
    time.sleep(0.1)
    click(550, 460)
    time.sleep(0.1)
    click(820, 630)
    time.sleep(0.1)
    click(820, 630)
    time.sleep(0.1)
    click(1320, 250)
    time.sleep(2)

if __name__ == '__main__':
    buildings = {}
    buildings['cursor'] = Building('cursor', 15, 0.1, 1500, 320)
    buildings['grandma'] = Building('grandma', 100, 1, 1500, 380)
    buildings['farm'] = Building('farm', 1100, 8, 1500, 440)
    buildings['mine'] = Building('mine', 12000, 47, 1500, 500)
    buildings['factory'] = Building('factory', 130000, 260, 1500, 560)

    upgrades = [150, 800, 1000, 5000, 10000, 11000, 50000, 55000, 120000, 600000]

    #t_end = time.time() + 5
    #while time.time() < t_end:
    #    click(200, 500)
    #    time.sleep(0.005)
    #sys.exit(1)

    reset_game()

    click_rate = 1
    clicks = 0
    t_end = time.time() + 30#(60 * 10)
    object_to_buy = None
    no_cursor = True
    rate = 0
    loop_count = 0
    while time.time() < t_end:
        if loop_count > 200:
            loop_count = 0
            clicks += rate
            print("Rate = %d" % (rate))
        if object_to_buy is None:
            if no_cursor:
                object_to_buy = buildings['cursor']
            else:
                object_to_buy = get_best_upgrade(buildings, upgrades)
            print(object_to_buy)

        if no_cursor and clicks > 40:
            object_to_buy.buy_object()
            rate += object_to_buy.reward
            clicks -= (object_to_buy.price * 1.1)
            object_to_buy = None
            no_cursor = False
        elif not no_cursor and (object_to_buy.price < clicks):
            click_rate *= object_to_buy.buy_object()
            rate += object_to_buy.reward
            if object_to_buy.building is not None:
                building = buildings[object_to_buy.building]
                rate += building.reward * building.number
                buildings[object_to_buy.building].reward *= 2
            clicks -= (object_to_buy.price * 1.1)
            object_to_buy = None

        # Main cookie
        click(200, 500)
        # Sleeping actually allows the window to catch up
        time.sleep(0.005)
        clicks += click_rate
        loop_count += 1

    # Stats page
    click(600, 190)
    im = pyscreenshot.grab()
    im.save('grt.png')

