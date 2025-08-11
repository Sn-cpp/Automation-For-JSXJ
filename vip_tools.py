import pyautogui as pyg
import keyboard as kb

def up_chestplate():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(229, 580)
    pyg.sleep(0.6)
    pyg.click(183, 710)
def up_chestplate_2():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(179, 520)

def up_weapon():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(238, 578)

def up_necklace():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(235, 550)
    pyg.sleep(0.4)
    pyg.moveTo(414, 471)
    pyg.drag(yOffset=230, duration=0.5)
    pyg.sleep(0.1)
    pyg.click(186, 816)
def up_necklace_2():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(154, 703)

def up_belt():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(235, 550)
    pyg.sleep(0.4)
    pyg.moveTo(414, 471)
    pyg.drag(yOffset=180, duration=0.5)
    pyg.sleep(0.1)
    pyg.click(183, 816)

def up_pendant():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(235, 550)
    pyg.sleep(0.4)
    pyg.moveTo(414, 471)
    pyg.drag(yOffset=100, duration=0.5)
    pyg.sleep(0.1)
    pyg.click(183, 801)

def up_glove():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(235, 550)
    pyg.sleep(0.4)
    pyg.click(183, 805)

def up_ring():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(235, 550)
    pyg.sleep(0.4)
    pyg.click(183, 775)
def up_ring_2():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(179, 548)


def up_boots():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(235, 550)
    pyg.sleep(0.4)
    pyg.click(183, 745)

def up_luck_pocket():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(229, 580)
    pyg.sleep(0.6)
    pyg.click(183, 740)
def up_luck_pocket_2():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(196, 582)

def up_helmet_2():
    pyg.press('4')
    pyg.sleep(0.4)
    pyg.click(154, 528)

def up_boots_2():
    pyg.press('4')
    pyg.sleep(0.3)
    pyg.click(148, 675)

def upgrade():
    print('reading 1st coord')
    pyg.sleep(3)
    pos1 = pyg.position()
    print('reading 2nd coord')
    pyg.sleep(3)
    pos2 = pyg.position()
    print('ready in 3s')
    pyg.sleep(3)

    while True:
        if kb.is_pressed('space'):
            break
        else:
            pyg.click(pos1.x, pos1.y)
            pyg.sleep(0.2)
            pyg.click(pos2.x, pos2.y)
            pyg.sleep(2)

def up_belt_2():
    pyg.press('4')
    pyg.sleep(0.3)
    pyg.click(156, 611)

pyg.sleep(5)

while not kb.is_pressed('space'):
    up_belt_2()