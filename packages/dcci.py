from enum import Enum
import numpy as np
import cv2

class DiagClassification(Enum):
    UP_RIGHT   = 1
    DOWN_RIGHT = 2
    SMOOTH     = 3

class OrthClassification(Enum):
    HORIZONTAL = 1
    VERTICAL   = 2
    SMOOTH     = 3

def Dccix2(img, T=115, k=5):
    img2 = np.float64(np.swapaxes(img, 0, 1))

    lx, ly = img2.shape
    imgInterp = np.zeros((lx*2-1, ly*2-1))
    imgInterp[::2,::2] = img2

    imgInterp = interpDiag(img, imgInterp, T, k)
    imgInterp = interpOrth(imgInterp, T, k)

    imgInterp[imgInterp < 0] = 0
    imgInterp[imgInterp > 255] = 255
    imgInterp = np.uint8(np.round(imgInterp))
    
    return np.swapaxes(imgInterp, 0, 1)

# Input: The 2x image with black space padding each of the given pixels
# Output: The same image with the diagonal non-edge pixels interpolated
def interpDiag(original,img, T, k):
    lx, ly = img.shape
    imgPadded = np.zeros((lx+4,ly+4))# Pad by 1 given pixel (2 real pixels) on each side
    imgPadded[2:-2,2:-2] = img

    # Think about each point in d1 and d2 as the (x,y) of the points diagonally between
    # each of the pixels being differenced (thus a 4x4 space would become a 3x3 space of 
    # the pixels diagonal from each 4 surrounding pixels of the original image)
    d1 = np.abs(original[1:,:-1] - original[:-1,1:])
    d2 = np.abs(original[1:,1:] - original[:-1,:-1])
    d1 = cv2.copyMakeBorder(d1, 1,0,1,0, cv2.BORDER_CONSTANT,value=0)
    d2 = cv2.copyMakeBorder(d2, 1,0,1,0, cv2.BORDER_CONSTANT,value=0)

    # print(original)
    # print(d2)

    # d1 = cv2.copyMakeBorder(d1, 2,2,2,2, cv2.BORDER_CONSTANT,value=0)
    # d2 = cv2.copyMakeBorder(d2, 2,2,2,2, cv2.BORDER_CONSTANT,value=0)

    # Center at the point to be interpolated, (x,y)
    for x in range(3, lx+1, 2):
        for y in range(3, ly+1, 2):  
            s4x4 = imgPadded[x-3:x+4:2,y-3:y+4:2] # 4x4 of the original image
            d1s = np.sum(d1[(x-3)//2-1:(x-3)//2+2, (y-3)//2-1:(y-3)//2+2]) # 3x3 region of differences around x,y
            d2s = np.sum(d2[(x-3)//2-1:(x-3)//2+2, (y-3)//2-1:(y-3)//2+2])

            # print(f"({(x-3)//2},{(y-3)//2}): {d1[(x-3)//2-1:(x-3)//2+2, (y-3)//2-1:(y-3)//2+2]}")

            # if x >= 3+0 and x < 3+3 and y >= 3+0 and y < 3+3:
                # print(f"({x-3},{y-3}): {d1s} : {d2s}")
                # print(original[x-1:x+2, y-1:y+2])
                # print(s4x4)
                # print(d1[x-1:x+2, y-1:y+2])
                # print(d2[x-1:x+2, y-1:y+2])

            # Get classification
            diagClass = DiagClassification.SMOOTH
            if 100*(1+d1s) > T * (1+d2s):
                diagClass = DiagClassification.UP_RIGHT
            elif 100*(1+d2s) > T * (1+d1s):
                diagClass = DiagClassification.DOWN_RIGHT

            
            # imgPadded[x,y] = upRight(s4x4)
            # imgPadded[x,y] = downRight(s4x4)
            # imgPadded[x,y] = diagSmooth(s4x4, d1s, d2s, k)

            if diagClass == DiagClassification.UP_RIGHT:
                imgPadded[x,y] = upRight(s4x4)
                # print(f"{(x-3)//2}, {(y-3)//2} up")
            elif diagClass == DiagClassification.DOWN_RIGHT:
                # print(f"{(x-3)//2}, {(y-3)//2} down")
                imgPadded[x,y] = downRight(s4x4)
            else:
                # print(f"{(x-3)//2}, {(y-3)//2} smooth")
                imgPadded[x,y] = diagSmooth(s4x4, d1s, d2s, k)
                
    return imgPadded[2:-2,2:-2]

def interpOrth(img, T, k):
    lx, ly = img.shape
    imgPadded = np.zeros((lx+6,ly+6))
    imgPadded[3:-3,3:-3] = img
    

    # Each (x,y) is the uninterpolated pixel between the diff. It works out that
    # The [unused] diffs surrounding original or diagonally interpolated pixels
    # is equal to 0
    d1 = np.abs(imgPadded[2:-4,3:-3] - imgPadded[4:-2,3:-3])
    d2 = np.abs(imgPadded[3:-3, 2:-4] - imgPadded[3:-3, 4:-2])

    d1 = cv2.copyMakeBorder(d1, 3,3,3,3, cv2.BORDER_CONSTANT,value=0)
    d2 = cv2.copyMakeBorder(d2, 3,3,3,3, cv2.BORDER_CONSTANT,value=0)

    # print(f"\nimg:\n{img}")
    # print(f"d1:\n{d1}")
    # print(f"d2:\n{d2}\n")

    # Center at the point to be interpolated, (x,y), as well as (x-1, y+1)
    for x in range(4, lx+3, 2):
        for y in range(3, ly+3, 2): 
            s7x7 = imgPadded[x-3:x+4,y-3:y+4]

            d1s = d1[x,y] + d1[x+2,y] + d1[x-2,y] + d1[x,y+2] + d1[x,y-2]
            d2s = d2[x,y] + d2[x+2,y] + d2[x-2,y] + d2[x,y+2] + d2[x,y-2]


            # Match classification and interpolate for x,y
            orthClass = OrthClassification.SMOOTH
            if  (100 * (1 + d1s) > T * (1 + d2s)):
                orthClass = OrthClassification.HORIZONTAL
            elif ( 100 * (1 + d2s) > T * (1 + d1s)):
                orthClass = OrthClassification.VERTICAL
                
            if orthClass == OrthClassification.HORIZONTAL:
                imgPadded[x,y] = horizontal(s7x7)
            elif orthClass == OrthClassification.VERTICAL:
                imgPadded[x,y] = vertical(s7x7)
            else:
                imgPadded[x,y] = orthSmooth(s7x7, d1s, d2s, k)

    for x in range(3, lx+3, 2):
        for y in range(4, ly+3, 2): 
            s7x7 = imgPadded[x-3:x+4,y-3:y+4]
            d1s = d1[x,y] + d1[x+2,y] + d1[x-2,y] + d1[x,y+2] + d1[x,y-2]
            d2s = d2[x,y] + d2[x+2,y] + d2[x-2,y] + d2[x,y+2] + d2[x,y-2]

            orthClass = OrthClassification.SMOOTH
            if  (100 * (1 + d1s) > T * (1 + d2s)):
                orthClass = OrthClassification.HORIZONTAL
            elif ( 100 * (1 + d2s) > T * (1 + d1s)):
                orthClass = OrthClassification.VERTICAL

            if orthClass == OrthClassification.HORIZONTAL:
                imgPadded[x,y] = horizontal(s7x7)
            elif orthClass == OrthClassification.VERTICAL:
                imgPadded[x,y] = vertical(s7x7)
            else:
                imgPadded[x,y] = orthSmooth(s7x7, d1s, d2s, k)

    return imgPadded[3:-3,3:-3]

# Input: 7x7 padded "diamond" area
# Output: Classification
def classifyOrth(s2, T):

    # Avoiding floating point error
    if  (100 * (1 + d1) > T * (1 + d2)):
        return OrthClassification.HORIZONTAL
    elif ( 100 * (1 + d2) > T * (1 + d1)):
        return OrthClassification.VERTICAL
    else:
        return 



# Input: 4x4 area
# Output: 7x7 interpolated area (Only diagonals used)
def upRight(s):
    #(-1 * P(0, 0) + 9 * P(1, 1) + 9 * P(2, 2) - 1 * P(3, 3)) / 16
    op = (-1 * s[0,0] + 9 * s[1,1] + 9 * s[2,2] + (-1)*s[3,3]) / 16
    op = 255 if op > 255 else op
    op = 0 if op < 0 else op
    return op

# Input: 4x4 area
# Output: 7x7 interpolated area (Only diagonals used)
def downRight(s):
    #Output pixel = (-1 * P(3, 0) + 9 * P(2, 1) + 9 * P(1, 2) - 1 * P(0, 3)) / 16
    op = ((-1)*s[3,0] + 9 * s[1,2] + 9* s[2,1] + (-1)*s[0,3] ) / 16
    op = 255 if op > 255 else op
    op = 0 if op < 0 else op
    return op

# Input: 4x4 area
# Output: 7x7 interpolated area (Only diagonals used)
def diagSmooth(s,d1,d2, k):
    w1 = 1 / (1 + d1**k)
    w2 = 1 / (1 + d2**k)
    weight1 = w1 / (w1 + w2)
    weight2 = w2 / (w1 + w2)

    downRightPixel = (-1 * s[0,0] + 9 * s[1, 1] + 9 * s[2, 2] - 1 * s[3, 3]) / 16
    upRightPixel = (-1 * s[3,0] + 9 * s[2,1] + 9 * s[1,2] - 1 * s[0,3]) / 16

    op = downRightPixel * weight1 + upRightPixel * weight2
    op = 255 if op > 255 else op
    op = 0 if op < 0 else op
    return op

# Input: 7x7 padded "diamond" area
# Output: 7x7 interpolated area (Only orthogonals used)
def horizontal(s, x=3, y=3):
    op = (-1 * s[x, y-3] + 9 * s[x, y-1] + 9 * s[x, y+1] - 1 * s[x, y + 3]) / 16
    op = 255 if op > 255 else op
    op = 0 if op < 0 else op
    return op
# Input: 7x7 padded "diamond" area
# Output: 7x7 interpolated area (Only orthogonals used)
def vertical(s, x=3, y=3):
    op = (-1 * s[x-3, y] + 9 * s[x - 1, y] + 9 * s[x + 1, y] - 1 * s[x + 3, y]) / 16
    op = 255 if op > 255 else op
    op = 0 if op < 0 else op
    return op

# Input: 7x7 padded "diamond" area
# Output: 7x7 interpolated area (Only orthogonals used)
def orthSmooth(s, d1, d2, k):
    x,y = 3, 3
    w1 = 1 / (1 + d1 ** k)
    w2 = 1 / (1 + d2 ** k)
    weight1 = w1 / (w1 + w2)
    weight2 = w2 / (w1 + w2)

    horizontalPixel = (-1 * s[x-3, y] + 9 * s[x-1, y] + 9 * s[x+1, y] - 1 * s[x+3, y]) / 16
    veritcalPixel = (-1 * s[x, y-3] + 9 * s[x, y-1] + 9 * s[x, y+1] - 1 * s[x, y+3]) / 16

    op = horizontalPixel * weight1 + veritcalPixel * weight2
    op = 255 if op > 255 else op
    op = 0 if op < 0 else op
    return op
