from model import Model
from view import View
from controller import Controller
import argparse
import utils
import cv2
import os


winname = 'main'
trackers = []
tracking = []
files = []


def main():
    # parse args
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', type=str, required=True, help='path to input video file')
    ap.add_argument('-o', '--output', type=str, default='./', help='path to output directory')
    args = vars(ap.parse_args())
    in_vid = args['input']
    out_dir = args['output']
    video_name = in_vid.split('/')[-1].split('.')[0]

    # initialization
    model = Model(winname)
    view = View(winname)
    controller = Controller(winname, view, model)
    cap = utils.load_video(in_vid)
    frame_id = 0

    cv2.namedWindow(winname)

    # initial frame for selecting roi
    success, orig = cap.read()
    if not success:
        return

    # create dir to store output roi
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    model.curr_frame = orig.copy()
    view.freeze_frame(controller, model)
    utils.tracker_init(model, trackers, tracking, files, out_dir, video_name, frame_id)

    # play video
    while cap.isOpened():
        success, orig = cap.read()
        if not success:
            break
        model.curr_frame = orig.copy()
        frame_id += 1

        rois = utils.track(winname, trackers, model)
        view.show(model)

        # MAC: SPACE (32) ENTER (13) DELETE (8) ESC (27)
        key = cv2.waitKey(1)
        if key == 32:
            view.freeze_frame(controller, model)
            cv2.setMouseCallback(winname, controller.empty_click_event)
            utils.tracker_init(model, trackers, tracking, files, out_dir, video_name, frame_id)
        elif key == ord('q'):
            break

        # write rois to txt file
        utils.write_to_file(files, frame_id, rois)

    # clean up
    cv2.destroyAllWindows()
    for f in files:
        f.close()


if __name__ == '__main__':
    main()
