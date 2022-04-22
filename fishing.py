import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture import WindowCapture
from vision import findClickPositions
from pynput.keyboard import Key, Controller

# WindowCapture.list_window_names()
# exit() 

cwd = os.getcwd()

wincap = WindowCapture('LOST ARK (64-bit, DX11) v.2.2.1.2')

n_path = os.path.join(cwd, 'fishing.jpg')

# loop_time = time()
keyboard = Controller()
print('wait 5 sec')
sleep(5)
# keyboard.press('s')
# keyboard.release('s')
while(True):
    sleep(5)
    keyboard.press('e')
    keyboard.release('e')

    while(True):

        screenshot = wincap.get_screenshot()

        # cv.imshow('Computer Vision', screenshot)
        result = findClickPositions(n_path, screenshot)

        if result:
            keyboard.press('e')
            keyboard.release('e')
            print('fish caught')
            break

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        # if cv.waitKey(1) == ord('q'):
        #     cv.destroyAllWindows()
        #     exit()

    print('sleep 7 sec')
    sleep(7)