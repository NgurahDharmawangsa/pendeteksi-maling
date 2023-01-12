import cv2
from cvzone.PoseModule import PoseDetector
import pyglet.media
import os
import requests
# get current DateTime
from datetime import datetime

static_back = None

cap = cv2.VideoCapture(0) #webcam
cap.set(3, 800)
cap.set(4, 600)

detector = PoseDetector()
sound = pyglet.media.load("alarm.wav", streaming=False)
people = False
img_count, breakcount = 0, 0

#path = 'C://Users/Muhammad Febri/Desktop/Py/img/'
path = 'C://Users/User/Documents/1)Kuliah/SMT 5/Pengolahan Citra Digital/Pendeteksi Maling/img/'
#C://Users/User/Documents/1)Kuliah/SMT 5/Pengolahan Citra Digital/Pendeteksi Maling/img
url   = 'https://api.telegram.org/bot'
token = "5895007785:AAEF8LPAPgen4CVZPu4pFniGX2Kik6188KQ" #replace token bot
#chat_id = "817848608"
chat_id = "523566224"
caption = "Ada Maling Terdeteksi !!"

while True:
    success, img = cap.read()
    img = detector.findPose(img, draw=False)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)

    img_name = f'image_{img_count}.png'

    # Converting color image to gray_scale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # In first iteration we assign the value 
    # of static_back to our first frame
    if static_back is None:
        static_back = gray
        continue
  
    # Difference between static background 
    # and current frame(which is GaussianBlur)
    diff_frame = cv2.absdiff(static_back, gray)

    # If change in between static background and
    # current frame is greater than 30 it will show white color(255)
    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    font = cv2.FONT_HERSHEY_PLAIN
    # Put current DateTime on each frame
    #cv2.putText(img,str(datetime.now()),(140,250), font, .5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(img, str(datetime.now()), (20, 440),
                font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    if bboxInfo:
        #-------------------------FULL SCREEN----------------------------
        #  cv2.rectangle(img, (700, 20), (1220, 80), (0, 0, 255), cv2.FILLED)
        # cv2.putText(img, "PEOPLE DETECTED!!!", (500, 70),
        #            cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
        # -------------------------DEFAULT SCREEN--------------------------
        cv2.rectangle(img, (120, 20), (470, 80), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, "ADA ORANG ASING !!", (130, 60),
                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        breakcount += 1


        if breakcount >= 30:
            if people == False:
                img_count += 1
                sound.play()
                cv2.imwrite(os.path.join(path, img_name), img)
                files = {'photo': open(path + img_name, 'rb')}
                resp = requests.post(url + token + '/sendPhoto?chat_id=' + chat_id + '&caption=' + caption + '', files=files)
                print(resp.status_code)
                people = not people
    else:
        breakcount = 0
        if people:
            people = not people

    cv2.imshow("Image", img)
    cv2.imshow("Threshold Frame", thresh_frame)
    #cv2.imshow("Difference Frame", diff_frame)

    if cv2.waitKey(30) & 0xff == ord('q'):
        break
    #cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()