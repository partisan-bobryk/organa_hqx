import cv2
import numpy as np
import time
import packages.dcci as dcci

dcci_time = time.time()
bicubic_time = time.time()
lenczos_time = time.time()

# Init
window_name = "UpScaling"
file1 = "./resources/link.png"
file2 = "./resources/multi_grayscale_1_100x100.tif"
file3 = "./resources/diagonal_left_100x100.tif"
file4 = "./resources/peppers_color.tif"

img = cv2.imread(file4, cv2.IMREAD_GRAYSCALE)[::2, ::2]
img2 = dcci.Dccix2(np.float64(img))
print('DCCI took {}'.format(dcci_time - time.time()))
img2[img2 > 255] = 255
img2[img2 < 0] = 0

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