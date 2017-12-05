import cv2
import numpy as np
import packages.dcci as dcci
import img_resources as imr

# Init
window_name = "UpScaling"

N = 1 # 2^N scaling
# Ts, ks = range(100,151,5), range(0,7,1)# Used for testing T/k values
Ts, ks = [115], [5] # Default T/k's; use for single/fast image

for file in imr.rpg_items:
    print(file)
    img = cv2.imread(file, cv2.IMREAD_COLOR)
    img2=np.array([])
    for k in ks:
        img3 = np.array([])
        for T in Ts:
            img2b = dcci.Dccix2(img[:,:,0], T, k)
            img2g = dcci.Dccix2(img[:,:,1], T, k)
            img2r = dcci.Dccix2(img[:,:,2], T, k)

            for i in range(1,N):
                img2b = dcci.Dccix2(img2b, T, k)
                img2g = dcci.Dccix2(img2g, T, k)
                img2r = dcci.Dccix2(img2r, T, k)
            
            img4 = np.stack((img2b,img2g,img2r),axis=2)
            if img3.shape[0] == 0:
                img3 = img4
            else:
                img3 = np.concatenate((img3,img4), axis=1)
        
        if img2.shape[0] == 0:
            img2 = img3
        else:
            img2 = np.concatenate((img2,img3), axis=0)

    cv2.imwrite("./output/latest-tk_test.png", img2)
    cv2.imshow(f"{window_name} - {file}", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()