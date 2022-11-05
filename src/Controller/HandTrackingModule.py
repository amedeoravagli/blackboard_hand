import math

import cv2
import mediapipe as mp

from src.Data.Operations import Operation


class HandDetector:
    def __init__(self, max_num_hands=2, detection_conf=0.5, track_conf=0.5):
        self.lm_list = None
        self.results = None

        self.max_hands = max_num_hands
        self.detection_con = detection_conf
        self.track_con = track_conf

        self.mp_hands = mp.solutions.hands
        static_mode_image = False
        self.hands = self.mp_hands.Hands(
            static_mode_image, self.max_hands, 1, detection_conf, track_conf
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hand_position(self, img, hand_num=0):

        x_list = []
        y_list = []
        bbox = []
        self.lm_list = []

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_num]
            h, w, c = img.shape
            for id, lm in enumerate(my_hand.landmark):

                cx, cy = int(lm.x * w), int(lm.y * h)
                x_list.append(cx)
                y_list.append(cy)

                self.lm_list.append([id, cx, cy])

            xmin, xmax = min(x_list), max(x_list)
            ymin, ymax = min(y_list), max(y_list)
            bbox = xmin, ymin, xmax, ymax

        return self.lm_list, bbox

    def fingers_up(self):
        fingers = []
        if self.lm_list:
            # Thumb
            if self.lm_list[self.tip_ids[0]][1] > self.lm_list[self.tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Fingers
            for id in range(1, 5):

                if (
                    self.lm_list[self.tip_ids[id]][2]
                    < self.lm_list[self.tip_ids[id] - 2][2]
                ):
                    fingers.append(1)
                else:
                    fingers.append(0)

        return fingers

    def get_op_coor(self, img):
        op = None
        pos = None
        self.find_hand_position(img)

        fingers = self.fingers_up()
        if fingers:
            if (
                fingers[0] == 0
                and fingers[1] == 1
                and fingers[2] == 0
                and fingers[3] == 0
                and fingers[4] == 0
            ):
                pos = self.lm_list[self.tip_ids[1]][1], self.lm_list[self.tip_ids[1]][2]
            elif (
                fingers[0] == 0
                and fingers[1] == 1
                and fingers[2] == 1
                and fingers[3] == 0
                and fingers[4] == 0
            ):
                pos = self.lm_list[self.tip_ids[1]][1], self.lm_list[self.tip_ids[1]][2]
                distance, _ = self.find_distance(fingers[1], fingers[2])
                if distance < 3:
                    op = Operation.DRAW
            elif (
                fingers[0] == 1
                and fingers[1] == 1
                and fingers[2] == 1
                and fingers[3] == 1
                and fingers[4] == 1
            ):
                pos = self.lm_list[self.tip_ids[1]][1], self.lm_list[self.tip_ids[1]][2]
                #op = Operation.ERASE

        return op, pos

    def find_distance(self, p1, p2, img=None, draw=False, r=15, t=3):
        x1, y1 = self.lm_list[p1][1:]
        x2, y2 = self.lm_list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, [x1, y1, x2, y2, cx, cy]
