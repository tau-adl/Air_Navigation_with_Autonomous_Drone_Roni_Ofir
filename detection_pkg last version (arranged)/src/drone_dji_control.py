#!/usr/bin/env python

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
import time

from std_msgs.msg import String

### Parameters ###
last_point = 4  # The number of points in the path, changeable.

### GLobal Varible ###
is_counting = 0
initialize_state = 1
point_counter = 0
is_landing = 0
counter = 0


class DemoDrone:
    def __init__(self):

        self.fly_state_to_publish = String()
        self.state_pub = rospy.Publisher("/in_point", String, queue_size=10)
        print("Published fly state")

        self.fly_state_to_publish = "initialize"
        # self.state_pub.publish(self.fly_state_to_publish)
        print("the topic just publish is initialize")

        self.input_sub = rospy.Subscriber("/what_to_project", String, self.callback)
        print("Subscribed to topic /what_to_project")
        self._mydata = "stam string"

    def callback(self, msg):
        global last_point
        global is_counting
        global initialize_state
        global point_counter
        global is_landing
        global counter

        self._mydata = msg.data
        if is_landing == 1:
            print('Landing!!! press ctrl+c')
        elif self._mydata == 'trophy':
            print('Landing!!!')
        # Landing.
        else:
            if is_counting == 1:
                self.fly_state_to_publish = 'moving'
                counter = counter + 1
                if counter >= 10000 * 0.3:  # about 3 sec
                    is_counting = 0
                    print("point counter", point_counter)
                    if point_counter < last_point:
                        self.fly_state_to_publish = 'waiting'
                    else:
                        print('We are in the last path')
                        self.fly_state_to_publish = 'end'
            if self._mydata == "arrow_forward":
                print('moving_forward')
                is_counting = 1
                self.fly_state_to_publish = 'moving_forward'
                counter = 0
                point_counter = point_counter + 1  # =1.

            if self._mydata == "arrow_right":
                print('moving_right')
                is_counting = 1
                self.fly_state_to_publish = 'moving_right'
                counter = 0
                point_counter = point_counter + 1  # =2
            if self._mydata == "arrow_back":
                print('moving_back')
                is_counting = 1
                self.fly_state_to_publish = 'moving_back'
                counter = 0
                point_counter = point_counter + 1  # =3
            if self._mydata == "arrow_left":
                print('moving_left')
                is_counting = 1
                self.fly_state_to_publish = 'moving_left'
                counter = 0
                point_counter = point_counter + 1  # =4

            if self._mydata == "circle":
                print("circle arrived, publishing waiting")
                self.fly_state_to_publish = 'waiting'

            self.state_pub.publish(self.fly_state_to_publish)

def main(args):
    # initializing the ros system and make a node.
    rospy.init_node('drone_dji_node', anonymous=True)
    trying = DemoDrone()  # go to init
    print('before sleep 5')
    time.sleep(5)
    print("the topic just publish after 5 sec is", trying.fly_state_to_publish)
    trying.state_pub.publish(trying.fly_state_to_publish)
    try:
        rospy.spin()
    except KeyboardInterrupt:  # can change to only esc key.
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
