import time
import cv2
import numpy as np
from HandTrackingModule import HandDetector
from View_UI import RenderUI
from Operations import Operation


def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    success, img = cap.read()
    h, w, _ = img.shape
    bg = np.ones_like(img, np.uint8)
    bg = bg * 255
    render = RenderUI(bg, (w, h))

    while True:
        success, img = cap.read()
        coord = detector.get_forefinger_pos(img)
        draw = render.update_view(coord, Operation.DRAW)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        draw = cv2.flip(draw, 1)
        cv2.putText(draw, str(int(fps)), (18, 78), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("image", draw)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()


if __name__ == "__main__":
    main()
