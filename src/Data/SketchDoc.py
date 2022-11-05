import cv2
import numpy as np
import math

from src.Data.Operations import Operation


class SketchDoc:
    def __init__(self, bg_color=(255, 255, 255), dimension=(405, 720, 3)):
        self.dim_view = None
        self.bg_color = bg_color
        self.open = False
        self.dimension = dimension
        self.doc = [[()]]
        self.num_line = 0
        # self.factor = int(self.dim_view[0] / self.dimension[0]), int(self.dim_view[1] / self.dimension[1])
        self.factor = 1, 1
        self.last_point = None
        self.last_op = None

    def set_open(self, status):
        self.open = status

    def is_open(self):
        return self.open

    def update_sketch(self, operation, pos: (int, int)):

        if pos is None:
            return
        position = self.reposition_point(pos)
        if operation == Operation.DRAW:
            self.doc[self.num_line].append(position)
            self.last_point = position
        elif operation == Operation.ERASE:
            check, p_to_erase = self.is_collided(position)
            if check:
                i = 0
                for i, points in p_to_erase:

                    for p in points:
                        j = 0
                        for pp in self.doc[i]:
                            if pp == p:
                                # divido una linea, creandone una nuova,
                                # quando cancello un punto intermedio ad una riga
                                self.num_line += 1
                                self.doc.append(self.doc[i][j:])
                                self.doc[i][j-1:].clear()

                                break
                            j += 1
                    i += 1
        else:
            # se l'ultima operazione è stata di disegno ma quella attuale
            # non lo è vuol dire che viene creata una nuova linea
            if self.last_op == Operation.DRAW:
                self.new_line()

        self.last_op = operation

    #        elif operation == Operation.PAINT:

    #        elif operation == Operation.SELECT:

    def reposition_point(self, point):
        y = point[0] * self.factor[0]
        x = point[1] * self.factor[1]
        return y, x

    def is_collided(self, position):
        points = {}
        precision = 5
        i = 0
        check = False
        for array in self.doc:
            pp_line = []
            for p in array:
                y, x = position[0] - p[0], position[1] - p[1]
                if int(math.sqrt(pow(x, 2) + pow(y, 2))) < precision:
                    check = True
                    pp_line.append(p)
            points.update(i, pp_line)
            i += 1

        return check, points

    def get_doc(self):
        return self.doc

    def new_line(self):
        self.last_point = None
        self.doc.append([])
        self.num_line += 1

    def get_last_point(self):
        return self.last_point
