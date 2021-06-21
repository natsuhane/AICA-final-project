from Gaze_Model.Face_Detection.Face_Detection import DetectFace
from Gaze_Model.gaze_tracking.eyes_model import EyesModel
import cv2
import time
import keyboard
from Gaze_Model.Remove_BG_Remove.main import RemoveBackground as bg
if __name__ == '__main__':
    # Detect 1P face
    _1P_Face = DetectFace("1P")
    for count in range(50):
        if cv2.waitKey(1) == ord('q'):
            break
        _1P_Face.open(1 + count // 6)
        time.sleep(0.001)
    _1P_Face.capture("P1.png")
    _1P_Face = None

    ReMove = bg("P1.png", "P1_Remove.png")
    ReMove = None

    # Detect 2P face
    _2P_Face = DetectFace("2P")
    for count in range(50):
        if cv2.waitKey(1) == ord('q'):
            break
        _2P_Face.open(1 + count // 6)
        time.sleep(0.001)
    _2P_Face.capture("P2.png")
    _2P_Face = None

    ReMove = bg("P2.png", "P2_Remove.png")
    ReMove = None

#     # 眨眼偵測
#     # EyesModels(1P視窗位置，2P視窗位置)
    Blink = EyesModel([0, 0], [300, 0])
    while True:
        if cv2.waitKey(1) != ord('q'):
            text1P, text2P = Blink.open()
            print(text1P)
        if keyboard.is_pressed("a"):
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        if keyboard.is_pressed("q"):
            print("You pressed q")
            break
    Blink = None


########################
# class gaze:
#     # Detect 1P face
#     def p1_face():
#         _1P_Face = DetectFace("1P")
#         for count in range(50):
#             _1P_Face.open(1 + count // 6)
#             time.sleep(0.001)
#         _1P_Face.capture("Person_1.png")
#         _1P_Face = None

#         ReMove = bg("Person_1.png", "Person_1_Remove.png")
#         ReMove = None

#     # Detect 2P face
#     def p2_face():
#         _2P_Face = DetectFace("2P")
#         for count in range(50):
#             _2P_Face.open(1 + count // 6)
#             time.sleep(0.001)
#         _2P_Face.capture("Person_2.png")
#         _2P_Face = None

#         ReMove = bg("Person_2.png", "Person_2_Remove.png")
#         ReMove = None

#     # 眨眼偵測
#     # EyesModels(1P視窗位置，2P視窗位置)
#     # def blink_init():
#     #     Blink = EyesModel([0, 0], [300, 0])
#     def blink():
#             Blink = EyesModel([0, 0], [300, 0])
#             text1P, text2P = Blink.open()
#     # def blink_flush():
#     #     Blink = None
