import cv2


class View:
    def __init__(self, _winname):
        self.winname = _winname
        self.drawing = False
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

    def show(self, model):
        model.img = model.curr_frame.copy()
        cv2.imshow(self.winname, model.img)

    def freeze_frame(self, controller, model):
        # reset model.rects
        model.rects = []
        self.x = self.y = self.w = self.h = 0
        cv2.setMouseCallback(self.winname, controller.click_event)

        while True:
            rect = model.calc_rect(self.x, self.y, self.w, self.h)
            model.update_img()

            if rect not in model.rects:
                cv2.rectangle(model.img, rect[0], rect[1], (0, 0, 255), 2, 1)
            cv2.imshow(self.winname, model.img)

            key = cv2.waitKey(1)
            if key == 32 or key == 27 or key == ord('q'):
                return
            elif key == 13 and rect[1][0] - rect[0][0] != 0 and rect[1][1] - rect[0][1] != 0:
                model.rects.append(rect)
                model.colors[repr(rect)] = (0, 255, 0)
                print(f'rect {rect} appended to model\nmodel.rects = {model.rects}\n')
            elif key == 8:
                model.delete_rect(controller.selected)
