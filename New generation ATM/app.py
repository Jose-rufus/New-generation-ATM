from flask import Flask, render_template, request
import cv2, sys, numpy, os
import urllib
import numpy as np
import time
import os
from subprocess import call
import time
import os
import glob
import smtplib
import base64
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import random
app = Flask(__name__)
gmail_user = "projectcardless@outlook.com"
gmail_pwd = "santo3330"
FROM = 'projectcardless@outlook.com'
TO = ['sneka123456@outlook.com'] #must be a list
otp_=random.randint(10000,100000)
pins=1234
@app.route('/')
def home():
    return render_template('home.html')

def mail():
    
    msg = MIMEMultipart()
    time.sleep(1)
    msg['Subject'] ="SECURITY"

    #BODY with 2 argument
    
    #body=sys.argv[1]+sys.argv[2]
    #DO THE CHANGES HERE
    body="THIS IS FROM pantech solution your otp for logging in :"+str(otp_)
    
    #otp_text="your otp for logging in :"+str(otp_)
    msg.attach(MIMEText(body,'plain'))
    #msg.attach(MIMEText(otp_text,'plain'))
    time.sleep(1)


    ###IMAGE
    fp = open("1.jpg", 'rb')   		
    time.sleep(1)
    img = MIMEImage(fp.read())
    time.sleep(1)
    fp.close()
    time.sleep(1)
    msg.attach(img)
    time.sleep(1)


    try:
            server = smtplib.SMTP("smtp.office365.com", 587) #or port 465 doesn't seem to work!
            print ("smtp.gmail")
            server.ehlo()
            print ("ehlo")
            server.starttls()
            print ("starttls")
            server.login(gmail_user, gmail_pwd)
            print ("reading mail & password")
            server.sendmail(FROM, TO, msg.as_string())
            print ("from")
            server.close()
            print ('successfully sent the mail')
    except:
            print ("failed to send mail")

@app.route('/my_function', methods=['POST'])
def my_function():
    # Code to call your function here
    size = 4
    haar_file = 'haarcascade_frontalface_default.xml'
    datasets = 'datasets'
    n=input("enter your name")
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
    (images, labels) = [numpy.array(lis) for lis in [images, labels]]

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
        for (x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(255,255,0),2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            #Try to recognize the face
            prediction = model.predict(face_resize)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

            if prediction[1]<500:
                #port.write('B')
            # print (names[prediction[0]])
                cv2.putText(im,names[prediction[0]],(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                print(names[prediction[0]])  
                if names[prediction[0]]==n:
                    print(names[prediction[0]])
                    print('you can proceed your transaction')
                    pin=int(input('enter your pin:'))
                    if pin ==pins:
                        print("You can continue further")
                        exit()
                    
            
                    else:
                        mail()
                        check_otp=int(input("Enter the otp :"))
                        if check_otp==otp_:
                            print("You can continue further")
                            exit()
                        else :
                            print("Incorrect pin ... exiting the portal")
                    
                    
                else:
                    print("unknown person")
                    cv2.imwrite('1.jpg',im)
                    mail()
                    check_otp=int(input("enter the otp : "))
                    if check_otp==otp_:
                        pin=int(input('enter your pin:'))
                        if pin == pins:
                            print("You can continue further")
                            exit()
                        else:
                            
                            print("Incorrect pin ... exiting the portal")
                            exit()

        
            else:
                cv2.putText(im,'Scanning',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
        cv2.imshow('OpenCV', im)
        key = cv2.waitKey(10)
        
       

    return 'Function called successfully'

if __name__ == '__main__':
    app.run()
