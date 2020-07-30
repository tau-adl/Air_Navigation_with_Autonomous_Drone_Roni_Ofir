#!/usr/bin/env python

# _mystring can get: initialize = For the first arrow, without detection or close and publishing arrow/nothing.
#                    moving = without detection, need to publish arrow/nothing.
#                    waiting = with detection, need to publish circle or nothing.
#                    end = without detection, publish trophy and exit program.

# identified_msg_to_publish can get: nothing = Static state.
#                    		     circle = detection start.
#                    		     arrow = detection end.
#                    		     trophy = final destination.


# --- Allow relative importing
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    print("relative importing")

import sys
import rospy
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import psutil

from std_msgs.msg import String
from sensor_msgs.msg import Image

from cv_bridge import CvBridge, CvBridgeError

### Parameters ###
Num_of_detection_iter = 20 # Must be 'Num_of_detection_iter' detected image in a row to be decided as detected, changeable.
check_only_image = 13 # Check only the 'check_only_image' taken image, changeable.
PROC_NAME = "display"

### GLobal Varible ###
frame_counter = 0
prev_state = 0  # 0=initialize, 1=moving, 2=waiting, 3=end.
detect_counter = 0  # The number of time detect in sequence.
last_arrow='0' # forward, right, back, left.

class Detector:
    def __init__(self):
        self.identified_msg_to_publish = String()
        self.string_pub = rospy.Publisher("/what_to_project", String, queue_size=10)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/color/image_raw", Image, self.callback_image)
        print("Subscribed to topic /raspicam_node/image")
        self.in_point_sub = rospy.Subscriber("/in_point", String, self.callback_string)
        print("Subscribed to topic /in_point")
        self._mydata = Image()
        self._mystring = "stam string"

    def callback_image(self, data):
        self._mydata = data
        self.run()

    def callback_string(self, msg):
        self._mystring = msg.data
        self.run()

    def run(self):
        global frame_counter
        global prev_state
        global Num_of_detection_iter
        global PROC_NAME
        global detect_counter
        global last_arrow
        global check_only_image

        try:
            frame = self.bridge.imgmsg_to_cv2(self._mydata, "bgr8")
            self._myframe = frame

        except CvBridgeError as e:
            print(e)

        ##### Here we implement out detection alogrythm ####
        self.identified_msg_to_publish = 'nothing' # For security.
        if self._mystring == "waiting":
            if prev_state == 1:
                prev_state = 2
                #closing the last figure
                for proc in psutil.process_iter():
                        # check whether the process to kill name matches
                        if proc.name() == PROC_NAME:
                            print("Close Image - close the arrow img")
                            proc.terminate()
                            proc.kill()

                print ("publishing circle now")
                self.identified_msg_to_publish = "circle"
                detect_counter = 0  # The number of time detec.

            elif prev_state==2:
                currect_pixel_sum = 0
                # The number of pixels to be the threshold between detect and not detect.
                percent_square = 1 #  changeable.
                total_pixels_square = 1700000 # changeable.

                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower_red = np.array([103, 120, 154]) # The lower color value threshold of the filter, changeable.
                upper_red = np.array([179, 255, 255]) # The upper color value threshold of the filter, changeable.
                mask = cv2.inRange(hsv, lower_red, upper_red)
                result=cv2.medianBlur(mask,9) # median filter, the second parameter is changeable but can only be odd.

                if frame_counter >= check_only_image: # Check only the check_only_image frame.
                    frame_counter = 0
                    currect_pixel_sum = result.sum()
                    print("", currect_pixel_sum)
                    if currect_pixel_sum <= percent_square * total_pixels_square: # Check if there are enough pixels covers.
                        detect_counter = detect_counter + 1
                        if detect_counter >= Num_of_detection_iter: # The demand for some detected frame in a row.
                            # closing the last figure
                            for proc in psutil.process_iter():
                                    # check whether the process to kill name matches
                                if proc.name() == PROC_NAME:
                                        print("Close Image")
                                        proc.terminate()
                                        proc.kill()

                            if last_arrow== "arrow_forward":
                                self.identified_msg_to_publish = "arrow_right"
                                last_arrow = "arrow_right"
                            elif last_arrow== "arrow_right":
                                self.identified_msg_to_publish = "arrow_back"
                                last_arrow = "arrow_back"
                            elif last_arrow== "arrow_back":
                                self.identified_msg_to_publish = "arrow_left"
                                last_arrow = "arrow_left"
                            prev_state = -1
                        else:
                            self.identified_msg_to_publish = "nothing"
                    else:
                        detect_counter = 0
                        self.identified_msg_to_publish = "nothing"

                else:
                    frame_counter = frame_counter + 1
                    self.identified_msg_to_publish = "nothing"

        else:
            self.identified_msg_to_publish = "nothing"
        elif (self._mystring == "moving_forward") or (self._mystring =="moving_right") or (self._mystring == "moving_back") or (self._mystring =="moving_left") or (self._mystring =="moving")):
        	self.identified_msg_to_publish = "nothing"
            prev_state = 1
		elif self._mystring == 'initialize':
			print ("in initialize")
			if prev_state == 0:
				print ('arrow_forward')
				self.identified_msg_to_publish = "arrow_forward"
				last_arrow = "arrow_forward"
				prev_state = 1
			else:  # He is moving.
				self.identified_msg_to_publish = "nothing"
		elif self._mystring == 'end':  # end
			print ('in end')
			if prev_state == 1:
				# closing the last figure
				for proc in psutil.process_iter():
						# check whether the process to kill name matches
						if proc.name() == PROC_NAME:
							print("Close Image")
							proc.terminate()
							proc.kill()

				self.identified_msg_to_publish = "trophy"
				prev_state = 3
			else:
				self.identified_msg_to_publish = "nothing"
        else:
            print ('not good')
            self.identified_msg_to_publish = "nothing"

        self.string_pub.publish(self.identified_msg_to_publish)

def main(args):
    # initializing the ros system and make a node.
    rospy.init_node('obj_detector_node', anonymous=True)
    trying = Detector()
    print ('before sleep 5')
    time.sleep(5)
    rospy.spin()

if __name__ == '__main__':
    main(sys.argv)
