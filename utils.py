import cv2


# tracker
def track(winname, trackers, model):
    res = []
    for tracker in trackers:
        if tracker:
            success, bbox = tracker.update(model.curr_frame)
            if not success:
                cv2.putText(model.curr_frame, 'Object Lost', (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.imshow(winname, model.curr_frame)
                cv2.waitKey(0)
                return

            roi = bbox2roi(bbox)
            roi_new = narrow_bbox(roi, model.curr_frame)
            narrowed_bbox = roi2bbox(roi_new)
            # print(narrowed_bbox)

            # draw old and new bboxes
            draw_box(model.curr_frame, narrowed_bbox, (0, 0, 255))
            draw_box(model.curr_frame, bbox, (0, 255, 0))
            res.append(bbox2roi(narrowed_bbox))
    return res


def tracker_init(model, trackers, tracking, files, out_dir, frame_id):
    for rect in model.rects:
        if rect not in tracking:
            file_name = ''.join([out_dir, str(rect[0][0]), '_', str(rect[0][1]), '.txt'])
            f = open(file_name, 'w')
            f.write('frame_id, x1, y1, x2, y2\n')
            f.write('{}, {:1.0f}, {:1.0f}, {:1.0f}, {:1.0f}\n'
                    .format(frame_id, rect[0][0], rect[0][1], rect[1][0], rect[1][1]))
            files.append(f)

            tracking.append(rect)
            tracker = cv2.TrackerCSRT_create()
            trackers.append(tracker)
            tracker.init(model.curr_frame,
                         tuple(roi2bbox([rect[0][0], rect[0][1], rect[1][0], rect[1][1]])))


# update trackers
def write_to_file(files, frame_id, rois):
    for f, rect in zip(files, rois):
        f.write('{}, {:1.0f}, {:1.0f}, {:1.0f}, {:1.0f}\n'
                .format(frame_id, rect[0], rect[1], rect[2], rect[3]))


# draw bbox on frame
def draw_box(_img, _bbox, _color):
    x, y, w, h = int(_bbox[0]), int(_bbox[1]), int(_bbox[2]), int(_bbox[3])
    cv2.rectangle(_img, (x, y), (x + w, y + h), _color, 1, 1)
    cv2.putText(_img, 'Object Detected', (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


# load video
def load_video(_video):
    _cap = cv2.VideoCapture(_video)
    if not _cap.isOpened():
        print("Error opening video stream or file")
    return _cap


# get bbox with file
def get_bbox(_line):
    # get xi, yi, xf, yf and convert to list<int>
    _line = _line.rstrip('\n').split(', ')[1:]
    _bbox = list(map(int, _line))
    # get w, h
    _bbox[2] -= _bbox[0]
    _bbox[3] -= _bbox[1]
    return tuple(_bbox)


# convert bbox = [x, y, w, h] to ROI = [x1, y1, x2, y2]
def roi2bbox(_roi):
    return [int(_roi[0]), int(_roi[1]), int(_roi[2]) - int(_roi[0]), int(_roi[3]) - int(_roi[1])]


# convert ROI = [x1, y1, x2, y2] to bbox = [x, y, w, h]
def bbox2roi(_bbox):
    return [int(_bbox[0]), int(_bbox[1]), int(_bbox[0]) + int(_bbox[2]), int(_bbox[1]) + int(_bbox[3])]


def in_box(n, bbox):
    flag = False

    for i in range(len(bbox)):
        if i != n:
            mid_x = abs((bbox[n][0] + bbox[n][2] / 2) - (bbox[i][0] + bbox[i][2] / 2))
            mid_y = abs((bbox[n][1] + bbox[n][3] / 2) - (bbox[i][1] + bbox[i][3] / 2))
            width = bbox[n][2] + bbox[i][2]
            height = bbox[n][3] + bbox[i][3]
            if mid_x <= width / 2 and mid_y <= height / 2:
                flag = True
                return flag
        else:
            continue
    return flag


def distance_x(n, bbox):
    flag = False
    x1 = bbox[n][0]
    width1 = bbox[n][2]

    for i in range(len(bbox)):
        if i != n:
            x2 = bbox[i][0]
            width2 = bbox[i][2]
            if x2 > x1:
                distance = x2 - x1 - width1
            else:
                distance = x1 - x2 - width2
            flag = flag or (distance <= 10)
        else:
            continue
    return flag


def distance_y(n, bbox):
    flag = False
    y1 = bbox[n][1]
    height1 = bbox[n][3]

    for i in range(len(bbox)):
        if i != n:
            y2 = bbox[i][1]
            height2 = bbox[i][3]
            if y2 > y1:
                distance = y2 - y1 - height1
            else:
                distance = y1 - y2 - height2
            flag = flag or (distance <= 10)
        else:
            continue
    return flag


def filter_bbox(bbox_old, bbox, roi):
    i = 0
    while i < len(bbox_old):
        [_, _, w, h] = bbox_old[i]
        if w * h < 20:
            bbox_old.pop(i)
            continue
        i += 1
    bbox_old_num = len(bbox_old)

    if bbox_old_num == 2:
        if not distance_x(0, bbox_old):
            if bbox_old[0][2] * bbox_old[0][3] > bbox_old[1][2] * bbox_old[1][3]:
                bbox[0] += bbox_old[0][0]
                bbox[2] = bbox_old[0][2]
            else:
                bbox[0] += bbox_old[1][0]
                bbox[2] = bbox_old[1][2]

        if not distance_y(0, bbox_old):
            if bbox_old[0][2] * bbox_old[0][3] > bbox_old[1][2] * bbox_old[1][3]:
                bbox[1] += bbox_old[0][1]
                bbox[3] = bbox_old[0][3]
            else:
                bbox[1] += bbox_old[1][1]
                bbox[3] = bbox_old[1][3]

    elif bbox_old_num == 1:
        bbox[0] += bbox_old[0][0]
        bbox[2] = bbox_old[0][2]

    elif bbox_old_num >= 3:
        for i in range(bbox_old_num):
            if not distance_x(i, bbox_old):
                if not in_box(i, bbox_old):
                    edge1 = bbox_old[i][0]
                    edge2 = roi[2] - roi[0] - bbox_old[i][0] - bbox_old[i][2]
                    if edge1 < edge2:
                        bbox[0] += bbox_old[i][0] + bbox_old[i][2] + 5
                    else:
                        bbox[2] = bbox_old[i][0] - 5


# 矫正bbox函数，输入ROI是原始bbox左上角和右下角坐标，输出是新的bbox左上角和右下角坐标
# input: roi_old
# output: roi_new
def narrow_bbox(roi, frame):
    point1 = (roi[0], roi[1])
    point2 = (roi[2], roi[3])
    bbox = roi2bbox(roi)
    test = frame.copy()

    # draw old bbox
    # cv2.rectangle(frame, point1, point2, (255, 0, 0), 1, 1)
    # cv2.imshow("frame", frame)
    # cv2.waitKey(0)

    template = test[point1[1]:point2[1], point1[0]:point2[0]]
    # print(point1, point2)
    # cv2.waitKey(0)

    gray_tpl = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # _, binary = cv2.threshold(gray_tpl,200,255,cv2.THRESH_BINARY)
    _, binary = cv2.threshold(gray_tpl, 0, 255, cv2.THRESH_OTSU)  # 转换为二值图
    # cv2.imshow("gray", gray_tpl)

    # choose contour algorithm
    # contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 得到所有最外轮廓
    bbox_old = [cv2.boundingRect(cnt) for cnt in contours]  # 生成对应bbox
    # print(bbox_old)
    # cv2.waitKey(0)

    # 根据bbox个数筛选有用的bbox
    filter_bbox(bbox_old, bbox, roi)

    # 重新框定ROI
    point1 = (bbox[0], bbox[1])
    point2 = (bbox[0] + bbox[2], bbox[1] + bbox[3])
    template = test[point1[1]:point2[1], point1[0]:point2[0]]
    gray_tpl = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # _, binary = cv2.threshold(gray_tpl, 100, 255, cv2.THRESH_BINARY)
    _, binary = cv2.threshold(gray_tpl, 0, 255, cv2.THRESH_OTSU)

    # cv2.imshow("template", binary)
    # cv2.waitKey(0)
    # contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    bbox_old = [cv2.boundingRect(cnt) for cnt in contours]

    # 生成最终的bbox
    bbox_final = list(bbox_old[0])
    bbox_2draw = list(bbox_old[0])
    # cv2.rectangle(test2, (bbox_final[0], bbox_final[1]), (bbox_final[0]+bbox_final[2],bbox_final[1]+bbox_final[3]),
    #               (0, 255, 0), thickness=1)
    for bbox_in in bbox_old[1:]:
        [x, y, w, h] = bbox_in
        # cv2.rectangle(test2, (x, y),(x+w, y+h), (0, 255, 0), thickness=1)
        bbox_final[2] = max(bbox_final[2], x + w - bbox_final[0])
        bbox_final[2] = max(bbox_final[2], bbox_final[2] + bbox_final[0] - x)
        bbox_final[3] = max(bbox_final[3], y + h - bbox_final[1])
        bbox_final[3] = max(bbox_final[3], bbox_final[3] + bbox_final[1] - y)
        bbox_final[0] = min(bbox_final[0], x)
        bbox_final[1] = min(bbox_final[1], y)
        if w * h > bbox_2draw[2] * bbox_2draw[3]:
            bbox_2draw = [x, y, w, h]

    point1 = (bbox[0] + bbox_final[0], bbox[1] + bbox_final[1])
    point2 = (point1[0] + bbox_final[2], point1[1] + bbox_final[3])
    # cv2.rectangle(test, point1, point2, (0, 0, 255), 1, 1)
    roi_final = [point1[0], point1[1], point2[0], point2[1]]
    # uncomment two lines below when use test.py
    # cv2.imshow("frame", frame)
    # cv2.imshow("copy", test)

    # cv2.waitKey(20)
    return roi_final
