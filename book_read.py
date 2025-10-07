import pyautogui as pyg
from time import time
import keyboard as kb

players = [
    (415, 25),
    (1395, 25),
    (560, 1125),
    (1500, 1125)
]

def learn(slot: int, player: int):
    pyg.click(players[player])
    pyg.sleep(0.1)
    pyg.press(str(slot))
    pyg.sleep(0.1)

def learn4p(indices: list):
    amount = 68
    last = time() - amount
    while True:
        if kb.is_pressed('space'):
            break
        
        now = time()

        if now - last >= amount:
            last = now
            for idx in indices:
                learn(5, idx)
            pyg.sleep(5)
            for idx in indices:                 
                learn(6, idx)

def HaiLangVuongMo_click():
    pos = []   
    print("started")
    for i in range(4):
        pyg.sleep(3)
        pos.append(pyg.position())
        print(f"recorded player {i+1}")

    print("click in 3s")   
    pyg.sleep(3)
    for i in range(4):
        pyg.click(pos[i].x, pos[i].y) 
    return
      
pyg.sleep(3)       
learn4p([0, 1, 2, 3])
#learn4p([0,1])                         