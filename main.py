import cv2
import numpy as np
import packages.dcci as dcci

# Init
window_name = "UpScaling"
files = [
    "./resources/bonzai.tif",
    "./resources/cameraman.tif",
    "./resources/diagonal_left_100x100.tif",
    "./resources/grayscale_test_1.png",
    "./resources/house.tif",
    "./resources/jetplane.tif",
    "./resources/lake.tif",
    # "./resources/lena_color_256.tif",
    # "./resources/lena_color_512.tif",
    "./resources/lena_gray_256.tif",
    # "./resources/lena_gray_512.tif",
    "./resources/link.png",
    "./resources/livingroom.tif",
    # "./resources/mandril_color.tif",
    "./resources/mandril_gray.tif",
    "./resources/multi_grayscale_1_100x100.tif",
    # "./resources/peppers_color.tif",
    "./resources/peppers_gray.tif",
    "./resources/pirate.tif",
    "./resources/plus_100x100.tif",
    "./resources/walkbridge.tif",
    "./resources/woman_blonde.tif",
    "./resources/woman_darkhair.tif",
]

for file in files:
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    img2 = dcci.Dccix2(np.float64(img[::2, ::2]))
    img2 = dcci.Dccix2(img2)
    img2[img2 > 255] = 255
    img2[img2 < 0] = 0
    img2 = np.uint8(np.round(img2))

    bicubic = cv2.resize(img[::2,::2],(0,0), fx=4., fy=4., interpolation=cv2.INTER_CUBIC)

    print(img2.shape)
    print(bicubic.shape)

    cv2.imshow(window_name, np.concatenate((bicubic[:-3,:-3],img2), axis=1))
    cv2.waitKey(0)
    cv2.destroyAllWindows()