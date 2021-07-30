#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
import geometry_msgs.msg

if __name__ == '__main__':
     
     rospy.init_node('tf_listener')
     listener = tf.TransformListener()
     car_vel = rospy.Publisher('cmd_vel', geometry_msgs.msg.Twist,queue_size=1)
     rate = rospy.Rate(10.0)

     while not rospy.is_shutdown():
         try:
             (trans,rot) = listener.lookupTransform('ball','camera_link', rospy.Time(0))
         except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
             continue
	
	 print " pos_x : %.3f  pos_y: %.3f  pos_z: %.3f" %(trans[0],trans[1],trans[2])
             
         angular = math.atan2(trans[1], trans[0])
         linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2 + trans[2] ** 2)
         cmd = geometry_msgs.msg.Twist()
         cmd.linear.x = linear
         cmd.angular.z = angular
         car_vel.publish(cmd)
         rate.sleep()
