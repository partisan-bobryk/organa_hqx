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

def isColor(img):
    return len(img.shape) == 3

def Dcci(img, N=1, T=155, k=5):
    COLOR_PAD = 4
    if isColor(img):
        y,x,z = img.shape
        imgP = np.zeros((y+2*COLOR_PAD, x+2*COLOR_PAD,z), dtype=np.uint8)
        imgP[COLOR_PAD:-COLOR_PAD,COLOR_PAD:-COLOR_PAD] = img
        img = cv2.cvtColor(imgP, cv2.COLOR_BGR2Lab)

        imgB = dcciN(img[:,:,0], N, T, k)
        imgG = dcciN(img[:,:,1], N, T, k)
        imgR = dcciN(img[:,:,2], N, T, k)
        img = np.stack((imgB, imgG, imgR), axis=2)

        img = img[(2**N)*COLOR_PAD:-(2**N)*COLOR_PAD,(2**N)*COLOR_PAD:-(2**N)*COLOR_PAD]
        img = cv2.cvtColor(img, cv2.COLOR_Lab2BGR)
        return img
    
    return dcciN(img, N, T, k)


def dcciN(img, N, T, k):
    for i in range(0,N):
        img = dccix2(img,T,k)
    return img

def dccix2(img, T, k):
    img2 = np.float64(np.swapaxes(img, 0, 1))

    lx, ly = img2.shape
    imgInterp = np.zeros((lx*2-1, ly*2-1))
    imgInterp[::2,::2] = img2

    imgInterp = interpDiag(img2, imgInterp, T, k)
    imgInterp = interpOrth(imgInterp, T, k)

    imgInterp[imgInterp < 0] = 0
    imgInterp[imgInterp > 255] = 255
    imgInterp = np.uint8(np.round(imgInterp))
    
    return np.swapaxes(imgInterp, 0, 1)

def interpDiag(original,img, T, k):
    """
    Input:  The 2x image with black space padding each of the given pixels
    Output: The same image with the diagonal non-edge pixels interpolated
    """
    lx, ly = img.shape
    imgPadded = np.zeros((lx+4,ly+4))# Pad by 1 given pixel (2 real pixels) on each side
    imgPadded[2:-2,2:-2] = img

    # Think about each point in d1 and d2 as the (x,y) of the points diagonally between
    # each of the pixels being differenced (thus a 4x4 space would become a 3x3 space of 
    # the pixels diagonal from each 4 surrounding pixels of the original image)
    d1 = np.abs(original[1:,:-1] - original[:-1,1:])
    d2 = np.abs(original[1:,1:] - original[:-1,:-1])
    d1 = cv2.copyMakeBorder(d1, 1,1,1,1, cv2.BORDER_CONSTANT,value=0)
    d2 = cv2.copyMakeBorder(d2, 1,1,1,1, cv2.BORDER_CONSTANT,value=0)

    # Center at the point to be interpolated, (x,y)
    for x in range(3, lx+1, 2):
        for y in range(3, ly+1, 2): 
            rx, ry = x-2, y-2
            dx, dy = (rx+1)//2, (ry+1)//2
            s4x4 = imgPadded[x-3:x+4:2,y-3:y+4:2] # 4x4 of the original image
            d1k = d1[dx-1:dx+2, dy-1:dy+2] # 3x3 region of differences around x,y
            d2k = d2[dx-1:dx+2, dy-1:dy+2]

            d1s = np.sum(d1k)
            d2s = np.sum(d2k)

            diagClass = DiagClassification.SMOOTH
            if 100*(1+d1s) > T * (1+d2s):
                diagClass = DiagClassification.UP_RIGHT
            elif 100*(1+d2s) > T * (1+d1s):
                diagClass = DiagClassification.DOWN_RIGHT

            if diagClass == DiagClassification.UP_RIGHT:
                imgPadded[x,y] = upRight(s4x4)
            elif diagClass == DiagClassification.DOWN_RIGHT:
                imgPadded[x,y] = downRight(s4x4)
            else:
                imgPadded[x,y] = diagSmooth(s4x4, d1s, d2s, k)
                

    return imgPadded[2:-2,2:-2]

def interpOrth(img, T, k):
    PAD = 4
    lx, ly = img.shape
    imgPadded = np.zeros((lx+2*PAD,ly+2*PAD))
    imgPadded[PAD:-PAD,PAD:-PAD] = img
    
    # Each (x,y) is the uninterpolated pixel between the diff. It works out that
    # The [unused] diffs surrounding original or diagonally interpolated pixels
    # is equal to 0
    d1 = np.abs(imgPadded[(PAD-1):-(PAD+1),PAD:-PAD] - imgPadded[(PAD+1):-(PAD-1),PAD:-PAD])
    d2 = np.abs(imgPadded[PAD:-PAD, (PAD-1):-(PAD+1)] - imgPadded[PAD:-PAD, (PAD+1):-(PAD-1)])

    d1 = cv2.copyMakeBorder(d1, PAD,PAD,PAD,PAD, cv2.BORDER_CONSTANT,value=0)
    d2 = cv2.copyMakeBorder(d2, PAD,PAD,PAD,PAD, cv2.BORDER_CONSTANT,value=0)

    #    First Loop
    #   o x o x o x o
    #   . o . o . o .
    #   o x o x o x o
    #   . o . o . o .
    #   o x o x o x o
    #   . o . o . o .
    #   o x o x o x o
    #
    #    2nd Loop
    #   o . o . o . o
    #   x o x o x o .
    #   o . o . o . o
    #   x o x o x o .
    #   o . o . o . o
    #   x o x o x o .
    #   o . o . o . o

    # Center at the point to be interpolated, (x,y), as well as (x-1, y+1)
    for x in range(PAD+1, lx+PAD, 2):
        for y in range(PAD, ly+PAD, 2): 
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

    for x in range(PAD, lx+PAD, 2):
        for y in range(PAD+1, ly+PAD, 2): 
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

    return imgPadded[PAD:-PAD,PAD:-PAD]

def upRight(s):
    """
    Input:  4x4 area
    Output: 7x7 interpolated area (Only diagonals used)
    """
    op = (-1 * s[0,0] + 9 * s[1,1] + 9 * s[2,2] + (-1)*s[3,3]) / 16
    op = 255 if op > 255 else op
    op = 0 if op < 0 else op
    return op

def downRight(s):
    """
    Input:  4x4 area
    Output: 7x7 interpolated area (Only diagonals used)
    """
    op = ((-1)*s[3,0] + 9 * s[1,2] + 9* s[2,1] + (-1)*s[0,3] ) / 16
    op = 255 if op > 255 else op
    op = 0 if op < 0 else op
    return op

def diagSmooth(s,d1,d2, k):
    """
    Input:  4x4 area
    Output: 7x7 interpolated area (Only diagonals used)
    """
    w1 = 1 / (1 + d1**k)
    w2 = 1 / (1 + d2**k)
    weight1 = w1 / (w1 + w2)
    weight2 = w2 / (w1 + w2)

    downRightPixel = (-1 * s[0,0] + 9 * s[1,1] + 9 * s[2,2] - 1 * s[3,3]) / 16
    upRightPixel   = (-1 * s[3,0] + 9 * s[2,1] + 9 * s[1,2] - 1 * s[0,3]) / 16

    op = downRightPixel * weight1 + upRightPixel * weight2
    op = 255 if op > 255 else op
    op = 0 if op < 0 else op
    return op

def horizontal(s, x=3, y=3):
    """
    Input:  7x7 padded "diamond" area
    Output: 7x7 interpolated area (Only orthogonals used)
    """
    op = (-1 * s[x, y-3] + 9 * s[x, y-1] + 9 * s[x, y+1] - 1 * s[x, y + 3]) / 16
    op = 255 if op > 255 else op
    op = 0 if op < 0 else op
    return op

def vertical(s, x=3, y=3):
    """
    Input:  7x7 padded "diamond" area
    Output: 7x7 interpolated area (Only orthogonals used)
    """
    op = (-1 * s[x-3, y] + 9 * s[x - 1, y] + 9 * s[x + 1, y] - 1 * s[x + 3, y]) / 16
    op = 255 if op > 255 else op
    op = 0 if op < 0 else op
    return op

def orthSmooth(s, d1, d2, k):
    """
    Input:  7x7 padded "diamond" area
    Output: 7x7 interpolated area (Only orthogonals used)
    """
    x,y = 3, 3
    w1 = 1 / (1 + d1 ** k)
    w2 = 1 / (1 + d2 ** k)
    weight1 = w1 / (w1 + w2)
    weight2 = w2 / (w1 + w2)

    horizontalPixel = (-1 * s[x-3, y] + 9 * s[x-1, y] + 9 * s[x+1, y] - 1 * s[x+3, y]) / 16
    veritcalPixel   = (-1 * s[x, y-3] + 9 * s[x, y-1] + 9 * s[x, y+1] - 1 * s[x, y+3]) / 16

    op = horizontalPixel * weight1 + veritcalPixel * weight2
    op = 255 if op > 255 else op
    op = 0 if op < 0 else op
    return op
