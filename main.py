import cv2
import numpy as np
import packages.dcci as dcci
from img_resources import files

# Init
window_name = "UpScaling"

for file in files:
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    img2 = dcci.Dccix2(np.float64(img[::2, ::2]))
    img2 = dcci.Dccix2(img2)
    img2[img2 > 255] = 255
    img2[img2 < 0] = 0
    img2 = np.uint8(np.round(img2))

    print(img2.shape)

    cv2.imshow(window_name, img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()