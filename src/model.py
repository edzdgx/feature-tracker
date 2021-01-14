import cv2


class Model:

    def __init__(self, _winname):
        self.winname = _winname
        self.curr_frame = None
        self.img = None
        self.rects = []
        self.colors = {}
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

    def calc_rect(self, _x, _y, _w, _h):
        # print(f'calculatig points')
        if _w > 0:
            self.x1 = _x
            self.x2 = _x + _w
        else:
            self.x1 = _x + _w
            self.x2 = _x
        if _h > 0:
            self.y1 = _y
            self.y2 = _y + _h
        else:
            self.y1 = _y + _h
            self.y2 = _y
        return [(self.x1, self.y1), (self.x2, self.y2)]

    def delete_rect(self, pt):
        rect = self.is_in_box(pt)
        if rect:
            self.colors.pop(repr(rect))
            self.rects.remove(rect)
        else:
            print(f'No boxes detected @ point {pt}')

    def is_in_box(self, pt):
        for rect in self.rects:
            if pt[0] in range(rect[0][0], rect[1][0]) and pt[1] in range(rect[0][1], rect[1][1]):
                return rect
        return False

    def update_img(self):
        self.img = self.curr_frame.copy()
        for rect in self.rects:
            cv2.rectangle(self.img, rect[0], rect[1], self.colors[repr(rect)], 2, 1)
