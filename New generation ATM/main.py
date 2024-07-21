from flask import Flask, render_template, request
import os
import cv2
import face_recognition
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
otp = random.randint(100000, 999999)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/my_function', methods=['POST'])
def my_function():
    if request.method == 'POST':
        # Capture video stream from default camera
        video_capture = cv2.VideoCapture(0)

        # Load dataset
        dataset_path = r"C:\Users\DELL\Desktop\atm code\datasets"
        images = []
        names = []

        for name in os.listdir(dataset_path):
            person_folder_path = os.path.join(dataset_path, name)
            for image_name in os.listdir(person_folder_path):
                image_path = os.path.join(person_folder_path, image_name)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)[0]
                images.append(encoding)
                names.append(name)
        print("works fine")
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(images, face_encoding)
                    name = "Unknown"

                    # If a match was found in the dataset, use the first one
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = names[first_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
                        # Display the resulting image
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

        # If a name is recognized, ask for the PIN
        if name != 'Unknown':
            return render_template('pin.html', name=name)

        # If a name is not recognized, send OTP to email
        else:
            # Generate a 6-digit OTP
            

            # Send OTP to user's email
            email = request.form['email']
            send_otp(email, otp)

            return render_template('otp.html', email=email)

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    # Verify the OTP entered by the user
    entered_otp = request.form['otp']
    email = request.form['email']

    if int(entered_otp) == otp:
        return render_template('success.html', name=name)
    else:
        return render_template('failure.html')
    exit()

def send_otp(email, otp):
    # Code to send the OTP to the user's email
    # This code will depend on the email service being used
    pass

