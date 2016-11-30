import cv2
import numpy as np
import dill
from os import listdir
from os.path import isfile, join


class patcher(object):
    def __init__(self,from_patch=0,from_img=0):
        self.box_ar=[]
        self.mark_cnt=0
        self.box=[]
    def patch(self,img):
        #let it all be std sized images
        stnd_size=(704,576)
        patch_size=(3,3)
        if len(img.shape)==3:
            img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        img=cv2.resize(img,stnd_size)
        #sliding window border thickness,patch_size
        bt=2
        #patch_size=(64,64)
        #image to renew image we will show,image we will map with frames
        img_cvt=cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
        img_mapped=np.array(img_cvt)
    
        #that is one for showing
        img_tmp=np.zeros(shape=(stnd_size[1]+2*bt,stnd_size[0]+2*bt,3),dtype=np.uint8)
        
        #adding borders to colored clean image
        img_tmp[bt:-bt,bt:-bt,:]=img_mapped
        img_cvt=img_tmp
        
        i=40
        j=40

        #commands
        #NOTE:keys codes may differ on different OS and PC
        #use script get key codes to know them
        up=97
        down=100
        left=115
        right=119

        mark=109
        quit_=113

        #main loop

        while(True):
          img_tmp[bt:-bt,bt:-bt,:]=img_mapped
          
          #supporting points of sliding window rectangle
          pt=(i,j)
          #pt2=(i+patch_size[0],j+patch_size[1])

          #drawing rectangle
          img_tmp[i-2:i+3,j-2:j+3]=np.array([0,255,0])
    
          cv2.imshow("tmp_with_img",img_tmp)
          key=cv2.waitKey()
          print key
          if key==left:
             i+=5
          elif key==right:
             i-=5
          elif key==up:
             j-=5
          elif key==down:
             j+=5
         #mark current point
          elif key==mark:
             self.mark_cnt+=1
             print [i,j]
             self.box.append([i,j])
             if self.mark_cnt % 2==0:
                 pt1=self.box[-2]
                 pt2=self.box[-1]
                 
                 pt1.reverse()
                 pt2.reverse()
                 
                 pt1=tuple(pt1)
                 pt2=tuple(pt2)
                 
                 cv2.rectangle(img_mapped,pt1,pt2,(0,255,0),1)
          elif key==quit_:
              cv2.destroyAllWindows()
              #cv2.imwrite(path_mapped+str(self.cur_img)+'.png',img_mapped)
             # self.cur_img+=1
              print self.box
              print 'returned'
              return 0
          #If we ran out of picture then go back
          if i<0:i=0
          if j<0:j=0
          if i+patch_size[0]>= img_tmp.shape[0]:i=img_tmp.shape[0]-patch_size[0]-1
          if j+patch_size[1]>= img_tmp.shape[1]:j=img_tmp.shape[1]-patch_size[1]-1

          
          img_tmp=np.zeros(shape=(stnd_size[1]+2*bt,stnd_size[0]+2*bt,3),dtype=np.uint8)


p=patcher()
#example for one photo

path='data/18-01_img_2.jpg'
img=cv2.imread(path)
print img.shape

p.patch(img)

boxes=p.box
print boxes

w_strm=open('boxes.pkl','wb')
dill.dump(boxes,w_strm)
w_strm.close()


