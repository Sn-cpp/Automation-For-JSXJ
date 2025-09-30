from win32gui import GetForegroundWindow, SetForegroundWindow
import pyautogui as pyg
import keyboard as kb

from cores.game_interface import GameInteface
from cores.utils import Util
from procedures.daily_task import DailyTask

class Client:
    def __init__(self, hwnd: int, foot_fight: bool = False):
        self.hwnd = hwnd
        self.ui = GameInteface(hwnd, foot_fight)
        self.current_process = None
        
    def create_task_process(self, num: int):    
        self.current_process = DailyTask(self.ui, num)

    def execute(self):
        """
            Return:
                + True -> task completed
                + False -> task undone
        """
        if self.current_process.count <= 0:
            return True
        
        self.set_active()
        pyg.sleep(0.3)

        while GetForegroundWindow() != self.hwnd:
            if kb.is_pressed('space'):
                break
            pass

        while self.current_process.execute():
            if kb.is_pressed('space'):
                break
            pass

        return False

    def set_active(self):
        pyg.press('alt')
        SetForegroundWindow(self.hwnd)
        pyg.press('alt')