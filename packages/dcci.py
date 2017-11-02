from enum import Enum

class DiagClassification(Enum):
    UP_RIGHT   = 1
    DOWN_RIGHT = 2
    SMOOTH     = 3

class OrthClassification(Enum):
    HORIZONTAL = 1
    VERTICAL   = 2
    SMOOTH     = 3

def Dccix2(img):
    # Iterate over each sub-image, s:
    
    diagClass = classifyOrth()
    if diagClass == DiagClassification.UP_RIGHT:
        upRight()
    elif diagClass == DiagClassification.DOWN_RIGHT:
        downRight()
    else:
        diagSmooth()

    orthClass = classifyOrth()
    if diagClass == OrthClassification.HORIZONTAL:
        horizontal()
    elif diagClass == OrthClassification.VERTICAL:
        vertical()
    else:
        orthSmooth()

    return img

def classifyDiag():
    return DiagClassification.UP_RIGHT

def classifyOrth():
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