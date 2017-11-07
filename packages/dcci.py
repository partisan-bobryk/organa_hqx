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

            diagClass = classifyOrth(s)
            diag = None
            if diagClass == DiagClassification.UP_RIGHT:
                diag = upRight(s)
            elif diagClass == DiagClassification.DOWN_RIGHT:
                diag = downRight(s)
            else:
                diag = diagSmooth(s)

            # Add diagonal pixels to both the output and replace the pixels in s
            imgOutPadded[2*y+1:2*y+1+5:2,2*x+1:2*x+1+5:2] += diag[1:6:2, 1:6:2]
            s2 = np.zeros((7,7), dtype=np.uint8)
            s2[::2,::2] = s
            s2[1:6:2, 1:6:2] = diag[1:6:2, 1:6:2]

            # Match classification and interpolate
            orth = None
            orthClass = classifyOrth(s2)
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
        return DiagClassification.UP_RIGHT
    elif (1+d2) > 1.15 * (1+d1):
        return DiagClassification.DOWN_RIGHT
    else:
        return DiagClassification.SMOOTH

# Input: 7x7 area
# Output: Classification
def classifyOrth(s2):
    d1 = np.sum(np.abs(s2[1:, -2:] - s2[-1:, -2:]))
    d2 = np.sum(np.abs(s2[-2:, 1:] - s2[-2:, -1:]))

    # Avoiding floating point error
    if (100 * (1 + d1) > 115 * (1 + d2)):
        return OrthClassification.HORIZONTAL
    elif (100 * (1 + d2) > 115 * (1 + d1)):
        return OrthClassification.VERTICAL
    else:
        return OrthClassification.SMOOTH



# Input: 4x4 area
# Output: 7x7 interpolated area (Only diagonals used)
def upRight(s):
    return np.zeros((7,7)) + 255

# Input: 4x4 area
# Output: 7x7 interpolated area (Only diagonals used)
def downRight(s):
    return np.zeros((7,7)) + 255

# Input: 4x4 area
# Output: 7x7 interpolated area (Only diagonals used)
def diagSmooth(s):
    return np.zeros((7,7)) + 255

# Input: 7x7 area
# Output: 7x7 interpolated area (Only orthogonals used)
def horizontal(s):
    # (-1 * P(X, Y - 3) + 9 * P(X, Y - 1) + 9 * P(X, Y + 1) - 1 * P(X, Y + 3)) / 16
    return (-1 * s[0, -3] + 9 * s[0, -1] + 9 * s[0, 1] - 1 * s[0, 3]) / 16

# Input: 7x7 area
# Output: 7x7 interpolated area (Only orthogonals used)
def vertical(s):
    return np.zeros((7,7)) + 255

# Input: 7x7 area
# Output: 7x7 interpolated area (Only orthogonals used)
def orthSmooth(s):
    return np.zeros((7,7)) + 255
