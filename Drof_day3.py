# -*- coding: utf-8 -*-

import numpy as np
import rospy
import cv2
from clover import srv
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_srvs.srv import Trigger
from pyzbar import pyzbar

rospy.init_node('drof')
bridge = CvBridge()
image_pub = rospy.Publisher('~Detect', Image, queue_size=10)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)

Detect = rospy.Publisher("/Detect", Image)
# Обработка QR
def qr_check(data):
    global cap, answer
    frame = bridge.imgmsg_to_cv2(data, 'bgr8')
    barcodes = qr_read(frame)  # read the barcode using zbar
    if barcodes:
        print(barcodes[0].data)
        answer = barcodes[0].data
        # draw rect and publish to topic
        (x, y, w, h) = barcodes[0].rect
        reccv.tangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        Detect.publish(bridge.cv2_to_imgmsg(frame, 'bgr8'))
        cap = True
        image_sub.unregister()


answer = ''
# Взлет
navigate(x=0, y=0, z=0.6, speed=0.2, frame_id='body', auto_arm=True)
rospy.sleep(10.)
cap = True
# Полет к QR
navigate(x=0.4, y=0.8, z=0.6, speed=0.2, frame_id='aruco_map', auto_arm=True)
rospy.sleep(15)

image_sub = rospy.Subscriber('main_camera/image_raw', Image, qr_check, queue_size=1)  # get capture
while not cap:  # wait the capture
    rospy.sleep(0.5)

# Полет к началу координат
navigate(x=0, y=0, z=0.6, speed=0.2, frame_id='aruco_map', auto_arm=True)
rospy.sleep(15)

land()
