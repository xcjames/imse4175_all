# Tips for image labelling (YOLO models, Images on bicycle lanes)

My task is to record a video on the bike lanes, extract some images from it, and label those images. Putting the labelled images into YOLO model, I get an object detection model, but the performance was unsatisfactory ☹. I started to find out problems in the very beginning step——Image Labelling, and discover the following:
# Image Taking
  ## 1.	Avoid taking images that contains:
  1. Static objects.
  2. Overlapping objects
  3. Small and blurred objects far away.
  4. Fast moving objects
  5. Low resolution images
  ## 2.	Methods:
  1. Take high-resolution long(10-30min) videos that contains a limited range of view, which has no static objects that you want to detect(bikes/e-bikes parking, cars in traffic jam, people sitting/standing…). The background can have anything BUT the objects that you want to detect, because you would never like to label the same objects again and again over 200 images, which is also bad for model performance. Also, avoid too many overlapping objects(perhaps more than 3?) in the image, which can make your labelling process extremely difficult.
  2. Write a Python program to extract photos, remember to make the image size larger to maintain high resolution.
  3. Select the images that contain the most objects, and copy them in another folder.
# Image Labelling
  ## 1.	Makesense.ai tips:
  1. Adjust the percentage of the webpage to be smaller, which will make the line thinner, and the image larger
  2. Be careful of “very small” bounding box mistakes, clicking on the web page will easily create some small bounding points, which can be removed by writing a python program deleting all bounding box that has width or height smaller than 0.001
  3. Throw poorly labelled images away.

