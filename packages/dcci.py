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
            s[1:6:2, 1:6:2] = s[1:6:2, 1:6:2]

            orth = None
            orthClass = classifyOrth(s)
            if diagClass == OrthClassification.HORIZONTAL:
                orth = horizontal(s)
            elif diagClass == OrthClassification.VERTICAL:
                orth = vertical(s)
            else:
                orth = orthSmooth(s)

            # Replace orthogonal pixels
            imgOutPadded[2*y:2*y+7:2, 2*x+1:2*x+1+5:2] += orth[0:7:2, 1:6:2]
            imgOutPadded[2*y+1:2*y+1+5:2, 2*x:2*x+7:2] += orth[1:6:2, 0:7:2]

    return np.uint8(np.round(imgOutPadded[6:-6, 6:-6]/16))

def classifyDiag(s):
    return DiagClassification.UP_RIGHT

def classifyOrth(s):
    return OrthClassification.HORIZONTAL

def upRight(s):
    return np.zeros((7,7)) + 255

def downRight(s):
    return np.zeros((7,7)) + 255

def diagSmooth(s):
    return np.zeros((7,7)) + 255

def horizontal(s):
    return np.zeros((7,7)) + 255

def vertical(s):
    return np.zeros((7,7)) + 255

def orthSmooth(s):
    return np.zeros((7,7)) + 255
