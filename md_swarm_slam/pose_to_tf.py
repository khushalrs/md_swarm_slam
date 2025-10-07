# md_swarm_slam/nodes/tf_to_odom.py
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import Buffer, TransformListener
from rclpy.time import Time

class TFToOdom(Node):
    def __init__(self):
        super().__init__('tf_to_odom')
        self.declare_parameter('odom_frame', 'drone1/odom')
        self.declare_parameter('base_frame', 'drone1/base_link')
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        self.pub = self.create_publisher(Odometry, 'odom', 10)
        self.timer = self.create_timer(0.02, self.tick)  # 50 Hz

    def tick(self):
        odom_frame = self.get_parameter('odom_frame').get_parameter_value().string_value
        base_frame = self.get_parameter('base_frame').get_parameter_value().string_value
        try:
            tf: TransformStamped = self.buffer.lookup_transform(odom_frame, base_frame, Time())
            msg = Odometry()
            msg.header.stamp = tf.header.stamp
            msg.header.frame_id = odom_frame
            msg.child_frame_id = base_frame
            msg.pose.pose.position.x = tf.transform.translation.x
            msg.pose.pose.position.y = tf.transform.translation.y
            msg.pose.pose.position.z = tf.transform.translation.z
            msg.pose.pose.orientation = tf.transform.rotation
            self.pub.publish(msg)
        except Exception:
            pass

def main():
    rclpy.init()
    n = TFToOdom()
    rclpy.spin(n)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
