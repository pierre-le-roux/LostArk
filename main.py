from operator import ne
import cv2 as cv
from cv2 import threshold
from cv2 import MARKER_CROSS
import numpy as np
import os

cwd = os.getcwd()

h_path = os.path.join(cwd, 'LostArk', 'lostark.jpg')
n_path = os.path.join(cwd, 'LostArk', 'fishing.jpg')

def findClickPositions(needle_img_path, haystack_img_path, method=cv.TM_CCOEFF_NORMED, threshold=0.05, debug_mode=None):
    
    haystack_img = cv.imread(haystack_img_path, cv.IMREAD_UNCHANGED)
    needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
        
    # get dimensions of the needle image
    needle_h = needle_img.shape[0]
    needle_w = needle_img.shape[1]

    result = cv.matchTemplate(haystack_img, needle_img, method)

    # inverted the threshold and where comparison to work with TM_SQDIFF_NORMED
    # threshold is normal when used with TM_CCOEFF_NORMED
    if method == cv.TM_SQDIFF_NORMED:
        locations = np.where(result <= threshold)
    elif method == cv.TM_CCOEFF_NORMED:
        locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    # first we need to create the list of [x, y, w, h] rectangles
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        rectangles.append(rect)
        rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles, 1, 1)

    points = []
    if len(rectangles):
        print('Catch Fish')

        line_colour = (0, 255, 0)
        line_type = cv.LINE_4
        marker_colour = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (x, y, w, h) in rectangles:

            # determine the center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)

            # save the points
            points.append((center_x, center_y))

            if debug_mode == 'rectangles':
                # determine the box positions
                top_left = (x, y)
                bottom_right = (x + w, y + h)

                # draw the box
                cv.rectangle(haystack_img, top_left, bottom_right,
                color=line_colour, lineType=line_type)
            elif debug_mode == 'points':
                cv.drawMarker(haystack_img, (center_x, center_y), marker_colour, marker_type)

        if debug_mode:
            cv.imshow('Matches', haystack_img)
            cv.waitKey()
            #cv.imwrite('result.jpg', haystack_img)
    
    return points

points = findClickPositions(n_path, h_path, method=cv.TM_CCOEFF_NORMED, threshold=0.95, debug_mode='points')
print(points)