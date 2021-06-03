import dlib
import cv2


class DetectFace:
    def __init__(self, name):
        self.webcam = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.X = 0
        self.Y = 0
        self.width = 0
        self.height = 0
        self.frame = 0
        self.img = 0
        self.Person = name
        if not self.webcam.isOpened():
            print("Cannot open camera")
            exit()

    def open(self, time_count):
        ret, self.frame = self.webcam.read()
        self.frame = cv2.flip(self.frame, 1, dst=None)
        _, self.img = self.webcam.read()
        self.img = cv2.flip(self.img, 1, dst=None)
        face_rect = self.detector(self.img, 0)
        cv2.putText(self.frame, self.Person, (10, 200), cv2.FONT_HERSHEY_TRIPLEX,
                    1, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(self.frame, str(time_count), (100, 200), cv2.FONT_HERSHEY_TRIPLEX,
                    1, (0, 255, 255), 1, cv2.LINE_AA)
        for _, rec in enumerate(face_rect):
            y = (rec.bottom() - rec.top()) * 0.6
            x1 = rec.left() - 20
            y1 = int(rec.top() - y - 5)
            x2 = rec.right() + 22
            y2 = rec.bottom() + 5
            self.X = x1
            self.Y = y1
            self.width = x2 - x1
            self.height = y2 - y1
            # 以方框標示偵測的人臉
            cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', self.frame)

    def capture(self, img_name):
        self.img = self.img[self.Y - 20:self.Y + self.height, self.X: self.X + self.width]
        cv2.imwrite(str(img_name), self.img)

    def __del__(self):
        self.webcam = None
        cv2.destroyAllWindows()
        self.detector = None
        print("記憶體釋放")
