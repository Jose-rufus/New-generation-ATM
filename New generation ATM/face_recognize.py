import cv2
import numpy as np
import os
import smtplib
import time
import random
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# DO THE CHANGES HERE
gmail_user = "joserufus23@outlook.com"
gmail_pwd = "josephat$23"
FROM = 'joserufus23@outlook.com'
TO = ['joserufus23042003@gmail.com']  # must be a list
otp_ = random.randint(10000, 100000)
pins = 1234



# Initialize flag for OTP verification
otp_verified = False

def mail():
    global otp_verified  # Use global keyword to modify the global variable
    msg = MIMEMultipart()
    time.sleep(1)
    msg['Subject'] = "SECURITY"

    body = "This OTP for logging in :" + str(otp_)

    msg.attach(MIMEText(body, 'plain'))
    time.sleep(1)

    fp = open("1.jpg", 'rb')
    time.sleep(1)
    img = MIMEImage(fp.read())
    time.sleep(1)
    fp.close()
    time.sleep(1)
    msg.attach(img)
    time.sleep(1)

    try:
        server = smtplib.SMTP("smtp.office365.com", 587)  # or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        print('successfully sent the mail')
        otp_verified = True  # Set flag to True after sending OTP
    except Exception as e:
        print("failed to send mail:", e)


size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'
n = input("enter your name : ")
print('Training...')
# Create a list of images and a list of corresponding names
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(width, height) = (130, 100)

# Create a Numpy array from the two lists above
(images, labels) = [np.array(lis) for lis in [images, labels]]

# OpenCV trains a model from the images
# NOTE FOR OpenCV2: remove '.face'
model = cv2.face.FisherFaceRecognizer_create()
model.train(images, labels)

# Part 2: Use fisherRecognizer on camera stream
face_cascade = cv2.CascadeClassifier(haar_file)
##with open("1.txt", mode='a') as file:
webcam = cv2.VideoCapture(0)

##url="http://192.168.43.1:8080/shot.jpg"
while True:

    (_, im) = webcam.read()
    ##    imgPath=urllib.urlopen(url)
    ##    imgNp=np.array(bytearray(imgPath.read()),dtype=np.uint8)
    ##    im=cv2.imdecode(imgNp,-1)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 255, 0), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        # Try to recognize the face
        prediction = model.predict(face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if prediction[1] < 500:
            # port.write('B')
            # print (names[prediction[0]])
            cv2.putText(im, names[prediction[0]], (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
            print('The accessing person is ', str(n))

            if names[prediction[0]] == n:

                print("The detected face person is : ", names[prediction[0]])
                print('you can proceed your transaction')
                pin = int(input('enter your pin: '))
                if pin == pins:
                    print("You can continue further")
                    exit()

                else:
                    if not otp_verified:  # Check if OTP verification is done
                        mail()
                        check_otp = int(input("Enter the OTP: "))
                        if check_otp == otp_:
                            print("You can continue further")
                            exit()
                        else:
                            print("Incorrect OTP... Exiting the process")
                            exit()
                    else:
                        print("OTP has already been verified")
                        exit()

            else:
                im2 = im
                cv2.putText(im2, 'unknown ', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
                print("The detected person is unknown ")
                cv2.imwrite('1.jpg', im2)
                if not otp_verified:  # Check if OTP verification is done
                    mail()
                    check_otp = int(input("enter the OTP: "))
                    if check_otp == otp_:
                        pin = int(input('enter your pin:'))
                        if pin == pins:
                            print("You can continue further")
                            exit()
                        else:
                            print("Incorrect pin ... exiting the portal")
                            exit()
                    else:
                        print("Incorrect OTP... Exiting the process")
                        exit()

        else:
            cv2.putText(im, 'Scanning', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
    cv2.imshow('OpenCV', im)
    key = cv2.waitKey(10)
