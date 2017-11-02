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

    img_padded = np.zeros((ly+6, lx+6), dtype=np.uint8)
    img_padded[3:-3,3:-3] = img
    print(img_padded[-10:, -10:])


    img2 = np.zeros((ly*2+12, lx*2+12))

    for x in range(0, lx+3):
        for y in range(0, ly+3):  
            s = img_padded[y:y+4, x:x+4]
            print(s)

            diagClass = classifyOrth(s)
            if diagClass == DiagClassification.UP_RIGHT:
                upRight()
            elif diagClass == DiagClassification.DOWN_RIGHT:
                downRight()
            else:
                diagSmooth()

            orthClass = classifyOrth(s)
            if diagClass == OrthClassification.HORIZONTAL:
                horizontal()
            elif diagClass == OrthClassification.VERTICAL:
                vertical()
            else:
                orthSmooth()

    return img

def classifyDiag(s):
    return DiagClassification.UP_RIGHT

def classifyOrth(s):
    return OrthClassification.HORIZONTAL

def upRight():
    return

def downRight():
    return

def diagSmooth():
    return

def horizontal():
    return

def vertical():
    return

def orthSmooth():
    return