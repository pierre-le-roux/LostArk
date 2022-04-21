import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import findClickPositions

# WindowCapture.list_window_names()
# exit() 

cwd = os.getcwd()

wincap = WindowCapture('LOST ARK (64-bit, DX11) v.2.2.1.1')

n_path = os.path.join(cwd, 'fishing.jpg')

loop_time = time()
while(True):

    screenshot = wincap.get_screenshot()

    # cv.imshow('Computer Vision', screenshot)
    findClickPositions(n_path, screenshot, debug_mode='rectangles')

    # measure fps
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')