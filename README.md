# feature-tracker
Tracking tool to extract multiple features in a video and store frame by frame ROIs in output files.

### Usage

```
$ python3 test.py -i <input_video> -o <output_directory>
```

### Required packages

This project requires *python 3.7+* to run. In order to use the tracker features of *opencv* library:
```
$ pip3 install opencv-contrib-python==4.4.0
```

### Functionality

Upon running, different mouse click events and keyboard press events have different functionalities:
| Keyboard Press | Functionality |
| ------ | ------ |
| SPACE | Pause and resume video |
| ENTER | Confirm selected ROI |
| DELETE | Delete selected ROI |
| ESC | Resume video |
| 'q' and 'Q' | Terminate program |

| Mouse Click | Functionality |
| ------ | ------ |
| Left Button Down | Select starting point of ROI |
| Left Button Up | Select ending point of ROI |
| Right Button Down | Select ROI for deletion |
