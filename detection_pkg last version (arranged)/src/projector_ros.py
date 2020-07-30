#!/usr/bin/env python

import matplotlib.pyplot as plt
import psutil
import matplotlib
import os
import sys
import rospy
import numpy as np
from PIL import Image

# --- Allow relative importing
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        print("relative importing")

from std_msgs.msg import String

### GLobal Varible ###
last_fig = "nothing"

class ProjectFig:
    def __init__(self):
        self.symbol_sub = rospy.Subscriber("/what_to_project", String, self.callback)
        print("Subscribed to topic /what_to_project")
        self._mydata = "stam string"

    def callback(self, msg):
        global last_fig
        width=1230 # The width of the projected image, changeable.
        height=700 # The height of the projected image, changeable.
		# x= 2200 # the x coordinate on the screen to the open the image.
		# y= 100 # the x coordinate on the screen to the open the image.
        self._mydata = msg.data #data= nothing, arrow, circle, trophy.

        if self._mydata=='circle':
            if last_fig != 'circle':
                last_fig='circle'
                print ('in circle')
                image=Image.open('/home/dji/camera_ws/src/detection_pkg/src/stop_sign.png')
                image=image.resize((width,height))
                #f.canvas.manager.window.move(x, y) # To move the open image on the screen, if want to do 1 screen for code, and second to be projected.
                image.show()
        elif self._mydata=='arrow_forward':
            if last_fig != 'arrow_forward':
                last_fig='arrow_forward'
                image=Image.open('/home/dji/camera_ws/src/detection_pkg/src/arrow_forward.png')
                image=image.resize((width,height))
                #f.canvas.manager.window.move(x, y) # To move the open image on the screen, if want to do 1 screen for code, and second to be projected.
                image.show()
        elif self._mydata=='arrow_right':
            if last_fig != 'arrow_right':
                last_fig='arrow_right'
                image=Image.open('/home/dji/camera_ws/src/detection_pkg/src/arrow_right.png')
                image=image.resize((width,height))
                #f.canvas.manager.window.move(x, y) # To move the open image on the screen, if want to do 1 screen for code, and second to be projected.
                image.show()
        elif self._mydata=='arrow_back':
            if last_fig != 'arrow_back':
                last_fig='arrow_back'
                image=Image.open('/home/dji/camera_ws/src/detection_pkg/src/arrow_back.png')
                image=image.resize((width,height))
                #f.canvas.manager.window.move(x, y) # To move the open image on the screen, if want to do 1 screen for code, and second to be projected.
                image.show()
        elif self._mydata=='arrow_left':
            if last_fig != 'arrow_left':
                last_fig='arrow_left'
                image=Image.open('/home/dji/camera_ws/src/detection_pkg/src/arrow_left.png')
                image=image.resize((width,height))
                #f.canvas.manager.window.move(x, y) # To move the open image on the screen, if want to do 1 screen for code, and second to be projected.
                image.show()

        elif self._mydata=='trophy':
            if last_fig != 'trophy':
                last_fig='trophy'
                print ('in the projector file -> in trophy')
                image=Image.open('/home/dji/camera_ws/src/detection_pkg/src/trophy.png')
                image=image.resize((width,height))
                #f.canvas.manager.window.move(x, y) # To move the open image on the screen, if want to do 1 screen for code, and second to be projected.
                image.show()
        elif self._mydata=='nothing':
            a=1
        else:
            print ("not good")

def main(args):
    # initializing the ros system and make a node.
    trying = ProjectFig()
    rospy.init_node('projector_node', anonymous=True)
    rospy.spin()


if __name__ == '__main__':
    main(sys.argv)





























