import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
colorR = (255,255,0)

cx,cy,w,h = 100,100,200,200


class DragRect():
    def __init__(self,posCenter,size=[200,200]):
        self.posCenter = posCenter
        self.size = size
    def update(self, cursor):
        cx,cy = self.posCenter
        w,h = self.size
        if cx-w//2<cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:
            colorR = (255,255,0)
            self.posCenter = cursor

rect = DragRect([150,150])

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    hands, img = detector.findHands(img)

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"] #List of landmarks
        bbox1 = hand1["bbox"] # bounding box info x,y,etc
        if lmList1:
            l, _, _ = detector.findDistance(lmList1[8],lmList1[12],img)
            print(l)
            if l<60:
                colorR = (0,255,0)
                cursor = lmList1[8]
                #call update function
                rect.update(cursor)
            else:
                colorR = (255,255,0)

    cx,cy = rect.posCenter
    w,h = rect.size

    cv2.rectangle(img, (cx-w//2,cy-h//2),(cx+w//2,cy+h//2),colorR,cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)