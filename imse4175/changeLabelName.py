import os
path = "/root/autodl-tmp/imse4175/img_data/labels/"

video_dirs = os.listdir(path)#['1stVideoLabel0_20', '2ndVideoLabel0_20', '3rdVideoLabel0_20', '4_high_angleLabel0_20']

for video_dir in video_dirs:
    labels = os.listdir(os.path.join(path, video_dir))
    for label in labels:
        os.rename(os.path.join(path, video_dir, label), os.path.join(path, video_dir, video_dir + label))
    