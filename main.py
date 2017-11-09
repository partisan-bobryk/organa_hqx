import cv2
import numpy as np
import packages.dcci as dcci

# Init
window_name = "UpScaling"
file1 = "./resources/link.png"
file2 = "./resources/multi_grayscale_1_100x100.tif"
file3 = "./resources/diagonal_left_100x100.tif"
file4 = "./resources/peppers_color.tif"

img = cv2.imread(file4, cv2.IMREAD_GRAYSCALE)[::2, ::2]
img2 = dcci.Dccix2(np.float64(img))
img2[img2 > 255] = 255
img2[img2 < 0] = 0

print(img2.shape)
# Exit application
cv2.imshow(window_name, img)
cv2.imshow(window_name + "2", np.uint8(np.round(img2)))
cv2.waitKey(0)
cv2.destroyAllWindows()