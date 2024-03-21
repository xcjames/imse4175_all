# IMSE4175 Code Implementation
This is the repository for IMSE4175 Object Detection and Tracking System on Bicycle Lanes.
     <br>Run `git clone https://github.com/xcjames/imse4175_all.git`
## 1. GPU and CUDA version
Use `nvidia-smi` to see the NVIDIA GPU you are using. Use `nvcc --version` to see the CUDA version you have, should be >=V11.1.105
## 2. Data Preparing (/imse4175)

### 2.1 CCTV datasets
Put some bike lanes videos in /imse4175/videos, and make new directories /imse4175/img_data/images, change the pwd in video2img.py to the current /imse4175/ path, and run `python video2img.py`. <br>
Then, quickly go over all images and select the images that contains some objects, which is suitable for image labelling. Then, go to [https://www.makesense.ai/](https://www.makesense.ai/), do image labelling. <br>
After getting all yolo labels, make new directories: img_data/images and img_data/labels. Put all images and labels inside these two directories directly, respectively.<br>
Then, create 3 directories: /img_data/train, /img_data/test, /img_data/val, and create empty directories /images, /labels inside each 3 of them. Move images in img_data/images, labels in img_data/labels into img_data/train/images, img_data/train/labels. <br>
Run`python split_train_val_test.py {path of the /img_data}`, then modify the path in yolov5/cctv.yaml. 

**Important: The name of directories must be "images" and "labels"**
### 2.2 FLIR RGB and FLIR Thermal datasets
Download FLIR dataset: [https://www.flir.com/oem/adas/adas-dataset-form/](https://www.flir.com/oem/adas/adas-dataset-form/) and download the [FLIR README.txt](https://adas-dataset-v2.flirconservator.com/dataset/README.txt) if more information is needed. Make a new directory /FLIR, get into it and unzip the compressed file. You will see 6 directories:  <br>
  • /images_rgb_train  
  • /images_rgb_val  
  • /images_thermal_train  
  • /images_thermal_val  
  • /video_rgb_test  
  • /video_thermal_test.  <br> 
inside each directory, create 2 sub-directories:/images, /labels. Put all images in /images, and modify the variable **paths** and **output_path** in json2yolo.py. Then, run `python json2yolo.py`, then modify the path in yolov5/flir.yaml, yolov5/flir_thermal.yaml. <br>

## 3. yolov5 model training (/yolov5)
Install requirements: `pip install -r requirements.txt `
Run `git clone https://github.com/ultralytics/yolov5.git` outside /imse4175_all. In /imse4175_all/yolov5, copy flir.yaml, flir_thermal.yaml, cctv.yaml to ./yolov5/data. <br>
Run the following command for model training:<br>
`
python train.py --data flir.yaml --weights yolov5s.pt --img 640 --epochs 150 --cfg yolov5s.yaml        
python train.py --data flir_thermal.yaml --weights yolov5s.pt --img 640 --epochs 150 --cfg yolov5s.yaml       
python train.py --data cctv.yaml --weights yolov5s.pt --img 640 --epochs 300 --cfg yolov5s.yaml    
`

## 4. yolov8 model training (/yolov8)

Run the following command for model training:<br>
`python train.py {cloned yolov5 path}/data/flir.yaml 150      
python train.py {cloned yolov5 path}/data/flir_thermal.yaml 150       
python train.py {cloned yolov5 path}/data/cctv.yaml 300`

## 5 DeepSORT Object Tracking and Counting
Find 3 YOLOv5 and 3 YOLOv8 trained models "best.pt" files, copy their path, <br>

Run the following command for object tracking & counting for some ".mp4" videos:
`
python main_yolov5.py {video path} {.pt yolo model path}<br>
python main_yolov8.py {video path} {.pt yolo model path}
`

