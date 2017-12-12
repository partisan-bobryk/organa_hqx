import cv2
import numpy as np
import packages.organa as organa
import img_resources as imr

# Init
window_name = "UpScaling"

N = 1 # 2^N scaling

# timg = np.zeros((7,7), dtype=np.uint8) +255
# timg[2:-2:2,2:-2:2] = 0

# timg = np.array([[255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
#                  [255, 255, 255, 255,   0, 255,   0, 255, 255, 255, 255],
#                  [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
#                  [255, 255, 255,   0, 255,   0, 255,   0, 255, 255, 255],
#                  [255,   0, 255, 255, 255,   0, 255, 255, 255,   0, 255],
#                  [255, 255, 255,   0,   0,   0,   0,   0, 255, 255, 255],
#                  [255,   0, 255, 255, 255,   0, 255, 255, 255,   0, 255],
#                  [255, 255, 255,   0, 255,   0, 255,   0, 255, 255, 255],
#                  [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
#                  [255, 255, 255, 255,   0, 255,   0, 255, 255, 255, 255],
#                  [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]], dtype=np.uint8)

# for imgT in [timg]:
#     cv2.imshow(f"{window_name}", organa.Organa(imgT))
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


for file in imr.test_images[7:8]:
    print(file)
    imgT = cv2.imread(file, cv2.IMREAD_COLOR)
    img = organa.Organa(imgT,N)

    img2 = cv2.resize(imgT, (0,0), fx=2**N, fy=2**N, interpolation=cv2.INTER_CUBIC)
    img2 = img2[:-(2**N-1),:-(2**N-1)]

    b = np.uint8(np.zeros((img.shape[0],4,3)) + (0,0,255))

    imgOut = np.concatenate((img,b,img2), axis=1)
    cv2.imshow(f"{window_name} (DCCI : Bicubic)- {file}", imgOut)
    cv2.waitKey(0)
    cv2.destroyAllWindows()