import cv2
import numpy as np
import time
import packages.dcci as dcci
import img_resources as imr
import timeit

# Init
window_name = "UpScaling"

# img = cv2.imread(img_files.pixel_art[0], cv2.IMREAD_GRAYSCALE)

# def time_results(fn):
#     time_start = time.clock()
#     output = fn
#     time_stop = time.clock()
#     time_passed = time_stop - time_start
#     return output, time_passed


setup = '''
import cv2
import packages.dcci as dcci
import img_resources as imr
img = cv2.imread(imr.pixel_art[1], cv2.IMREAD_GRAYSCALE)
'''
N_dc=100
N_other=10000
dc = timeit.timeit('img2 = dcci.Dccix2(img)', setup=setup, number=N_dc)
print(f"DCCI took {dc/N_dc}s")
bc = timeit.timeit('img2 = cv2.resize(img, (0,0), fx=2, fy=2, interpolation=cv2.INTER_CUBIC)', setup=setup, number=N_other)
print(f"Bicubic took {bc/N_other}s")
lenc = timeit.timeit('img2 = cv2.resize(img, (0,0), fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4)', setup=setup, number=N_other)
print(f"Lenczos took {lenc/N_other}s")
# dcci_img, dcci_time = time_results(dcci.Dccix2(np.float64(img)))
# bicubic_img, bicubic_time = time_results()
# lenczos_img, lenczos_time = time_results(cv2.resize(img, (0,0), fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4))

# # Return time results
# print('DCCI took {}'.format(dcci_time))
# print('Bicubic took {}'.format(bicubic_time))
# print('lenczos took {}'.format(lenczos_time))

# cv2.imshow("Original TEST", img)
# cv2.imshow("DCCI TEST", dcci_img)
# cv2.imshow("Bicubic TEST", bicubic_img)
# cv2.imshow("lenczos TEST", lenczos_img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()