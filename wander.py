#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from math import radians
from sensor_msgs.msg import Joy
import numpy as np

def scan_callback(scan):
	global g_range_ahead
	depths = []
	for dist in scan.ranges:
		if not np.isnan(dist):
			depths.append(dist)

	if len(depths) == 0:
		g_range_ahead = 0.8
	else:
		g_range_ahead = min(depths)

	#g_range_ahead = min(depths)
	#g_range_ahead = msg.ranges[len(msg.ranges)/2]
	print "range ahead: %0.2f" % g_range_ahead

def joy_cb(msg):
	if msg.buttons[0]:
		print "0 pressed"
		global move
		move = not move
	else:
		print msg

g_range_ahead = 1 # anything to start
scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)
joy_sub = rospy.Subscriber('/joy', Joy, joy_cb)
cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1) #'cmd_vel/velocityramp'
rospy.init_node('wander')
state_change_time = rospy.Time.now()
driving_forward = True
rate = rospy.Rate(10)
move = False

while not rospy.is_shutdown():
	count = 0
	if driving_forward:
		if (g_range_ahead < 0.8 or rospy.Time.now() > state_change_time):
				driving_forward = False
				state_change_time = rospy.Time.now() + rospy.Duration(1)
	else: # we're not driving_forward
		if rospy.Time.now() > state_change_time:
				driving_forward = True # we're done spinning, time to go forward!
				state_change_time = rospy.Time.now() + rospy.Duration(30)
	twist = Twist()
	if driving_forward:
		twist.linear.x = 0.6
	else:
		twist.angular.z = 0.9 #radians(45) #45deg/s in rad/s

	if move:
		cmd_vel_pub.publish(twist)

	rate.sleep()
