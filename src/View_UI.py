import cv2


class RenderUI:

    def __init__(self, background, res_cam):
        self.bg = background
        self.view = background
        h, w, _ = background.shape
        self.bg_width = w
        self.bg_height = h
        self.p_factor = w / res_cam[0], h / res_cam[1]

    def update_view(self, hand_coordinate: (int, int), operation):
        #coord_img = int(hand_coordinate[0] * self.p_factor[0]), int(hand_coordinate[1] * self.p_factor[1])
        img = self.view.copy()
        img = cv2.circle(img, hand_coordinate, 3, (255, 0, 255), -1)

        return img
