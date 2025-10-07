from win32gui import GetForegroundWindow, GetWindowText
import keyboard as kb
import numpy as np
import cv2
from pytesseract import image_to_string
from time import sleep

from assets.assets_loader import Assets
from cores.enum_header import HSVMaskEnum

class Util:
    HSVMask = {
        HSVMaskEnum.NORMAL_GREEN_TEXT : ((0, 232, 107), (75, 255, 255)),
        HSVMaskEnum.COORDINATE_TEXT : ((0, 75, 75), (75, 255, 255)),
        HSVMaskEnum.MOB_DOT : ((132, 0, 0), (180, 255, 255))
    }
    def getHWND():
        client = None
        print("Listening for client")
        while True:
            if kb.is_pressed('enter'):
                client = GetForegroundWindow()
                print("HWND: ", client)
                print("Title: ", GetWindowText(client))
                break
            pass
        print("Selected client: ", GetWindowText(client))
        sleep(0.5)
        return client

    def process_green_text(roi: np.ndarray, text_type: HSVMaskEnum = HSVMaskEnum.NORMAL_GREEN_TEXT):
        # upscale_roi = cv2.resize(cv2.cvtColor(roi, cv2.COLOR_RGB2HSV), (int(roi.shape[1] * 8), int(roi.shape[0] * 8)), interpolation=cv2.INTER_CUBIC)
        upscale_roi = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
        return cv2.bitwise_not(cv2.inRange(upscale_roi, *Util.HSVMask[text_type]))

    def read_green_text(roi: np.ndarray):
        try:
            text = str(image_to_string(Util.process_green_text(roi, HSVMaskEnum.NORMAL_GREEN_TEXT), lang='vie'))
            return text if len(text) else None
        except:
            return None
    
    def read_coordinate(roi: np.ndarray):
        # coord_roi = Util.process_green_text(roi, GreenTextTypeEnum.COORDINATE)
        roi_x = roi[:, :155]
        roi_y = roi[:, 200:]
        return roi_x, roi_y

    def read_red_text(roi: np.ndarray):
        resize = cv2.resize(cv2.cvtColor(roi, cv2.COLOR_RGB2HSV), (int(roi.shape[1] * 8), int(roi.shape[0] * 8)), interpolation=cv2.INTER_CUBIC)
        roi_threshold = cv2.inRange(resize, (0, 140, 108), (180, 255, 255))

        try:
            text = str(image_to_string(roi_threshold, lang='vie'))
            return text if len(text) else None
        except:
            return None

    def read_mission_text(roi: np.ndarray):
        upscale = cv2.resize(cv2.cvtColor(roi, cv2.COLOR_RGB2HSV), (int(roi.shape[1] * 8), int(roi.shape[0] * 8)), interpolation=cv2.INTER_CUBIC)
        threshold = cv2.inRange(upscale, (0, 170, 95), (180, 255, 255))
        
        try:
            text = str(image_to_string(threshold, lang='vie'))
            return text if len(text) else None
        except:
            return None

    def normalize_client_rect(rect: list[int, int, int, int]):
        rect[0] += 9
        rect[1] += 39
        rect[2] -= 9
        rect[3] -= 9

    def locate_img(img: np.ndarray, template: np.ndarray):
        res = cv2.matchTemplate(img, cv2.cvtColor(template, cv2.COLOR_RGB2GRAY), cv2.TM_CCOEFF_NORMED)


        THRESHOLD = 0.75
        loc = np.where(res >= THRESHOLD)


        for y, x in zip(loc[0], loc[1]):
            return True, x, y
        
        return False, None, None
    
    def locate_mob_dot(img: np.ndarray, mob_dot: np.ndarray):
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        frame_threshold = cv2.inRange(hsv,*Util.HSVMask[HSVMaskEnum.MOB_DOT])

        res = cv2.matchTemplate(mob_dot, frame_threshold, cv2.TM_CCOEFF_NORMED)
        
        loc = np.where(res >= 0.6)

        if len(loc[0]) == 0 or len(loc[1]) == 0:
            return None
        
        return int(np.mean(loc[1])), int(np.mean(loc[0]))
    
    def resize_asset(asset: np.ndarray, shape):
        return cv2.resize(asset, shape, interpolation=cv2.INTER_LINEAR)

