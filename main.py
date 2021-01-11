import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)

#IN HSV(MIN-HIGH) Format
colors = [
    [152,92,137,179,255,255], #Pink
    [23,39,186,62,255,255],  #Flourescent Yellow
    [40,22,126,86,149,255]  #Dark Green
    ]

#IN BGR Format
colors_val = [
    [102,51,204], #Pink
    [6,252,194],  #Flourescent Yellow
    [11,139,19]   #Dark Green
    ]

co_ord = []

def color_find(img, colors,colors_val):
    img_HSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    points = []
    for color in colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(img_HSV,lower,upper)
        x,y = Countours(mask)
        cv2.circle(imgRes,(x,y),15,colors_val[count],cv2.FILLED)

        if x!=0 and y!=0:
            points.append([x,y,count])
        count+=1
    return points

def Countours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            perimeter = cv2.arcLength(cnt,True)
            approximate = cv2.approxPolyDP(cnt,0.02*perimeter,True)
            x,y,w,h = cv2.boundingRect(approximate)
    return x+w//2,y

def draw(co_ord,colors_val):
    for cd in co_ord:
        cv2.circle(imgRes,(cd[0],cd[1]),10, colors_val[cd[2]],cv2.FILLED)

while True:
    success,img = cap.read()
    imgRes = img.copy()
    points = color_find(img,colors,colors_val)
    if len(points)!=0:
        for p in points:
            co_ord.append(p)
    if len(co_ord)!=0:
        draw(co_ord,colors_val)

    cv2.imshow("Result",imgRes)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break