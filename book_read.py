import pydirectinput as dv_input
from time import sleep, time
import keyboard as kb

players = [
    (415, 25),
    (1395, 25),
    (560, 1125),
    (1500, 1125)
]

def learn(slot: int, player: int):
    dv_input.click(players[player])
    sleep(0.1)
    dv_input.press(str(slot))
    dv_input.press(str(slot))
    sleep(0.1)

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
            sleep(5)
            for idx in indices:                 
                learn(6, idx)

def HaiLangVuongMo_click():
    pos = []   
    print("started")
    for i in range(4):
        dv_input.sleep(3)
        pos.append(dv_input.position())
        print(f"recorded player {i+1}")

    print("click in 3s")   
    dv_input.sleep(3)
    for i in range(4):
        dv_input.click(pos[i].x, pos[i].y) 
    return
      
sleep(3)       
learn4p([0, 1, 2, 3])
#learn4p([0,1])                         