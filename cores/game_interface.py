from win32gui import GetWindowRect, SetForegroundWindow
import numpy as np

import pydirectinput as dv_input
from zbl import Capture

from time import time, sleep

import cv2

from assets.assets_loader import Assets
from cores.utils import Util

from cores.enum_header import SignalTypeEnum, HSVMaskEnum

from difflib import SequenceMatcher

class GameInteface:
    def __init__(self, client_hwnd: int, foot_fight: bool):
        self.hwnd = client_hwnd
        self.update_client_rect()

        self.screenshot = None

        self.timer = None
        self.foot_fight = foot_fight


        self.reach = False
        self.count = 0
        self.dist = float('inf')

    def set_target_coord(self, coord: tuple):
        self.target_coord = coord
        return True
        
    def capture_client(self):
        with Capture(window_handle=self.hwnd) as sct:
            self.screenshot = sct.grab()

    def crop_screenshot(self, y_0 = 0, y_1 = None, x_0 = 0, x_1 = None):
        return self.screenshot[y_0:y_1, x_0: x_1]

    def offset_v(self, y):
        return int(y * self.bottom / 741)

    def offset_h(self, x):
        return int(x * self.right / 982)

    def client_rect_change(self):
        new_rect = list(GetWindowRect(self.hwnd))
        Util.normalize_client_rect(new_rect)

        for new, cur in zip(new_rect, [self.left, self.top, self.right, self.bottom]):
            if new != cur:
                self.update_client_rect(rect=new_rect)
                return

    def update_client_rect(self, rect: list[int, int, int, int] = None):
        if rect is None:
            rect = list(GetWindowRect(self.hwnd))

        #Normalizing
        Util.normalize_client_rect(rect)

        #Client rect
        self.left = rect[0]
        self.top = rect[1]
        self.right = rect[2]
        self.bottom = rect[3]

        #Client dimension
        self.width = rect[2] - rect[0] + 1
        self.height = rect[3] - rect[1] + 1
        
        #Client center
        self.center_x = self.width // 2
        self.center_y = self.height // 2
    
    def get_center_x(self, global_offset=False):
        return self.center_x + self.left if global_offset else self.center_x
    
    def get_center_y(self, global_offset=False):
        return self.center_y + self.top if global_offset else self.center_y

    def goto_npc(self, npc_name: str):
        self.click_from_center()
        dv_input.press('tab')
        sleep(0.5)
        self.click_from_center(277, 345)
        dv_input.typewrite(npc_name)
        sleep(0.2)
        dv_input.press('enter')
        sleep(0.2)
     
        self.dist = float('inf')

        return True
    
    def resize_asset(self, asset: np.ndarray):
        return asset
        return Util.resize_asset(asset, (self.offset_v(asset.shape[1]), self.offset_h(asset.shape[0])))

    def is_reach_npc(self):
        self.capture_client()
        template = cv2.cvtColor(self.screenshot, cv2.COLOR_RGB2HSV)

        thresh_flag = cv2.bitwise_not(cv2.inRange(template, (92, 200, 136), (125, 255, 255)))
        thresh_marker = cv2.bitwise_not(cv2.inRange(template, (56, 86, 147), (74, 255, 255)))

        marker_res = cv2.matchTemplate(self.resize_asset(Assets.PlayerMarker), thresh_marker, cv2.TM_CCOEFF_NORMED)
        flag_res = cv2.matchTemplate(self.resize_asset(Assets.NpcFlag_R), thresh_flag, cv2.TM_CCOEFF_NORMED)
        if marker_res.max() > 0.7:
            if flag_res.max() <= 0.7:
                flag_res = cv2.matchTemplate(self.resize_asset(Assets.NpcFlag_L), thresh_flag, cv2.TM_CCOEFF_NORMED)
                if flag_res.max() < 0.7:
                    return False
            
            flag_pos = np.unravel_index(flag_res.argmax(), flag_res.shape)
            marker_pos = np.unravel_index(marker_res.argmax(), marker_res.shape)

            d = ((flag_pos[0] - marker_pos[0]) ** 2 + (flag_pos[1] - marker_pos[1]) ** 2) ** 0.5

            if d == self.dist:
                self.count += 1
                if self.count == 1:
                    self.count = 0
                    return True
            else:
                self.dist = d
        
        return False

    def click_center(self):
        sleep(0.2)
        dv_input.click(self.get_center_x(True), self.get_center_y(True))
        return True

    # def click(self, x, y):
    #     dv_input.moveTo(self.left + x, self.top + y)
    #     return True

    def click_from_center(self, dx: int = 0, dy: int = 0):
        dv_input.click(self.get_center_x(True) + self.offset_h(dx), self.get_center_y(True) + self.offset_v(dy))
        return True

    def move(self, dx: int = 0, dy: int = 0):
        dv_input.moveTo(self.get_center_x(True) + self.offset_h(dx), self.get_center_y(True) + self.offset_v(dy))
        return True

    def press(self, key: str):
        dv_input.press(key)
        return True

    def check_location(self, location: str):
        self.capture_client()
        text = Util.read_green_text(self.screenshot)
        if text != None and len(text):
            loc = text.casefold()
            words = location.casefold().split(' ')
            for word in words:
                if word in loc:
                    return True
        
        return False
    
        if coord == None:
            return flag
        
        coord_str = Util.read_green_text(self.screenshot[51:68, 805:860])

        if coord_str != None and len(coord_str):
            return SequenceMatcher(None, f'{coord[0]}/{coord[1]}', coord_str).ratio() > 0.89
        
        return False

    def is_reached(self):
        if self.count == 0:
            dv_input.press('tab')
            sleep(0.2)
            self.count = 1
        self.capture_client()

        template = cv2.cvtColor(self.screenshot, cv2.COLOR_RGB2HSV)
    
        thresh_flag = cv2.bitwise_not(cv2.inRange(template, (104, 118, 161), (116, 236, 255)))

        flag_res = cv2.matchTemplate(self.resize_asset(Assets.PositionFlag), thresh_flag, cv2.TM_CCOEFF_NORMED)

        if flag_res.max() > 0.7:
            self.count = 2
        else:
            if self.count >= 2:
                self.count += 1
                if self.count == 4:
                    self.count = 0
                    dv_input.press('tab')
                    sleep(0.5)
                    return True
        
        return False
        # if self.search_center:
        #     if 
        # else:

        # if pos[0] == self.search_center[0] and pos[1] == self.search_center[1]:
        #     self.count += 1
        #     if self.count == 3:
        #         self.count = 0
        #         self.old_pos = None
        #         dv_input.press('tab')
        #         return True
        # else:
        #     self.count = 0
        #     self.old_pos = pos
        #     sleep(1)

        return False

        if self.check_location(coord=self.target_coord):
            sleep(1)
            self.capture_client()
            if self.check_location(coord=self.target_coord):
                return True
        
        return False
        # text = Util.read_red_text(self.screenshot[self.height-170: self.height-130, 44:100])
        # if text is not None:
        #     if 'Đã' in text or 'đến' in text:
        #         return True
        # return False

    def detect_dialog(self, signal_type: SignalTypeEnum):
        
        self.capture_client()
        if signal_type == SignalTypeEnum.NPC_DIALOG:
            flag, x, y = Util.locate_img(self.resize_asset(Assets.DialogBoxSignal), 
                                         self.crop_screenshot(self.center_y-self.offset_v(246), self.center_y+self.offset_v(239), self.center_x-self.offset_h(445), self.center_x-self.offset_h(50))
                                        )
            sleep(0.4)
            return flag
        elif signal_type == SignalTypeEnum.REWARD:
            flag, x, y = Util.locate_img(Assets.FameReward, 
                                         self.crop_screenshot(self.center_y-self.offset_v(331), None, self.center_x-self.offset_h(240), self.center_x+self.offset_h(100))
                                        )
            sleep(0.4)
            return flag
        return False
    
    def detect_and_click(self, signal_type: SignalTypeEnum, dx: int = 0, dy: int = 0):
        self.capture_client()
        if signal_type == SignalTypeEnum.TASK_MARK:
            flag, x, y = Util.locate_img(Assets.TaskSignal,
                                         self.crop_screenshot(self.center_y-self.offset_v(246), self.center_y+self.offset_v(189), 0, self.center_x-self.offset_h(200))
                                         )
            if flag:
                dv_input.click(self.left + x, self.get_center_y(True) - self.offset_v(246) + y)
                return flag
            
        return False
    
    def goto_mob(self):
        self.capture_client()
        text = Util.read_mission_text(
            self.crop_screenshot(self.center_y+self.offset_v(160), self.center_y+self.offset_v(200), self.center_x-self.offset_h(205), self.center_x+self.offset_h(140))
        )
        
        if text != None:
            if 'Lang' in text:
                dv_input.press('f4')
                dv_input.press('tab')
                sleep(0.2)
                self.click_from_center(-340, 110)
                self.reach = False
                dv_input.press('tab')
                sleep(0.2)
            elif 'Du' in text:
                dv_input.press('f4')
                dv_input.press('tab')
                sleep(0.2)
                self.click_from_center(366, -147)
                self.reach = False
                dv_input.press('tab')
                sleep(0.2)
            elif 'Son' in text or 'Sơn' in text:
                dv_input.press('f4')
                dv_input.press('tab')
                sleep(0.2)
                self.click_from_center(134, -220)
                self.reach = False
                dv_input.press('tab')
                sleep(0.2)
            elif 'Thủ' in text:
                dv_input.press('f4')
                dv_input.press('tab')
                sleep(0.2)
                self.click_from_center(337, 60)
                self.reach = False
                dv_input.press('tab')
                sleep(0.2)
            else:
                return False
            return True

        return False

    def set_timer(self):
        self.timer = time()
        return True

    def elapse(self, amount):
        current = time()
        if current - self.timer >= amount:
            return True
        return False
    
    def is_task_complete(self):
        sleep(0.3)
        self.capture_client()
        text = Util.read_mission_text(
            self.crop_screenshot(self.center_y+self.offset_v(160), self.center_y+self.offset_v(200), self.center_x-self.offset_h(205), self.center_x+self.offset_h(140))
        )
        self.press('f4')

        self.click_center()



        if text != None and '24/' in text:
            return True
        

        mean_dot = Util.locate_mob_dot(
            self.crop_screenshot(self.offset_v(75), self.offset_v(175), self.offset_h(-130), self.offset_h(-30)),
            Assets.MobDot
        )

        if mean_dot != None:
            dv_input.click(self.left + self.width - self.offset_h(130) + mean_dot[0], self.top + self.offset_v(75) + mean_dot[1])
            sleep(1)
            
        dv_input.press('f')
 
        return False
    
    def get_on_horse(self):
        if self.foot_fight:
            dv_input.press('m')
        return True
    