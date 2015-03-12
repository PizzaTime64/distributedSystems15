#@hadrianbsrg - hadrianbs.web.id

import cv2
import os
import time

start_time = time.time()
imgList = os.listdir(os.getcwd())
print imgList

for x in imgList:
    fileExt = os.path.splitext(x)
    if(fileExt[1] == '.py'):
        continue
    print x
    image = cv2.imread(x)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray_' + x, gray_image)
    

print "Computation time %s" %(time.time() - start_time)

#cv2.waitKey(0)
#cv2.destroyAllWindows()
