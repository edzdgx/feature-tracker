# Feature tracker
This project is a tracking tool to extract manually selected features in a video, track those features frame by frame, and store tracked ROIs in output files in the form of:

| Frame_ID | x1 | y1 | x2 | y2 |
| ------ | ------ | ------ | ------ | ------ |

### Required packages

This project requires *Python 3.7+* to run. In order to use the tracker features of *OpenCV* library, 
install the following version of *OpenCV*:
```sh
$ pip3 install opencv-contrib-python==4.4.0
```

### Usage
When running the program, two options are provided:
* -i: path to input video file, required
* -o: directory to store output text file, default to current directory

```bash
$ python3 main.py -i <input_video> -o <output_directory>
```

Output text file will be named as *'videoname_x0_y0.txt'*, where (x0, y0) is the top-left coordinate of selected ROI.

For example, if the following command is executed, and two ROIs are selected with (x0, y0) at (100, 200), (400, 400):

```bash
$ python3 main.py -i video/example.mp4 -o output
```

The following directory and files will be generated:
```
.
├── video
│   ├── example.mp4
└── output
    ├── example_100_200.txt
    └── example_400_400.txt
```

### Functionality

Upon running, different mouse click events and keyboard press events have different functionalities:

| Keyboard Press | Functionality |
| ------ | ------ |
| SPACE | Play video / pause video |
| ENTER | Confirm selected ROI |
| DELETE | Delete selected ROI |
| ESC | Resume video |
| 'q' and 'Q' | Terminate program |
---
| Mouse Click | Functionality |
| ------ | ------ |
| Left Button Down | Select starting point of ROI |
| Left Button Up | Select ending point of ROI |
| Right Button Down | Select ROI for deletion |
