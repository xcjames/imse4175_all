import cv2
import numpy as np
from time import sleep

largura_min=80 #Largura minima do retangulo
altura_min=80 #Altura minima do retangulo

offset=6 #Erro permitido entre pixel  

pos_linha=550 #Posição da linha de contagem 

delay= 60 #number of frames(pictures) displayed in 1 sec

detec = []
carros= 0


def pega_centro(x, y, w, h):
    x1 = int(w / 2) 
    y1 = int(h / 2)
    #(x1,y1) becomes the mid-point of (w,h)
    cx = x + x1
    cy = y + y1
    return cx,cy

#To capture a video, you need to create a VideoCapture object
cap = cv2.VideoCapture('video.mp4')#打开文件
print(cap)

# subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()#创建的一个背景对象
subtract = cv2.createBackgroundSubtractorMOG2(500,100,detectShadows=False)#创建的一个背景对象

# subtracao = cv2.createBackgroundSubtractorMOG2(history=20000,varThreshold=300,detectShadows=False)#创建的一个背景对象
    # history：用于训练背景的帧数(当前帧受之前多少帧的影响)，默认帧数为500帧，如果不动手设置learingRate,history就被用于计算当前的learningRate, 此时history越大，learningRate越小，背景更新越慢；
    # varThreshold:方差阈值，用于判断当前像素是前景还是背景。一般默认为16，如果光照变化明显，如阳光下的水面，建议设为25，值越大灵敏度越低。灵敏度低，则背景的细微变化没那么容易被识别为前景
    # detectShadows：是否检测影子，设为true为检测，false为不检测，检测影子会增加程序时间复杂度，一般设置为false；

print(subtract)
while True:
    ret , frame1 = cap.read()#将函数进行输出，其中capture.read()函数是返回值为bool型的函数，该函数是按帧读取的，如果读取成功ret则会为1，当读到文件末尾则会变为0
    #frame1：读取到的图像帧
    tempo = float(1/delay)
    sleep(tempo) 
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY) #convert the frame1 from colored to grey.
    blur = cv2.GaussianBlur(grey,(5,5),5)
    #blurring: reduce details --> reduce noise.
        #GaussianBlur(InputArray src, OutputArray dst, Size ksize, double sigmaX, double sigmaY=0, int borderType=BORDER_DEFAULT);
        # src –输入图像；图像可以具有任何数量的信道，其独立地处理的，但深度应CV_8U，CV_16U，CV_16S，CV_32F或CV_64F。
        # dst –输出与图像大小和类型相同的图像src。
        # ksize –高斯核大小。 ksize.width 并且 ksize.height 可以有所不同，但它们都必须是正数和奇数。或者，它们可以为零，然后从计算 sigma*。
        # sigmaX – X方向上的高斯核标准偏差。
        # sigmaY – Y方向上的高斯核标准差；如果 sigmaY 为零，则将其设置为等于 sigmaX；如果两个西格玛均为零，则分别根据ksize.width 和 进行计算 ksize.height（getGaussianKernel()有关详细信息，请参见 link)；完全控制的结果，无论这一切的语义未来可能的修改，建议指定所有的ksize，sigmaX和sigmaY。
        # borderType – the method that you are going to deal with borders像素外推方法。
    #等效于：cv2.GaussianBlur(grey,blur,(3,3),5)
    img_sub = subtract.apply(blur)# 获得前景蒙版
        #前景蒙版（alpha matte）：也称前景透明度或透明度蒙版，是前背景分离的结果，是一个灰度图，
        #每一个像素点的灰度值表示原始图像每个像素属于前景物体的程度，白色代表某一个像素确定属于前景，黑色代表某一个像素确定属于背景。
    dilate = cv2.dilate(img_sub,np.ones((5,5))) #dilate膨胀处理白色部分（前景变大）（取kernel内最大的那个值）
        # erode 腐蚀处理就是前景变小（取kernel内最小的那个值）
        # img – 目标图片
        # kernel – 进行操作的内核，默认为3×3的矩阵
        # iterations – 膨胀次数，默认为1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    #cv2.getStructuringElement（a,b,c）a设定卷积核的形状、b设定卷积核的大小、c表示描点的位置，一般 c = 1，表示描点位于中心
    #①：MORPH_RECT(函数返回矩形卷积核)
    #②：MORPH_CROSS(函数返回十字形卷积核)
    #③：MORPH_ELLIPSE(函数返回椭圆形卷积核)

    dilate_close1 = cv2.morphologyEx (dilate, cv2. MORPH_CLOSE , kernel) #第一次闭运算
    dilate_close2 = cv2.morphologyEx (dilate_close1, cv2. MORPH_CLOSE , kernel) #第二次闭运算
        #opening : erode, and then dilate (reduce the noise in background, eliminate white dots inside black area)  开：先进行腐蚀运算，再进行膨胀运算。
        #closing : dilate and then erode. (reduce the noise in foreground, eliminate black dots inside white area) 闭：先进行膨胀运算，再进行腐蚀运算。
        #开运算和闭运算都是处理噪点用的：
        #开：消去一个黑图中的很多小白点

        #闭：小区一个白图中的很多小黑点

    contorno,h=cv2.findContours(dilate_close2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #thresh：图像数据（二值图像或经过Canny算法处理之后的图像）
        #cv2.RETR_TREE：轮廓检索方式，还有cv2.RETR_LIST、cv2.RETR_EXTERNAL、cv2.RETR_CCOMP
        #cv2.CHAIN_APPROX_SIMPLE：轮廓的估计方法，除此之外还有 cv2.CHAIN_APPROX_NONE
    #返回两个变量contour，h
        #contours：一个包含了图像中所有轮廓的list对象。其中每一个独立的轮廓信息以边界点坐标（x,y）的形式储存在numpy数组中。
        #hierarchy：一个包含4个值的数组：[Next, Previous, First Child, Parent]。
            # Next：与当前轮廓处于同一层级的下一条轮廓
            # Previous：与当前轮廓处于同一层级的上一条轮廓
            # First Child：当前轮廓的第一条子轮廓
            # Parent：当前轮廓的父轮廓

    cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (255,127,0), 3) #画线条
        #img：要划的线所在的图像;
        #pt1：直线起点
        #pt2：直线终点  （坐标分别为宽、高,opencv中图像的坐标原点在左上角）
        #color：直线的颜色
        #thickness=1：线条粗细,默认是1.如果一个闭合图形设置为-1，那么整个图形就会被填充。
    for(i,c) in enumerate(contorno): #contorno：一个包含了图像中所有轮廓的list对象。其中每一个独立的轮廓信息以边界点坐标（x,y）的形式储存在numpy数组中。
        #print((i,c))
        cv2.circle(frame1, c[0][0], 3, (255, 0,255), -1)
        (x,y,w,h) = cv2.boundingRect(c)#用一个最小的矩形，把找到的形状包起来，返回x，y是矩阵左上点的坐标，w，h是矩阵的宽和高
        
        
        #use the width and height larger than a certain value to determine whether it is a valid contour
        validar_contorno = (w >= largura_min) and (h >= altura_min)
        cv2.rectangle(frame1,[100,100],(100+largura_min,100+altura_min),(0,15,0),2)  #画出valid contour size
        if not validar_contorno:
            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)  #画出这个矩形      
        centro = pega_centro(x, y, w, h)#这个矩形的中心的坐标
        detec.append(centro) 
        cv2.circle(frame1, centro, 4, (0, 0,255), -1)
        #cv2.circle(image, center, radius, color, thickness)
            #image:在image上绘制圆的图像。
            #center：圆的中心坐标。坐标表示为两个值的元组，即(X坐标值，Y坐标值)。
            #radius:圆的半径。
            #color:要绘制的圆的边界线的颜色。例如：(255，0，0)为蓝色。
            #thickness:圆边界线的粗细像素。厚度-1像素将以指定的颜色填充矩形形状。


        for (x,y) in detec:
            if y<(pos_linha+offset) and y>(pos_linha-offset):
                carros+=1 #计vehicle数量
                # cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (255,127,0), 3) #画线条
                cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (0,127,255), 3) #换一个颜色，表明这辆车已经被计入了。 
                detec.remove((x,y))#已经detect到，去掉。
                print("car is detected : "+str(carros))   #目前已经找到车的数量。     
       
    cv2.putText(frame1, "VEHICLE COUNT : "+str(carros), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    cv2.imshow("Video Original" , frame1)
    cv2.imshow("grey_blur",blur)
    cv2.imshow("dilate",dilate)
    cv2.imshow("dilatada",dilate_close2)
    cv2.imshow("img_sub",img_sub)
    # cv2.imshow("subtracao")
    # contorno,h=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imshow("contorno",contorno[0])
    if cv2.waitKey(1) == 27: #esc键的ASCII值是27，按了esc退出程序。
        break
    
cv2.destroyAllWindows()
cap.release()
