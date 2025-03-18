from datetime import datetime
import cv2
import numpy as np
import face_recognition
import os
from functionC import findEncoding, markAttendance

def startVideo(videoPath):
    # Updated path to the images directory
    path = 'section_C/database_C'
    
    imageList = []
    personName = []
    
    # Get a list of all files in the specified directory
    dataList = os.listdir(path)

    for data in dataList:
        curImage = cv2.imread(f'{path}/{data}')
        imageList.append(curImage)
        curName = os.path.splitext(data)[0]
        personName.append(curName)

    print('Starting Encoding of Known Images in Database...')
    encodedKnown = findEncoding(imageList, personName)
    print('Encoding of Known Images Completed...')

    cap = cv2.VideoCapture(videoPath)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame or end of video")
            break
        
        frameS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        frameS = cv2.cvtColor(frameS, cv2.COLOR_BGR2RGB)

        cv2.putText(frame, "Press Esc to Exit", (15, 450), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)

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
                filename = f"AttendanceImage_{date_str}.csv"
                markAttendance(name, filename)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f'unknown', (x1, y1-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))

        cv2.imshow("Video", frame)
        key = cv2.waitKey(1)
        if key == 27:  # Press Esc to exit
            cv2.destroyWindow("Video")
            break

    cap.release()
    cv2.destroyAllWindows()
