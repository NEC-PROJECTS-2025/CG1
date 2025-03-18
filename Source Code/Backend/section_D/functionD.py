import cv2
import webbrowser
import face_recognition
import os
from datetime import datetime

import numpy as np


def findEncoding(imageList, nameList):
    encodeList = []
    for img, name in zip(imageList, nameList):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if len(encode) > 0:
            encodeList.append(encode[0])
        else:
            encode.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            encodeList.append(encode[0])
            print(f"{name}'s image is not proper please recapture it")
    return encodeList


def markAttendance(name, path):
    with open(f'{path}', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for dataLine in myDataList:
            entry = dataLine.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            f.writelines(f'\n{name},{dt_string}')


def openExcelWebcam():
    webbrowser.open("AttendanceWebcam.csv")


def openExcelImage():
    webbrowser.open("AttendanceImage.csv")


def openExcelVideo():
    webbrowser.open("AttendanceVideo.csv")


def openReadme():
    webbrowser.open(f'{os.path.dirname(__file__)}/README.md')


def captureImages(name, num_images=15):
    cap = cv2.VideoCapture(0)
    count = 0
    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.putText(frame, f"Capturing Image {count + 1}/{num_images}", (15, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('Webcam', frame)
        
        key = cv2.waitKey(1)
        if key == 32:  # Press SpaceBar to capture
            count += 1
            cv2.imwrite(f'database_D/{name}_{count}.jpg', frame)
            cv2.putText(frame, "Image Captured!", (15, 450), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Webcam', frame)
            cv2.waitKey(500)  # Display captured image text for 500ms

        if key == 27:  # Press Esc to exit early
            break

    cap.release()
    cv2.destroyAllWindows()


def startWebcam():
    path = 'database_D'
    imageList = []
    personName = []
    dataList = os.listdir(path)

    for data in dataList:
        curImage = cv2.imread(f'{path}/{data}')
        imageList.append(curImage)
        curName = os.path.splitext(data)[0]
        personName.append(curName)

    print('Starting Encoding of Known Images in Database...')
    encodedKnown = findEncoding(imageList, personName)
    print('Encoding of Known Images Completed...')

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frameS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        frameS = cv2.cvtColor(frameS, cv2.COLOR_BGR2RGB)

        cv2.putText(frame, "Press Esc to Exit or R to Register", (15, 450), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)

        curFaceFrame = face_recognition.face_locations(frameS)
        curEncoding = face_recognition.face_encodings(frameS, curFaceFrame)

        for encoding, faceFrame in zip(curEncoding, curFaceFrame):
            result = face_recognition.compare_faces(encodedKnown, encoding)
            faceDist = face_recognition.face_distance(encodedKnown, encoding)
            Index = np.argmin(faceDist)

            y1, x2, y2, x1 = faceFrame
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            if faceDist[Index] < 0.55 and result:
                name = personName[Index].upper()
                print(name)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{name}', (x1, y1-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))

                date_str = datetime.now().strftime("%Y-%m-%d")
                filename = f"Attendance_{date_str}.csv"
                markAttendance(name, filename)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f'unknown', (x1, y1-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))

        cv2.imshow("Webcam", frame)
        key = cv2.waitKey(1)
        if key == 27:  # Press Esc to exit
            cv2.destroyWindow("Webcam")
            break
        elif key == ord('r'):  # Press 'r' to register a new person
            person_name = input("Enter the name of the person to register: ")
            captureImages(person_name)
            # Re-encode known faces after adding new person
            dataList = os.listdir(path)
            imageList = []
            personName = []
            for data in dataList:
                curImage = cv2.imread(f'{path}/{data}')
                imageList.append(curImage)
                curName = os.path.splitext(data)[0]
                personName.append(curName)
            encodedKnown = findEncoding(imageList, personName)
            print('Re-encoding Completed...')

if __name__ == "__main__":
    startWebcam()
