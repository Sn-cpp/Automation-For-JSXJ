import keyboard as kb
from time import sleep, time
from threading import Thread

from cores.client import Client
from cores.utils import Util


stop = False
running = True

def key_monitor():
    global stop, running
    esc_start = None

    while not stop:
        if kb.is_pressed('space'):
            running = not running
            print(f"Toggled running: {running}")
            sleep(0.3)
        if kb.is_pressed('esc'):
            if esc_start is None:
                esc_start = time()
            elif time() - esc_start >= 3.0:
                stop = True
                print("Exiting")
        else:
            esc_start = None
              
        sleep(0.05)


if __name__ == "__main__":
    sleep(2)                    
    clients = {  
        '1' : (Client(Util.getHWND(), False), 1),
     #   '2' : (Client(Util.getHWND(), False), 15),
     #   '3' : (Client(Util.getHWND(), False), 15),
     #   '4' : (Client(Util.getHWND(), True), 15) 
    }
   
    for client, task in clients.values():       
        client.create_task_process(task)
    
    monitor_thread = Thread(target=key_monitor)
    monitor_thread.start()

    while not stop:

        if running:
            done = True

            sleep(0.2) 
            for client, _ in clients.values():
                if not client.execute():  
                    done = False
                sleep(0.2)
            
            if done:
                stop = True


    






