# C-HAWK

This drone control mainly uses the libraries OpenCV and [libardrone](https://github.com/venthur/python-ardrone).
The drone will follow a chessboard. For this function the [chessboard recognition](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html) from OpenCV is used.
After the drone has detected the chessboard, it computes the middle of the board and the length of the diagonal of the board.
These informations are put into three different PD-Controller ([PID-Controller](https://en.wikipedia.org/wiki/PID_controller) with the I-constant equal to 0).
Thereby three "directions" are optimised:
* x-coordinate -> left/right-control
* y-coordinate -> height-control
* length of diagonale -> backwards/forwards-control

## To run the program:
You have to download the GitHub project [libardrone](https://github.com/venthur/python-ardrone).
Then put the files from this project into the libardrone folder.
Connect your laptop to the drone and run CentralControl.py.
For takeoff press any key. 
Now the drone should try to follow the chessboard.
For landing and shutting down the drone press space.

## Overview over the included files:
* CentralControl.py: 
* PIDController.py: a normal implementation of a PID-Controller where the constants are set via parameters
* Testprotocol.txt: some example values for speed settings which worked well
* patternRecognition.py:
* schachbrettmuster.jpg: example image
* schachmuster_5x5.jpg: example image

**_Authors:_** Christian Gebhardt and Christian Münch
