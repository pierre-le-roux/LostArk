import imghdr
import cv2 as cv
import numpy as np
from time import time
import win32gui, win32ui, win32con


def window_capture():
    '''
    Capture a screenshot, turn it into a format opencv can read and return it
    '''

    # size of my monitor
    w = 1920
    h = 1080
    bmpfilenamename = "debug.bmp"

    hwnd = win32gui.FindWindow(None, windowname)

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
    
    # save the screenshot
    #dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    img = img[...,:3]

    img = np.ascontiguousarray(img)

    return img


loop_time = time()
while(True):

    screenshot = window_capture()

    cv.imshow('Computer Vision', screenshot)

    # measure fps
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')


def list_window_names():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd))
    win32gui.EnumWindows(winEnumHandler, None)

# call it here:
# list_window_names()