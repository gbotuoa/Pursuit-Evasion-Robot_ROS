#!/usr/bin/env python
# BEGIN ALL
# Best one
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import os
from std_msgs.msg import String, Bool
import math as m

g_vel_scales = [0.1, 0.1] # default to very slow
g_vel_ramps = [1, 1] # units: meters per second^2


def scan_callback(scan):
  #global g_range_ahead
  #g_range_ahead = min(msg.ranges)
		global closest , position ,cnt , last_closest
		depths = []
		for dist in scan.ranges:
				if not np.isnan(dist) and dist < 2.2:
						depths.append(dist)
	#scan.ranges is a tuple, and we want an array.
		fullDepthsArray = scan.ranges[:]

		if len(depths) == 0:
			closest = 0
			position = 0
		else:
			closest = min(depths)
			position = fullDepthsArray.index(closest)

	   	follow()

def follow():
		command.linear.x = m.tanh(4 * (closest - stopDistance))*max_speed
		#turn faster the further we're turned from our intended object.

		command.angular.z = ((position-320.0)/320.0)

		#if we're going slower than our min_speed, just stop.
		if abs(command.linear.x) < min_speed:
				command.linear.x = 0.0

		g_target_twist.linear.x= (command.linear.x)*1.5
		g_target_twist.angular.z= (command.angular.z)
		#print g_target_twist.linear.x, g_target_twist.angular.z
		send_twist()
		#cmd_vel_pub.publish(command)


def ramped_vel(v_prev, v_target, t_prev, t_now, ramp_rate):
		# compute maximum velocity step
		step = ramp_rate * (t_now - t_prev).to_sec()
		sign = 1.0 if (v_target > v_prev) else -1.0
		error = m.fabs(v_target - v_prev)
		if error < step: # we can get there within this timestep-we're done.
			return v_target
		else:
			return v_prev + sign * step # take a step toward the target

def ramped_twist(prev, target, t_prev, t_now, ramps):
		tw = Twist()
		tw.angular.z = ramped_vel(prev.angular.z, target.angular.z, t_prev,
		t_now, ramps[0])
		tw.linear.x = ramped_vel(prev.linear.x, target.linear.x, t_prev,
		t_now, ramps[1])
		return tw

def send_twist():
		global g_last_twist_send_time, g_target_twist, g_last_twist, g_vel_scales, g_vel_ramps, g_twist_pub
		t_now = rospy.Time.now()
		g_last_twist = ramped_twist(g_last_twist, g_target_twist, g_last_twist_send_time, t_now, g_vel_ramps)
		g_last_twist_send_time = t_now
		g_twist_pub.publish(g_last_twist)

def fetch_param(name, default):
		if rospy.has_param(name):
			return rospy.get_param(name)
		else:
			print "parameter [%s] not defined. Defaulting to %.3f" % (name, default)
			return default

if __name__== '__main__':
		rospy.init_node('wander_fol')
		global command, followDistance , stopDistance , max_speed , min_speed, move
		g_last_twist_send_time = rospy.Time.now()
		g_twist_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
		g_target_twist = Twist() # initializes to zero
		g_last_twist = Twist()
		g_vel_scales[0] = fetch_param('~angular_scale', 0.6)
		g_vel_scales[1] = fetch_param('~linear_scale', 0.8)
		g_vel_ramps[0] = fetch_param('~angular_accel', 1.0)
		g_vel_ramps[1] = fetch_param('~linear_accel', 1.0)
		move = False
		#followDistance=0.8
		stopDistance=0.6
		max_speed=0.5
		min_speed=0.01

		scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)
		cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
		command = Twist()
		command.linear.x = 0.0
		command.linear.y = 0.0
		command.linear.z = 0.0
		command.angular.x = 0.0
		command.angular.y = 0.0
		command.angular.z = 0.0
		rate = rospy.Rate(10)
		#closest = 0
		cnt=0
		last_closest =0
		rospy.spin()
