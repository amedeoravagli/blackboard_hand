import cv2
from Operations import Operation


class SketchDoc:
    def __init__(self, bg_color=(255, 255, 255)):
        self.bg_color = bg_color
        self.open = False

    def set_open(self, status):
        self.open = status

    def is_open(self):
        return self.open

    def update_sketch(self, operation):
        return
