import cv2
import os
import time
pwd = "/root/autodl-tmp/imse4175"
videos_src_path = pwd + "/videos"   
frames_save_path = pwd + "/img_data/images/"
width = 720
height = 480
time_interval = 10
def video2frame(video_src_path, frame_save_path, frame_width, frame_height, interval):
    """
    Extract frames in the video.
    :param video_src_path: the path storing videos
    :param frame_save_path:　save frame to this path
    :param frame_width:　frame width
    :param frame_height:　frame height
    :param interval:　time interval between frame
    """
    videos = os.listdir(video_src_path)
    for each_video in videos:
        print("processing: ", each_video)    
        each_video_name = each_video[:-4]
        os.makedirs(frame_save_path + each_video_name)
        each_video_save_full_path = os.path.join(frame_save_path, each_video_name) 
        each_video_full_path = os.path.join(video_src_path, each_video)
        cap = cv2.VideoCapture(each_video_full_path)
        frame_index = 0
        frame_count = 0
        if cap.isOpened():
            success = True
        else:
            success = False
            print("Processing failed.")
        while(success):
            success, frame = cap.read()
            print("---> Extracting frame%d:" % frame_index, success)      
            if frame_index % interval == 0 and success:    
                resize_frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
                cv2.imwrite(each_video_save_full_path + "/" + each_video_name + "%d.jpg" % frame_count, resize_frame)
                frame_count += 1
            frame_index += 1
        cap.release()		
def main():
    video2frame(videos_src_path, frames_save_path, width, height, time_interval)
if __name__ == '__main__':
    main()