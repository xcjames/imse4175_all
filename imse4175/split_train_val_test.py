import os
import random
import shutil
import sys

#Before run this code, create 3 folders: train, val, test. Each folder containing 2 sub-directories: images, labels.
#Then, put all images and labels into the "/images" "/labels" in train
#Then the command: python split_train_val_test.py {path of the directory which contains /train, /val, and /test}

data_dir_path=sys.argv[1]
train_data_folder =data_dir_path+ "/train"
val_data_folder = data_dir_path+"/val"
test_data_folder = data_dir_path+"/test"
# 获取所有文件名（不包括子文件夹）
labels = sorted([f for f in os.listdir(train_data_folder+"/labels")])
images = sorted([f for f in os.listdir(train_data_folder+"/images")])
print(len(images),len(labels))
train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1
train_num = train_ratio*len(images)
val_num = val_ratio*len(images)
test_num = test_ratio*len(images)
#select the test set and val set randomly. 
val_spacing = int(1/val_ratio)
test_spacing = int(1/test_ratio)
for i in range(1,int(val_num)):
    # shutil.move(train_data_folder+"/images/"+"1stVideo0.jpg",val_data_folder+"/images/"+"1stVideo0.jpg")
    try:
        shutil.move(train_data_folder+"/images/"+images[(i*val_spacing)-1],val_data_folder+"/images/"+images[(i*val_spacing)-1])
        print("Already move",images[(i*val_spacing)-1],"to validation set")
        shutil.move(train_data_folder+"/labels/"+labels[(i*val_spacing)-1],val_data_folder+"/labels/"+labels[(i*val_spacing)-1])
        print("Already move",labels[(i*val_spacing)-1],"to validation set")
    except:
        print("Wrong when moving",images[(i*val_spacing)-1],"to validation set!!!!!!")
for i in range(1,int(test_num)):
    # shutil.move(train_data_folder+"/images/"+"1stVideo0.jpg",val_data_folder+"/images/"+"1stVideo0.jpg")
    try:
        shutil.move(train_data_folder+"/images/"+images[(i*test_spacing)-2],test_data_folder+"/images/"+images[(i*test_spacing)-2])
        print("Already move",images[(i*test_spacing)-1],"to test set")
        shutil.move(train_data_folder+"/labels/"+labels[(i*test_spacing)-2],test_data_folder+"/labels/"+labels[(i*test_spacing)-2])
        print("Already move",labels[(i*test_spacing)-1],"to test set")
    except:
        print("Wrong when moving",images[(i*test_spacing)-1],"to test set!!!!!!")
# 1stVideo0.jpg

 
