#! /usr/bin/env python

from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from geometry_msgs.msg import Point
import rospy
import time
import tf


def callback_blob(data):
    global px, py
    px = int(data.x)
    py = int(data.y)

def callback_pointcloud(data):

    assert isinstance(data, PointCloud2)
    gen = point_cloud2.read_points(data, field_names=("x", "y", "z"), skip_nans=True, uvs=[[px, py]])
    print(px, py)
    time.sleep(1)
    for p in gen:
        print " x : %.3f  y: %.3f  z: %.3f" %(p[2],-p[0],-p[1])
        br = tf.TransformBroadcaster()
        br.sendTransform((-p[2],p[1],p[0]),
                   tf.transformations.quaternion_from_euler(0, 0, 0),
                   rospy.Time.now(),
                   "camera_link",
                   "ball")
  

def main():

    rospy.init_node('pcl_listener', anonymous=True)
    rospy.Subscriber('/blob/point_blob',Point,callback_blob,queue_size=1)
    rospy.Subscriber('/camera/depth_registered/points', PointCloud2, callback_pointcloud,queue_size=1)
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":

    main()
