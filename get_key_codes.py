import numpy as np
import cv2

a=np.zeros((100,100),dtype=np.uint8)
for i in range(6):
           cv2.imshow('img',a)
           key=cv2.waitKey()
           print key
cv2.destroyAllWindows()
