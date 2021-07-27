#! /usr/bin/env python

from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
import rospy
import time

def callback_pointcloud(data):
    assert isinstance(data, PointCloud2)
    gen = point_cloud2.read_points(data, field_names=("x", "y", "z"), skip_nans=True)
    time.sleep(1)
    print type(gen)
    for p in gen:
      print " x : %.3f  y: %.3f  z: %.3f" %(p[0],p[1],p[2])

def main():
    rospy.init_node('pcl_listener', anonymous=True)
    rospy.Subscriber('/camera/depth_registered/points', PointCloud2, callback_pointcloud)
    try:
    	rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    main()