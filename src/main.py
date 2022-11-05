import time
import cv2
import numpy as np
from src.Controller.HandTrackingModule import HandDetector
from src.Data.Operations import Operation
from src.View.UI import RenderUI
from src.Data.SketchDoc import SketchDoc


def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    success, img = cap.read()
    h, w, _ = img.shape
    bg = np.ones((405, 720, 3), np.uint8)
    bg = bg * 255
    render = RenderUI(bg, (h, w))
    sketch = SketchDoc()
    sketch.set_open(True)
    while True:

        # read a new frame
        success, img = cap.read()

        op, coord = detector.get_op_coor(img)
        render.update_sketch(sketch, coord, op)
        draw = render.update_cursor(coord)
        sketch.update_sketch(op, coord)
        # draw = render.get_output_image()

        # calculate fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        draw = cv2.flip(draw, 1)
        cv2.putText(
            draw, str(int(fps)), (18, 78), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3
        )

        cv2.imshow("image", draw)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()


if __name__ == "__main__":
    main()
