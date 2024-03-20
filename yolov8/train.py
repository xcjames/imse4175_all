#Use the command:
#python train.py /root/autodl-tmp/yolov5/data/flir.yaml 150
#python train.py /root/autodl-tmp/yolov5/data/flir_thermal.yaml 150
#python train.py /root/autodl-tmp/yolov5/data/cctv.yaml 300

from ultralytics import YOLO
import sys
# Load a model
# model = YOLO('yolov8s.yaml')  # build a new model from YAML
# model = YOLO('./yolov8s.pt')  # load a pretrained model (recommended for training)
# model = YOLO('yolov8s.yaml').load('/root/autodl-tmp/yolov8/runs/detect/train/weights/last.pt')  # build from YAML and transfer weights
model = YOLO('yolov8s.yaml').load('./yolov8s.pt') 
# model = YOLO('/root/autodl-tmp/yolov8/runs/detect/train6/weights/last.pt') #resume training

# Train the model

results = model.train(data=sys.argv[1], epochs=int(sys.argv[2]), imgsz=640)

#resume training, resume=True
# results = model.train(data=sys.argv[1], epochs=int(sys.argv[2]), imgsz=640,device=[0, 1],resume=True)