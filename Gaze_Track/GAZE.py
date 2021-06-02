from GazeTracking.Gaze_Track.gaze_tracking.eyes_model import EyesModel
import cv2
predict = EyesModel()
while True:
    # 這邊是讓她不會跑到當機 而做的停留
    if cv2.waitKey(1) != 27:
        # open 會 return 1P 2P 狀態
        _1P, _2P = predict.open()
        """
        "None" : 沒偵測到
        "Blinking" : 眨眼
        "Looking" : 抓到眼睛
        """
        print(_1P, _2P)

