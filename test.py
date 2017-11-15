import cv2
import numpy as np
import time
import packages.dcci as dcci
import img_resources as imr

dcci_time = time.time()
bicubic_time = time.time()
lenczos_time = time.time()

# Init
window_name = "UpScaling"

for file in imr.rpg_items:
    print(file)
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)[::2, ::2]
    img2 = dcci.Dccix2(img)
    print('DCCI took {}'.format(dcci_time - time.time()))

    bicubic = cv2.resize(img, (0,0), fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    print('Bicubic took {}'.format(bicubic_time - time.time()))
    lenczos = cv2.resize(img, (0,0), fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4)
    print('Lanczos took {}'.format(lenczos_time - time.time()))

    cv2.imshow(window_name, img)
    cv2.imshow(window_name + " DCCI ", np.uint8(np.round(img2)))

    cv2.imshow(window_name + " Bicubic ", bicubic)
    cv2.imshow(window_name + " Lenczos ", lenczos)

    # Exit application
    cv2.waitKey(0)
    cv2.destroyAllWindows()