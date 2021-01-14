import cv2


class Controller:
    def __init__(self, _winname, _view, _model):
        self.winname = _winname
        self.view = _view
        self.model = _model
        self.selected = [0, 0]

    def click_event(self, _event, _x, _y, _flags, _param):
        # print('event: {}, flag: {}'.format(_event, _flags))
        if _event == cv2.EVENT_LBUTTONDOWN:
            self.view.drawing = True
            self.view.x = _x
            self.view.y = _y
            self.view.w = 0
            self.view.h = 0
        elif _event == cv2.EVENT_MOUSEMOVE:
            if self.view.drawing:
                self.view.w = _x - self.view.x
                self.view.h = _y - self.view.y
        elif _event == cv2.EVENT_LBUTTONUP:
            self.view.drawing = False
            self.view.w = _x - self.view.x
            self.view.h = _y - self.view.y
        elif _event == cv2.EVENT_RBUTTONDOWN:
            self.selected = [0, 0]
            rect = self.model.is_in_box([_x, _y])
            if rect:
                self.selected = [_x, _y]
                print(f'right button clicked, {(_x, _y)} IS in box')
            else:
                self.selected = [0, 0]
                for key in self.model.colors:
                    self.model.colors[key] = (0, 255, 0)
                print(f'right button clicked, {(_x, _y)} NOT in box')

            self.view.x = self.view.y = self.view.w = self.view.h = -1

            # only one box can be blue
            for key in self.model.colors:
                if key == repr(rect):
                    self.model.colors[key] = (255, 0, 0)
                else:
                    self.model.colors[key] = (0, 255, 0)

    def empty_click_event(self, _event, _x, _y, _flags, _param):
        pass
