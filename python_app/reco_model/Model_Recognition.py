import os
from datetime import datetime

import customtkinter
import cv2
import face_recognition
import numpy as np


class AttendanceSystem:
    def __init__(self):

        self.classNames = []
        self.encoded_face_train = []
        self.path = 'student_images'
        self.attendance_file = 'Attendance.csv'

    def load_images(self):
        mylist = os.listdir(self.path)
        for cl in mylist:
            curImg = cv2.imread(os.path.join(self.path, cl))
            self.classNames.append(os.path.splitext(cl)[0])
            curImg = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)
            encoded_face = face_recognition.face_encodings(curImg)[0]
            self.encoded_face_train.append(encoded_face)

    def mark_attendance(self, name):
        with open(self.attendance_file, 'r+') as f:
            myDataList = f.readlines()
            nameList = [line.split(',')[0] for line in myDataList]
            if name not in nameList:
                now = datetime.now()
                time = now.strftime('%I:%M:%S:%p')
                date = now.strftime('%d-%B-%Y')
                f.write(f'n{name}, {time}, {date}\n')

    def play_sound(self,success):
        # if success:
        #     playsound('success.mp3')
        # else:
        #     print('No match found.')
        pass



    def start_attendance_system(self,right_dashboard):

        progressbar = customtkinter.CTkProgressBar(master=right_dashboard)
        progressbar.configure(mode="indeterminate",width=290,height=20)
        x = (right_dashboard.winfo_width() - progressbar.winfo_width()) / 2
        y = (right_dashboard.winfo_height() - progressbar.winfo_height()) / 2
        progressbar.place(x=x, y=y)
        progressbar.start()
        self.load_images()

        cap = cv2.VideoCapture(0)
        progressbar.stop()
        progressbar.destroy()

        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            faces_in_frame = face_recognition.face_locations(imgS)
            encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
            for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
                matches = face_recognition.compare_faces(self.encoded_face_train, encode_face)
                faceDist = face_recognition.face_distance(self.encoded_face_train, encode_face)
                matchIndex = np.argmin(faceDist)
                if faceDist [matchIndex] <0.4:
                    name = self.classNames[matchIndex].upper().lower()
                    y1, x2, y2, x1 = faceloc
                    # since we scaled down by 4 times
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    self.mark_attendance(name)
                    self.play_sound(True)

            cv2.imshow('webcam', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return True


