from enum import Enum
import numpy as np

class DiagClassification(Enum):
    UP_RIGHT   = 1
    DOWN_RIGHT = 2
    SMOOTH     = 3

class OrthClassification(Enum):
    HORIZONTAL = 1
    VERTICAL   = 2
    SMOOTH     = 3

def Dccix2(img):
    img2 = np.swapaxes(img, 0, 1)

    lx, ly = img2.shape
    imgInterp = np.zeros((lx*2-1, ly*2-1))
    imgInterp[::2,::2] = img2

    imgInterp = interpDiag(imgInterp)
    imgInterp = interpOrth(imgInterp)
    return np.swapaxes(imgInterp, 0, 1)

# Input: The 2x image with black space padding each of the given pixels
# Output: The same image with the diagonal non-edge pixels interpolated
def interpDiag(img):
    lx, ly = img.shape
    imgPadded = np.zeros((lx+4,ly+4))# Pad by 1 given pixel (2 real pixels)
    imgPadded[2:-2,2:-2] = img

    # Center at the point to be interpolated, (x,y)
    for x in range(3, lx+1, 2):
        for y in range(3, ly+1, 2):  
            s4x4 = imgPadded[x-3:x+4:2,y-3:y+4:2]
            
            diagClass,d1, d2 = classifyDiag(s4x4)
            if diagClass == DiagClassification.UP_RIGHT:
                imgPadded[x,y] = upRight(s4x4)
            elif diagClass == DiagClassification.DOWN_RIGHT:
                imgPadded[x,y] = downRight(s4x4)
            else:
                imgPadded[x,y] = diagSmooth(s4x4, d1, d2)

    return imgPadded[2:-2,2:-2]

def interpOrth(img):
    lx, ly = img.shape
    imgPadded = np.zeros((lx+6,ly+6))
    imgPadded[3:-3,3:-3] = img
    
    # Center at the point to be interpolated, (x,y), as well as (x-1, y+1)
    for x in range(4, lx+3, 2):
        for y in range(3, ly+3, 2): 
            s7x7 = imgPadded[x-3:x+4,y-3:y+4]
            # Match classification and interpolate for x,y
            orthClass, d1, d2 = classifyOrth(s7x7)
            if orthClass == OrthClassification.HORIZONTAL:
                imgPadded[x,y] = horizontal(s7x7)
            elif orthClass == OrthClassification.VERTICAL:
                imgPadded[x,y] = vertical(s7x7)
            else:
                imgPadded[x,y] = orthSmooth(s7x7, d1, d2)

    for x in range(3, lx+3, 2):
        for y in range(4, ly+3, 2): 
            s7x7 = imgPadded[x-3:x+4,y-3:y+4]
            # Match classification and interpolate for x,y
            orthClass, d1, d2 = classifyOrth(s7x7)
            if orthClass == OrthClassification.HORIZONTAL:
                imgPadded[x,y] = horizontal(s7x7)
            elif orthClass == OrthClassification.VERTICAL:
                imgPadded[x,y] = vertical(s7x7)
            else:
                imgPadded[x,y] = orthSmooth(s7x7, d1, d2)

    return imgPadded[3:-3,3:-3]

# Input: 4x4 area
# Output: Classification
def classifyDiag(s):
    d1 = np.sum(np.abs(s[1:,:-1] - s[:-1,1:]))
    d2 = np.sum(np.abs(s[1:,1:] - s[:-1,:-1]))

    if (1+d1) > 1.15 * (1+d2):
        return DiagClassification.UP_RIGHT, d1, d2
    elif (1+d2) > 1.15 * (1+d1):
        return DiagClassification.DOWN_RIGHT, d1, d2
    else:
        return DiagClassification.SMOOTH, d1, d2

# Input: 7x7 padded "diamond" area
# Output: Classification
def classifyOrth(s2):
    d1 = np.sum(np.abs(s2[1:, -2:] - s2[-1:, -2:]))
    d2 = np.sum(np.abs(s2[-2:, 1:] - s2[-2:, -1:]))

    # Avoiding floating point error
    if (100 * (1 + d1) > 115 * (1 + d2)):
        return OrthClassification.HORIZONTAL, d1, d2
    elif (100 * (1 + d2) > 115 * (1 + d1)):
        return OrthClassification.VERTICAL, d1, d2
    else:
        return OrthClassification.SMOOTH, d1, d2



# Input: 4x4 area
# Output: 7x7 interpolated area (Only diagonals used)
def upRight(s):
    #(-1 * P(0, 0) + 9 * P(1, 1) + 9 * P(2, 2) - 1 * P(3, 3)) / 16
    op = (-1. * s[0,0] + 9. * s[1,1] + (-1.0)*s[3,3]) / 16.0
    return op

# Input: 4x4 area
# Output: 7x7 interpolated area (Only diagonals used)
def downRight(s):
    #Output pixel = (-1 * P(3, 0) + 9 * P(2, 1) + 9 * P(1, 2) - 1 * P(0, 3)) / 16
    op = ((-1.)*s[0,3] + 9. * s[2,1] + (-1.)*s[3,0] ) / 16.0
    return op

# Input: 4x4 area
# Output: 7x7 interpolated area (Only diagonals used)
def diagSmooth(s,d1,d2):
    w1 = 1.0 / (1.0 + d1**5)
    w2 = 1.0 / (1.0 + d2**5.0)
    weight1 = w1 / (w1 + w2)
    weight2 = w2 / (w1 + w2)

    downRightPixel = (-1 * s[0,0] + 9 * s[1, 1] + 9. * s[2, 2] - 1 * s[3, 3]) / 16.
    upRightPixel = (-1. * s[0, 3] + 9. * s[1, 2] + 9. * s[2, 1] - 1. * s[3, 0]) / 16.

    op = downRightPixel * weight1 + upRightPixel * weight2

    return op

# Input: 7x7 padded "diamond" area
# Output: 7x7 interpolated area (Only orthogonals used)
def horizontal(s):
    x, y = 3,3
    return (-1 * s[x, y-3] + 9 * s[x, y-1] + 9 * s[x, y+1] - 1 * s[x, y + 3]) / 16

# Input: 7x7 padded "diamond" area
# Output: 7x7 interpolated area (Only orthogonals used)
def vertical(s):
    x, y = 3, 3
    return (-1 * s[x-3, y] + 9 * s[x - 1, y] + 9 * s[x + 1, y] - 1 * s[x + 3, y]) / 16

# Input: 7x7 padded "diamond" area
# Output: 7x7 interpolated area (Only orthogonals used)
def orthSmooth(s, d1, d2):
    x,y = 3, 3
    w1 = 1.0 / (1.0 + d1 ** 5.0)
    w2 = 1.0 / (1.0 + d2 ** 5.0)
    weight1 = w1 / (w1 + w2)
    weight2 = w2 / (w1 + w2)

    horizontalPixel = (-1 * s[x-3, y] + 9 * s[x-1, y] + 9. * s[x+1, y] - 1 * s[x+3, y]) / 16.
    veritcalPixel = (-1. * s[x, y-3] + 9. * s[x, y-1] + 9. * s[x, y+1] - 1. * s[x, y+3]) / 16.

    op = horizontalPixel * weight1 + veritcalPixel * weight2

    return op
