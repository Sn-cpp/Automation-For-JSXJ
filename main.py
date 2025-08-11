import keyboard as kb
import pyautogui as pyg

from cores.client import Client
from cores.utils import Util

if __name__ == "__main__":
    pyg.sleep(2)                   
    clients = {
        '1' : (Client(Util.getHWND(), False), 10),
       # '2' : (Client(Util.getHWND(), False), 10),
        #'3' : (Client(Util.getHWND(), False), 10),
        #'4' : (Client(Util.getHWND(), False), 10)
    }

    for client, task in clients.values():
        client.create_task_process(task)


    while True:
        if kb.is_pressed('space'):
            break
        
        for client, _ in clients.values():
            client.execute()
            pyg.sleep(0.2)

        pass





