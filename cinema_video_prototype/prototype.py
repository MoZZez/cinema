import numpy as np
import cv2
import  dill

from sklearn.externals import joblib
from sklearn.ensemble import ExtraTreesClassifier

from os import listdir
from os.path import isfile, join

import xlwt
import xlrd

#first version of script
#working model ExtraTrees trained on imbalanced set(does not metter for trees)
#average accuracy ~96% on balanced test set

class marker(object):
    def __init__(self,model_path='model_v2.pkl',boxes_path='boxes_1.pkl'):
        #loading model
        self.model=joblib.load(model_path)
        self.labels_dict={1:'occupied',2:'free'}
        #here is support points to build bounding boxes around every seat
        r_strm=open(boxes_path,'rb')
        points=dill.load(r_strm)
        r_strm.close()

        #content of every bounding bow will be reshaped to this
        self.stnd_size=(20,30)
        #reshape them so for every box we have to points 1,2
        #1 -upper left angle,2-lower right angle
        self.boxes=[]
        for i in range(0,len(points),2):
            box=[points[i],points[i+1]]
            self.boxes.append(box)

    #default version:indexing places with nat. numbers 1....n
    def write_to_file(self,preds,path='occupation_table.xls'):

        wb=xlwt.Workbook(encoding="utf-8")
        sheet1 = wb.add_sheet("Sheet 1")
          
        for i in range(len(preds[0])):
            sheet1.write(i,0,str(i+1))

        for i in range(len(preds)):
            for j in range(len(preds[i])):
                sheet1.write(j,i+1,self.labels_dict[int(preds[i][j])])
                
        wb.save(path)
        return 0
    
    def predict(self,img):
        preds=[]
        #if picture is gray or colored
        if len(img.shape)>2:
            img_to_show=np.array(img)
            img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        elif len(img.shape)==2:
            img_to_show=cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

        font = cv2.FONT_HERSHEY_PLAIN 
        #main cycle   
        for i in range(len(self.boxes)):
            #points 1,2
            pt1=self.boxes[i][0]
            pt2=self.boxes[i][1]

            #getting and proccesing content of box
            sample=img[pt1[1]:pt2[1],pt1[0]:pt2[0]]
            sample=cv2.resize(sample,self.stnd_size)
            sample=np.reshape(sample,(1,sample.shape[0]*sample.shape[1]))

            #getting label for sample
            #1-man,2-no man
            pred=self.model.predict(sample)
            preds.append(pred)

            #if man is in box paining box red otherwise green
            pt1=tuple(pt1)
            pt2=tuple(pt2)

            #write seat`s number
                        
            if pred==2:
                cv2.rectangle(img_to_show,pt1,pt2,(0,255,0),1)
                cv2.putText(img_to_show,str(i+1),pt1, font, 1, (0,255,0),1)
            else:
                cv2.putText(img_to_show,str(i+1),pt1, font, 1, (0,0,255),1)
                cv2.rectangle(img_to_show,pt1,pt2,(0,0,255),1)
        #returning marked pictures and all preds,so having boxes array and preds you can match them
        return  img_to_show,preds
    
    def process_video(self,file_path='video.wmv',from_cam=False,frequency=5):
        #catching video stream
        if from_cam==False:
            vc=cv2.VideoCapture(file_path)
        else:
            #0-first avaliable camera connected to PC,may change it by changing index
            vc=cv2.VideoCapture(0)
            
        frame_cnt=0
        preds=[]
        while True:
            #reading frames from video stream ret-indicator of success
            #we read every frequency frame
            
            for i in range(frequency):
             ret,frame=vc.read()
              
            ret,frame=vc.read()
            
            frame_cnt+=1
            if ret==False:
                print 'video is finised or some error have occured'
                break
            print frame.shape
            
            img_to_show,pred=self.predict(frame)
            print img_to_show.shape
            preds.append(pred)
            cv2.imwrite(str(frame_cnt)+'.jpg',img_to_show)
        
        self.write_to_file(preds)

            

            
                
    
#demonstration

mark=marker()
mark.process_video(frequency=5000)
