import cv2
import utils
import os

# in_vid = '../vid/changxun_left_panel_0.mp4'
# in_txt = '../bbox/changxun_left_panel_0/changxun_left_panel_0_a.txt'
in_vid = '/Users/edz/Desktop/hiscene/feature-tracker/vid/changxun_ac_0.mp4'
in_txt = '/Users/edz/Desktop/hiscene/feature-tracker/changxun_ac_0/changxun_ac_0815_258.txt'
is_print = False
out_dir = 'outfile/'


def main():
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # path to input video
    cap = utils.load_video(in_vid)

    frame_id = 0

    # open file for reading ROI location
    f = open(in_txt, 'r')

    # get rid of header and get first bbox
    _ = f.readline()

    while cap.isOpened():
        # read frame and update bounding box
        _, img = cap.read()
        line = f.readline()
        if not _ or not line:
            break
        bbox = utils.get_bbox(line)
        utils.draw_box(img, bbox, (0, 0, 255))

        # cv2.imshow('frame', img[bbox[1]+1:bbox[1]+bbox[3], bbox[0]+1:bbox[0]+bbox[2]])
        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

        # update frame_id and write to file
        if is_print:
            print('{}{}.jpg'.format(out_dir, frame_id))
            cv2.imwrite('{}{}.jpg'.format(out_dir, frame_id), img[bbox[1]+1:bbox[1]+bbox[3], bbox[0]+1:bbox[0]+bbox[2]])
        frame_id += 1
        # print('{}, {:1.0f}, {:1.0f}, {:1.0f}, {:1.0f}'
        #       .format(frame_id, bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]))
    cv2.waitKey(5)
    cap.release()
    cv2.destroyAllWindows()

    f.close()


if __name__ == '__main__':
    main()
