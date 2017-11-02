import cv2
import numpy as np
import packages.dcci as dcci

# Init
window_name = ""
file = "./resources/bonzai.tif"

img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
img2 = dcci.Dccix2(img)

# Exit application
cv2.imshow(window_name, img2)
cv2.waitKey(0)
cv2.destroyAllWindows()