"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from .gaze_tracking import GazeTracking


class EyesModel:
    def __init__(self, location1, location2):
        self.gaze1P = GazeTracking()
        self.gaze2P = GazeTracking()
        self.webcam = cv2.VideoCapture(0)
        self.Location1P = location1
        self.Location2P = location2

    def open(self):
        _, frame = self.webcam.read()
        frame = cv2.flip(frame, 1, dst=None)
        text1P = "NONE"
        text2P = "NONE"
        self.gaze1P.refresh(frame[:, :360, :])
        frame[:, :360, :] = self.gaze1P.annotated_frame()
        if self.gaze1P.is_blinking():
            text1P = "Blinking"
        elif self.gaze1P.is_right():
            text1P = "Looking"
        elif self.gaze1P.is_left():
            text1P = "Looking"
        elif self.gaze1P.is_center():
            text1P = "Looking"
        cv2.putText(frame, text1P, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 2)
        cv2.putText(frame, text1P, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 2)
        left_pupil_1P = self.gaze1P.pupil_left_coords()
        right_pupil_1P = self.gaze1P.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil_1P), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31),
                    1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil_1P), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                    (147, 58, 31), 1)

        self.gaze2P.refresh(frame[:, 280:, :])
        frame[:, 280:, :] = self.gaze2P.annotated_frame()
        if self.gaze2P.is_blinking():
            text2P = "Blinking"
        elif self.gaze2P.is_right():
            text2P = "Looking"
        elif self.gaze2P.is_left():
            text2P = "Looking"
        elif self.gaze2P.is_center():
            text2P = "Looking"
        cv2.putText(frame, text2P, (330, 60), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 2)
        cv2.putText(frame, text2P, (330, 60), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 2)
        left_pupil_2P = self.gaze2P.pupil_left_coords()
        right_pupil_2P = self.gaze2P.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil_2P), (330, 130), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                    (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil_2P), (330, 165), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                    (147, 58, 31), 1)
        cv2.namedWindow("1P Eyes", 0)
        cv2.namedWindow("2P Eyes", 0)
        cv2.moveWindow("1P Eyes", self.Location1P[0], self.Location1P[1])
        cv2.moveWindow("2P Eyes", self.Location2P[0], self.Location2P[1])
        cv2.imshow("1P Eyes", frame[:, :320])
        cv2.imshow("2P Eyes", frame[:, 320:])
        return text1P, text2P
