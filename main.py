import cv2
import numpy as np
import packages.dcci as dcci
import img_resources as imr

# Init
window_name = "UpScaling"

N = 3 # 2^N scaling
pad = 4


# f = np.zeros((32,32,3), dtype=np.uint8)

# f += 64
# # f *= 2
# cv2.imwrite("resources/stripes.png", f)


# img = np.array(range(0,4))**2
# img = [img]
# # img = np.matmul(img,img.transpose())
# img = np.matmul(np.transpose(img),img)
# print(f"Original:\n{img}")

# imgO = dcci.Dccix2(img)

# print(f"Output:\n{imgO}")

for file in imr.rpg_items_sheet:
    print(file)
    imgT = cv2.imread(file, cv2.IMREAD_COLOR)

    y,x,z = imgT.shape
    img = np.zeros((y+2*pad, x+2*pad,z), dtype=np.uint8)
    img[pad:-pad,pad:-pad] = imgT

    img = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)

    for n in range(0,N):
        imgB = dcci.Dccix2(img[:,:,0])
        imgG = dcci.Dccix2(img[:,:,1])
        imgR = dcci.Dccix2(img[:,:,2])
        img = np.stack((imgB, imgG, imgR), axis=2)

    img = img[(2**N)*pad:-(2**N)*pad,(2**N)*pad:-(2**N)*pad]
    img = cv2.cvtColor(img, cv2.COLOR_Lab2BGR)


    img2 = cv2.resize(imgT, (0,0), fx=2**N, fy=2**N, interpolation=cv2.INTER_CUBIC)
    img2 = img2[:-(2**N-1),:-(2**N-1)]
    b = np.uint8(np.zeros((img.shape[0],4,3)) + (0,0,255))


    imgOut = np.concatenate((img,b,img2), axis=1)
    cv2.imwrite("./output/latest.png", imgOut)
    # cv2.imwrite("./output/latest-bicubic.png", img2)
        # cv2.imshow(f"{window_name} - {file}2", img2)
    cv2.imshow(f"{window_name} (DCCI : Bicubic)- {file}", imgOut)
    cv2.waitKey(0)
    cv2.destroyAllWindows()