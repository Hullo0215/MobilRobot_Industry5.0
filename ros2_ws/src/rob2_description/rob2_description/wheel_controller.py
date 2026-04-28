import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState

class WheelController(Node):

    def __init__(self):
        super().__init__('wheel_controller')

        self.sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cb,
            10)

        self.pub = self.create_publisher(
            JointState,
            '/joint_states',
            10)

        self.left = ['B1_1_joint', 'B2_1_joint', 'B3_1_joint', 'B4_1_joint', 'B5_1_joint', 'B6_1_joint']
        self.right = ['J1_1_joint', 'J2_1_joint', 'J3_1_joint', 'J4_1_joint', 'J5_1_joint', 'J6_1_joint']

        self.names = self.left + self.right
        self.positions = [0.0] * 12

    def cb(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z

        left_speed = linear - angular
        right_speed = linear + angular

        # update positions
        for i in range(6):
            self.positions[i] += left_speed * 0.1

        for i in range(6, 12):
            self.positions[i] += right_speed * 0.1

        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = self.names
        js.position = self.positions

        self.pub.publish(js)


def main(args=None):
    rclpy.init(args=args)
    node = WheelController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
