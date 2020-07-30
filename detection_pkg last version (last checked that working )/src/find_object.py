#!/usr/bin/env python

#--- Allow relative importing
if __name__ == '__main__' and __package__ is None:
	from os import sys, path
	sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
	print("relative importing")
    
import sys
import rospy
import cv2
import time
import numpy as np

from std_msgs.msg import String
from sensor_msgs.msg import Image

from cv_bridge import CvBridge, CvBridgeError

###GLobal Varible ###
frame_counter=0

class BlobDetector:
	def __init__(self):
		print '111111111111111111111111111111'
    
		self.identified_msg_to_publish = String()
		print (">> Publishing whether detect or not detect")
      		self.string_pub  = rospy.Publisher("/is_identified",String,queue_size=10)


		self.identified_msg_to_publish="hello"
		#self.state_pub.publish(self.fly_state_to_publish)
		print "the topic just publish is hello"



        	self.bridge = CvBridge()
 #       self.image_sub = rospy.Subscriber("/raspicam_node/image",Image,self.callback)
        	self.image_sub = rospy.Subscriber("/camera/color/image_raw",Image,self.callback)
        	print ("<< Subscribed to topic /raspicam_node/image")    
        	self._mydata=Image()

    	def callback(self,data):
		global frame_counter
		print '22222222222222222222222222222222222222'
	#	print data
		self._mydata=data
        	#--- Assuming image is 640x480
        	try:
			print ("in callback func before bridge !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!&&&&&&&&&&&&*")
           		frame = self.bridge.imgmsg_to_cv2(data, "bgr8") # to check if need rgb or bgr.

			#print frame
			self._myframe=frame
			print ("in callback func after bridge !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!&&&&&&&&&&&&*")
        	except CvBridgeError as e:
    			print(e)

##### Here we implement out detection alogrythm ####
		currect_pixel_sum=0
		percent_square=0.75
		total_pixels_square=3767880;

		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		print (hsv.dtype)

		print (hsv.shape)
		print(hsv[0:4,0,0])
    		lower_blue = np.array([0, 188, 83])
    		upper_blue = np.array([9, 227, 188])
#     lower_blue = np.array([l_h, l_s, l_v])
#     upper_blue = np.array([u_h, u_s, u_v])
    		mask = cv2.inRange(hsv, lower_blue, upper_blue)
    #mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
    		result = cv2.bitwise_and(frame, frame, mask=mask)
    
    #scipy.ndimage.median_filter(mask, size=10, footprint=None, output=mask2, mode='reflect', cval=0.0, origin=0)
   # 		cv2.imshow("frame", frame)
  #  		cv2.imshow("mask", mask)
    #cv2.imshow("mask2", mask2)
    #		cv2.imshow("result", result)
    		print ("just before if frame_counter>=13:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!&&&&&&&&&&&&&&&&&&&&*")
    		if (frame_counter>=13):

        		frame_counter=0
        		currect_pixel_sum= mask.sum()
        #currect_pixel_sum= mask2.sum()
#         print("", currect_pixel_sum)
        		if (currect_pixel_sum>=percent_square*total_pixels_square):
           			self.identified_msg_to_publish="IDENTIFY"
        		else:
          	  		self.identified_msg_to_publish="NOT_IDENTIFY"
			print(self.identified_msg_to_publish)
		else:
  			frame_counter=frame_counter+1
			print(frame_counter)

		self.string_pub.publish(self.identified_msg_to_publish)

#### Finish with the detection algorythm ####

def main(args):
	print ("main !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!&&&&&&&&&&&&&&&&&&&&*")
# initializing the ros system and make a node.


    	rospy.init_node('obj_detector_node', anonymous=True)
	trying=BlobDetector()


	trying.string_pub.publish(trying.identified_msg_to_publish)

    	try:
		print ("before rospy spin !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!&&&&&&&&&&&&&&&&&&&&*")
      		rospy.spin()
		print ("after spin !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!&&&&&&&&&&&&&&&&&&&&*")
    	except KeyboardInterrupt: # can change to only esc key.
        	print("Shutting down")
    	print ("end !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!&&&&&&&&&&&&&&&&&&&&*")
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)
