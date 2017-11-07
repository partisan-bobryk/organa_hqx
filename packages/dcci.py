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
    ly, lx = img.shape

    imgPadded = np.zeros((ly+6, lx+6), dtype=np.uint8)
    imgPadded[3:-3,3:-3] = img

    imgOutPadded = np.zeros((ly*2+12, lx*2+12))

    for x in range(0, lx+3):
        for y in range(0, ly+3):  
            s = imgPadded[y:y+4, x:x+4]

            # Add Original Pixels
            imgOutPadded[2*y:2*y+7:2, 2*x:2*x+7:2] += s

            diagClass, d1, d2 = classifyOrth(s)
            diag = None
            if diagClass == DiagClassification.UP_RIGHT:
                diag = upRight(s)
            elif diagClass == DiagClassification.DOWN_RIGHT:
                diag = downRight(s)
            else:
                diag = diagSmooth(s, d1, d2)

            # Add diagonal pixels to both the output and replace the pixels in s
            imgOutPadded[2*y+1:2*y+1+5:2,2*x+1:2*x+1+5:2] += diag[1:6:2, 1:6:2]
            s2 = np.zeros((7,7), dtype=np.uint8)
            s2[::2,::2] = s
            s2[1:6:2, 1:6:2] = diag[1:6:2, 1:6:2]

            # Match classification and interpolate
            orth = None
            orthClass, d1, d2 = classifyOrth(s2)
            if orthClass == OrthClassification.HORIZONTAL:
                orth = horizontal(s2)
            elif orthClass == OrthClassification.VERTICAL:
                orth = vertical(s2)
            else:
                orth = orthSmooth(s2)

            # Replace orthogonal pixels
            imgOutPadded[2*y:2*y+7:2, 2*x+1:2*x+1+5:2] += orth[0:7:2, 1:6:2]
            imgOutPadded[2*y+1:2*y+1+5:2, 2*x:2*x+7:2] += orth[1:6:2, 0:7:2]

    return np.uint8(np.round(imgOutPadded[6:-6, 6:-6]/16))

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

# Input: 7x7 area
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

    w1 = 1.0 / (1.0 + d1**5.0)
    w2 = 1.0 / (1.0 + d2**5.0)
    weight1 = w1 / (w1 + w2)
    weight2 = w2 / (w1 + w2)

    downRightPixel = (-1 * s[0,0] + 9 * s[1, 1] + 9. * s[2, 2] - 1 * s[3, 3]) / 16.
    upRightPixel = (-1. * s[0, 3] + 9. * s[1, 2] + 9. * s[2, 1] - 1. * s[3, 0]) / 16.

    op = downRightPixel * weight1 + upRightPixel * weight2

    return op

# Input: 7x7 area
# Output: 7x7 interpolated area (Only orthogonals used)
def horizontal(s):
    return np.zeros((7,7)) + 255

# Input: 7x7 area
# Output: 7x7 interpolated area (Only orthogonals used)
def vertical(s):
    return np.zeros((7,7)) + 255

# Input: 7x7 area
# Output: 7x7 interpolated area (Only orthogonals used)
def orthSmooth(s):
    return np.zeros((7,7)) + 255
