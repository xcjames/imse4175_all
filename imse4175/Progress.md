## Task(6)-2024-03-25
1. Add Speed Detection Function
2. Store the counting result in a csv file, modify the font and color of the text in videos, making them clearer.
3. Retrain, and Test the Trained YOLOv5m, YOLOv8m Models.

//Status:
1. In progress.
2. In progress.
3. In progress.

## Task(5)-2024-03-02
1. Labeled 3116 new images from newly recorded long videos in TSEUNG KWAN O, and some online images.
2. Add "scooters", and "strollers" as new categories(total 8 categories now.)
3. Retrain, and Test the Trained YOLOv5s, YOLOv8s Models.

//Status:
1. Done.
2. Done.
3. Done.

## Task(4)-2024-01-12
1. Training using CCTV images on YOLOv5
2. Testing the Trained Models.

//Status:
1. Done.
2. Done.

## Task(3)-2024-01-12
1. do 80 images labeling using makesense.ai
2. Training using rgb FLIR dataset on YOLOv5

//Status:
1. Done(rgb FLIR dataset on YOLOv5)
2. Done


## Task(2)-2023-11-01
1. Need to train the model first(use FLIR dataset, model from the website, probably try to use YOLOv8?)
2. Labeling: if result not accurate, do labeling of the dataset.
3. speed should also be considered! Read some papers to tackle this! opencv(is there a function that can use speed as a feature? )
4. Overall,ultimate goal is to use thermal camera, need to compare CCTV baseline with thermal.

//Status:
1. Done(rgb FLIR dataset on YOLOv5)
2. Done.
3. Done.
4. Done.

## Task(1)-2023-10-27
1. Get some videos from higher angles.
2. Do labeling by yourself.
3. Some problems are in these results:  (1)It seldom detects "other vehicles" label, It rarely detect buses, vans, trucks...(even though they have large size in the videos) ;  (2)It seldom detects "bicycles" when a person is riding on it. Instead, it detects the whole object as "person".
4. Learn how to train the YOLO (https://github.com/chenbinluo/Learning_target_detection).
5. Understand details for three python files. Set a template for my own project.

//Status:
1. Done. 
2. Done.
3. Done.
4. Done. Downloaded FLIR dataset. https://adas-dataset-v2.flirconservator.com/#downloadguide, 
5. Done.








