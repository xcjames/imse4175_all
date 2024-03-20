# from __future__ import print_function
import glob
import os
import json
paths = [r"/root/autodl-tmp/FLIR/images_thermal_train",r"/root/autodl-tmp/FLIR/images_thermal_val",r"/root/autodl-tmp/FLIR/video_thermal_test",
r"/root/autodl-tmp/FLIR/images_rgb_train", r"/root/autodl-tmp/FLIR/images_rgb_val",r"/root/autodl-tmp/FLIR/video_rgb_test"]
output_paths = [r"/root/autodl-tmp/FLIR/images_thermal_train/labels", r"/root/autodl-tmp/FLIR/images_thermal_val/labels", r"/root/autodl-tmp/FLIR/video_thermal_test/labels",
r"/root/autodl-tmp/FLIR/images_rgb_train/labels", r"/root/autodl-tmp/FLIR/images_rgb_val/labels", r"/root/autodl-tmp/FLIR/video_rgb_test/labels"]


# paths = [r"/root/autodl-tmp/FLIR/images_thermal_train"] #r"/root/autodl-tmp/FLIR/images_thermal_train", 
# output_paths = [r"/root/autodl-tmp/FLIR/images_thermal_train/labels"] #r"/root/autodl-tmp/FLIR/images_thermal_train/labels", 

for (path, output_path) in zip(paths, output_paths):
    json_files = sorted(glob.glob(os.path.join(path, '*.json'))) # get all the json files in the folder.
    for json_file in json_files:
        with open(json_file) as f:
            data = json.load(f)  # make json to dict
            try:
                images = data['images']
                annotations = data['annotations']
            except:
                print("Completed changing json to YOLO txt")
                continue

            # Original FLIR categories
            '''
            Category Id 1:  person
            Category Id 2:  bike (renamed from "bicycle")
            Category Id 3:  car (this includes pick-up trucks and vans)
            Category Id 4:  motor (renamed from "motorcycle" for brevity)
            Category Id 6:  bus
            Category Id 7:  train
            Category Id 8:  truck (semi/freight truck, excluding pickup truck)
            Category Id 10: light (renamed from "traffic light" for brevity)
            Category Id 11: hydrant (renamed "fire hydrant" for brevity)
            Category Id 12: sign (renamed from "street sign" for brevity)
            Category Id 17: dog
            Category Id 37: skateboard
            Category Id 73: stroller (four-wheeled carriage for a child, also called pram)
            Category Id 77: scooter
            Category Id 79: other vehicle (less common vehicles like construction equipment and trailers)
            '''
            # project categories
            categories = ["person","car","dog","bicycle","e-bike","other vehicles", "stroller", "scooter"]
            # mapping Original FLIR categories to project categories
            rgb_flir_categories_2_six_categories={
                1:0,
                2:3,
                3:1,
                4:4,
                6:5,
                7:5,
                8:5,
                17:2,
                73:6,
                77:7,
                79:5
            }
            for i in range(0, len(images)):
                converted_results = []
                for ann in annotations:
                    if ann['image_id'] == images[i]["id"] and (ann['category_id'] in rgb_flir_categories_2_six_categories.keys()):  # if the category is among the 6 categories
                        cat_id = int(rgb_flir_categories_2_six_categories[int(ann['category_id'])])

                        # left, top are x, y of the bounding box upper-left corner coordinate.
                        # bbox_width, bbox_height are the width, height of bounding box
                        left, top, bbox_width, bbox_height = map(float, ann['bbox'])  

                        # coordinate of the center point
                        x_center, y_center = (left + (bbox_width / 2), top + (bbox_height / 2))

                        # normalization to range of 0-1
                        x_rel, y_rel = ((x_center /images[i]["width"]) , (y_center / images[i]["height"]))
                        w_rel, h_rel = ((bbox_width / images[i]["width"]), (bbox_height / images[i]["height"]))
                        converted_results.append((cat_id, x_rel, y_rel, w_rel, h_rel))

                image_name = images[i]['file_name']
                # image_name is in the format of data/xxxxxxxxxxxxxxxxxxxx.jpg, need to remove the "data/" and ".jpg"
                image_name = image_name[5:-4]

                print(image_name)  
                file = open(output_path + '/' + str(image_name) + '.txt', 'w+')
                file.write('\n'.join('%d %.6f %.6f %.6f %.6f' % res for res in converted_results))
                file.close()