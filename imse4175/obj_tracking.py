import os
import cv2
# pwd = "/root/autodl-tmp/imse4175"
video_path = "root/autodl-tmp/imse4175/videos/1stVideo.mp4"
print(video_path)
cap = cv2.VideoCapture(video_path)
print(cap)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
print(frame_height)
size = (frame_width, frame_height) 
result = cv2.VideoWriter('./filename.mp4',  
                         cv2.VideoWriter_fourcc(*'XVID'), 
                         10, size) 
    
while(True): 
    ret, frame = cap.read() 
  
    if ret == True:  
  
        # Write the frame into the 
        # file 'filename.avi' 
        result.write(frame) 
  
        # Display the frame 
        # saved in the file 
        cv2.imshow('Frame', frame) 
  
        # Press S on keyboard  
        # to stop the process 
        if cv2.waitKey(1) & 0xFF == ord('s'): 
            break
  
    # Break the loop 
    else: 
        break
  
# When everything done, release  
# the video capture and video  
# write objects 
cap.release() 
result.release()



# ret, frame = cap.read()


# while ret:
#     cv2.imshow("frame",frame)
#     cv2.waitKey(20)
#     ret, frame = cap.read()
# cap.release()
cv2.destroyAllWindows()