import cv2

from src.Data.Operations import Operation


class Cursor:
    def __init__(self, color, size):
        self.color = color
        self.size = size

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size


class Pencil:
    def __init__(self, color, size):
        self.color = color
        self.size = size

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size


class RenderUI:
    def __init__(self, gui, res_cam):
        self.bg = gui
        self.output = gui
        h, w, _ = gui.shape
        self.bg_width = w
        self.bg_height = h
        # self.p_factor = int(h / res_cam[0]), int(w / res_cam[1])
        self.pencil = Pencil((0, 0, 0), 3)
        self.cursor = Cursor((0, 0, 0), 3)

    def update_cursor(self, hand_coordinate: (int, int)):
        img = self.output.copy()
        # hand_pos = hand_coordinate[0] * self.p_factor[0], hand_coordinate[1] * self.p_factor[1]
        if hand_coordinate is not None:
            cv2.circle(
                img,
                hand_coordinate,
                self.cursor.get_size(),
                self.cursor.get_color(),
                -1,
            )

        return img

    def update_sketch(self, sketch, new_point, operation=None):

        if new_point is None:
            return

        if operation == Operation.DRAW:
            if sketch.is_open():
                old_point = sketch.get_last_point()
                if old_point is not None:
                    self.output = cv2.line(
                        self.output,
                        old_point,
                        new_point,
                        self.pencil.get_color(),
                        self.pencil.get_size(),
                    )
        if operation == Operation.ERASE:
            return
            for line in sketch.get_doc():
                o_p = None
                for n_p in line:
                    if o_p is not None:
                        self.output = cv2.line(
                            self.bg,
                            o_p,
                            n_p,
                            self.pencil.get_color(),
                            self.pencil.get_size(),
                        )
                    o_p = n_p

    def get_output_image(self):
        return self.output
