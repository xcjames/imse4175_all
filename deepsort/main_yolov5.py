import os
import random

import cv2
from ultralytics import YOLO

from tracker import Tracker

import torch
import sys
#/root/autodl-tmp/imse4175/videos/2ndVideo.mp4     /root/autodl-tmp/long_hk_videos/VID_20240228_171754.mp4
# video_name = "petal_20240306_225032.mp4"
# video_path = os.path.join("/root/autodl-tmp/",video_name)
#Use this command: python main_yolov5.py {video path} {.pt yolo model path}
video_path = sys.argv[1]
yolo_model_path = sys.argv[2]
video_out_path = os.path.join('.', video_path.split("/")[-1].split(".")[0]+'_yolov5_out.mp4')
categories = ['person', 'car', 'dog','bicycle', 'e-bike', 'other vehicles', "stroller", "scooter"]
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

height = frame.shape[0]
width = frame.shape[1]


cap_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'MP4V'), cap.get(cv2.CAP_PROP_FPS),
                          (frame.shape[1], frame.shape[0]))

# model = YOLO("/root/autodl-tmp/yolov5/runs/train/exp24_CCTV/weights/best.pt")
# /root/autodl-tmp/yolov5/yolov5s.pt
# model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
#/root/autodl-tmp/yolov5/runs/train/exp3_summary_all/weights/best.pt
# model = torch.hub.load('/root/autodl-tmp/yolov5', 'custom', path='/root/autodl-tmp/yolov5/runs/train/exp23_rgb/weights/best.pt', source='local')
model = torch.hub.load('/root/autodl-tmp/yolov5', 'custom', path=yolo_model_path, source='local')


# model = YOLO("yolov8n.pt")
tracker = Tracker()

colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for j in range(10)]

detection_threshold = 0.5

#Counting:
objects_num_list= [0,0,0,0,0,0,0,0]
objects_num=0
offset=20
pos = 600
already_tracked_id = []

count_img = 0
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

while ret:
    r_img = model(frame)
    results = r_img.xyxy
    count_img+=1  
    print(count_img, " images detected among ", total)     
    for result in results:#iterate each image   
        pos = height-int((height/10)*3)
        left_pt = int((width)/20)
        right_pt = width-left_pt
        
        vert_left_x = int((width)/3)
        vert_up_y = int((height)/3)
        vert_below_y = int((height)/3)*2

        cv2.line(frame, (left_pt, pos), (right_pt, pos), (255,127,0), 3)
        cv2.line(frame, (vert_left_x, vert_up_y), (vert_left_x, vert_below_y), (255,127,0), 3)
        detections = []
        # class_id_list = []
        for r in result:#in one image, iterate detections
            x1, y1, x2, y2, score, class_id = r
            x1 = int(x1)
            x2 = int(x2)
            y1 = int(y1)
            y2 = int(y2)
            class_id = int(class_id)
            if score > detection_threshold:
                detections.append([x1, y1, x2, y2, score, class_id])
                # class_id_list.append(class_id)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (colors[class_id % len(colors)]), 3)
            cv2.putText(frame, categories[class_id], (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
            
        
        tracker.update(frame, detections)
        
        for track in tracker.tracks:
            tr_x1, tr_y1, tr_x2, tr_y2 = track.bbox
            track_id = track.track_id
            class_id = track.class_id
            # print("i, class_id_list", i, class_id_list)
            # cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
            cv2.circle(frame, (int((tr_x1+tr_x2)/2), int((tr_y1+tr_y2)/2)), 4, (0, 0,255), -1)
            cv2.putText(frame, str(track_id), (int(tr_x2), int(tr_y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            if (  ((((tr_x1+tr_x2)/2)< vert_left_x+offset and ((tr_x1+tr_x2)/2)> vert_left_x-offset ) or 
                   (((tr_y1+tr_y2)/2)< pos+offset and ((tr_y1+tr_y2)/2)>(pos-offset))) 
                   and (track_id not in already_tracked_id)):
                objects_num_list[class_id] += 1 # number of objects of a certain type
                objects_num += 1
                already_tracked_id.append(track_id)
                # cv2.line(frame1, (25, pos), (1200, pos), (255,127,0), 3) #画线条
                cv2.line(frame, (left_pt, pos), (right_pt, pos), (0,127,255), 3) #换一个颜色，表明这辆车已经被计入了。 
                cv2.line(frame, (vert_left_x, vert_up_y), (vert_left_x, vert_below_y), (0,127,255), 3)
        
            # cv2.putText(frame, categories[class_id]+str(track_id), (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
        # counting_str = str("Total: "+str(objects_num)+"\n"+
        #                 'person: '+str(objects_num_list[0])+"\n"+
        #                   'car:'+str(objects_num_list[1])+"\n"+
        #                     'dog:'+str(objects_num_list[2])+"\n"+
        #                     'bicycle:'+str(objects_num_list[3])+"\n"+
        #                      'e-bike:'+str(objects_num_list[4])+"\n"+
        #                        'other:'+str(objects_num_list[5]))
        for r in range(0,len(objects_num_list)):
            cv2.putText(frame, categories[r]+":"+str(objects_num_list[r]), (left_pt, int((left_pt/2)*(r+1))), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255),1)
        
    cap_out.write(frame)
    ret, frame = cap.read()

cap.release()
cap_out.release()
cv2.destroyAllWindows()
