import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import stat

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

def markAttendance(name, filename):
    file_exists = os.path.exists(filename)
    if file_exists:
        # Temporarily make the file writable
        os.chmod(filename, stat.S_IWRITE)
        
        with open(filename, 'r') as f:
            existing_entries = f.readlines()
            if any(name in entry for entry in existing_entries):
                # Revert file permissions to read-only
                os.chmod(filename, stat.S_IREAD)
                return  # Name already exists, no need to add again
                
    with open(filename, 'a') as f:
        f.write(f'{name},{datetime.now()}\n')
    
    # Change the file permissions to read-only
    os.chmod(filename, stat.S_IREAD)

def captureImages(name, num_images=15):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow to avoid webcam issues
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    if not cap.isOpened():
        print("Error: Could not open webcam. Please check if another app is using it.")
        exit()

    count = 0
    directions = [
        "Face Forward",
        "Turn Left",
        "Turn Right",
        "Look Up",
        "Look Down",
        "Tilt Left",
        "Tilt Right",
        "Slight Left",
        "Slight Right",
        "Left Profile",
        "Right Profile",
        "Up Left",
        "Up Right",
        "Down Left",
        "Down Right"
    ]

    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            break
        
        direction = directions[count] if count < len(directions) else "Face Forward"
        instruction_frame = frame.copy()
        cv2.putText(instruction_frame, f"Capture {count + 1}/{num_images}: {direction}", (15, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        
        frame_height, frame_width, _ = instruction_frame.shape
        center_x, center_y = frame_width // 2, frame_height // 2
        radius = min(frame_width, frame_height) // 3  # Increased radius to fit larger faces

        # Draw thin progress bar
        bar_height = 10
        cv2.rectangle(instruction_frame, (10, 10), (frame_width - 10, 10 + bar_height), (0, 0, 0), 2)
        cv2.rectangle(instruction_frame, (10, 10), (10 + int((frame_width - 20) * (count / num_images)), 10 + bar_height), (0, 255, 0), cv2.FILLED)

        # Draw circle
        cv2.circle(instruction_frame, (center_x, center_y), radius, (0, 255, 0), 2)

        # Detect face and check if it fits within the circle
        face_locations = face_recognition.face_locations(frame)
        fits_in_circle = False
        for (top, right, bottom, left) in face_locations:
            face_center_x, face_center_y = (left + right) // 2, (top + bottom) // 2
            face_radius = max(right - left, bottom - top) // 2
            distance_from_center = np.sqrt((face_center_x - center_x) ** 2 + (face_center_y - center_y) ** 2)
            if distance_from_center + face_radius <= radius:
                fits_in_circle = True
                break

        if fits_in_circle:
            cv2.putText(instruction_frame, "Face Fits", (15, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(instruction_frame, "Face Not Fit", (15, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.circle(instruction_frame, (center_x, center_y), radius, (0, 0, 255), 2)
        
        cv2.imshow('Webcam', instruction_frame)
        
        key = cv2.waitKey(1)
        if key == 32 and fits_in_circle:  # Press SpaceBar to capture if face fits
            count += 1
            cv2.imwrite(f'C:\\Users\\HP\\OneDrive\\Desktop\\Attendance-Face-Detection-master\\Attendance-Face-Detection-master\\Attendance-Face-Detection-master\\section_C\\database_C/{name}_{count}.jpg', frame)  # Save the original frame without instructions
            cv2.putText(instruction_frame, "Image Captured!", (15, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Webcam', instruction_frame)
            cv2.waitKey(500)  # Display captured image text for 500ms

        if key == 27:  # Press Esc to exit early
            break

    cap.release()
    cv2.destroyAllWindows()

def startWebcam():
    path = 'C:\\Users\\HP\\OneDrive\\Desktop\\Attendance-Face-Detection-master\\Attendance-Face-Detection-master\\Attendance-Face-Detection-master\\section_C\\database_C'
    imageList = []
    personName = []
    dataList = [file for file in os.listdir(path) if file.endswith(('.jpg', '.png'))]  # Only include images


    for data in dataList:
        curImage = cv2.imread(f'{path}/{data}')
        if curImage is None:
            print(f"Warning: Could not read image {data}. Skipping...")
            continue

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

        cv2.putText(frame, "Press Esc to Exit or R to Register", (15, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

        curFaceFrame = face_recognition.face_locations(frameS)
        curEncoding = face_recognition.face_encodings(frameS, curFaceFrame)

        for encoding, faceFrame in zip(curEncoding, curFaceFrame):
            if len(encodedKnown) > 0:  # Ensure there are known faces before comparing
                result = face_recognition.compare_faces(encodedKnown, encoding)
                faceDist = face_recognition.face_distance(encodedKnown, encoding)
                Index = np.argmin(faceDist)

                if faceDist[Index] < 0.55 and result[Index]:  # Ensure face matching is correct
                    name = personName[Index].upper()
                else:
                    name = "Unknown"


            y1, x2, y2, x1 = faceFrame
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            if faceDist[Index] < 0.55 and result:
                name = personName[Index].upper()
                print(name)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{name}', (x1, y1-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                
                # Generate filename based on the current date
                date_str = datetime.now().strftime("%Y-%m-%d")
                filename = f"AttendanceWebcam_{date_str}.csv"
                markAttendance(name, filename)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f'unknown', (x1, y1-5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

        cv2.imshow("Webcam", frame)
        key = cv2.waitKey(1) & 0xFF  # Ensure proper key detection
        if key == 27 or cv2.getWindowProperty("Webcam", cv2.WND_PROP_VISIBLE) < 1:  # Exit when window is closed
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
    cap.release()
    cv2.destroyAllWindows()

