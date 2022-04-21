from logging import exception
import numpy as np
import win32gui, win32ui, win32con


class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None    
    bmp_debug = ""

    def __init__(self, window_name):

        # find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception(f'Window not found: {window_name}')

        # define your monitor width and height
        self.w = 1920
        self.h = 1080

        # define debug file name
        self.bmp_debug = "debug.bmp"


    def get_screenshot(self):
        '''
        Capture a screenshot, turn it into a format opencv can read and return it
        '''

        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (0,0), win32con.SRCCOPY)
        
        # save the screenshot
        #dataBitMap.SaveBitmapFile(cDC, self.bmpfilenamename)
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]

        img = np.ascontiguousarray(img)

        return img