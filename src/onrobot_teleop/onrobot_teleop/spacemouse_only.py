#!/usr/bin/env python3

'''
Spacemouse

    Left button : open 5 mm
    Right button : close 5 mm

Publisher:
    /onrobot/finger_width_controller/commands
    std_msgs/msg/Float64MultiArray

Subscriber:
    /onrobot/joint_states
    sensor_msgs/msg/JointState

    
"""Current state of the SpaceMouse device.

Attributes:
t: Timestamp (seconds since program start)
x: X-axis translation [-1.0, 1.0]
y: Y-axis translation [-1.0, 1.0]
z: Z-axis translation [-1.0, 1.0]
roll: Roll rotation [-1.0, 1.0]
pitch: Pitch rotation [-1.0, 1.0]
yaw: Yaw rotation [-1.0, 1.0]
buttons: List of button states (0 or 1)
"""

t: float = -1.0
x: float = 0.0
y: float = 0.0
z: float = 0.0
roll: float = 0.0
pitch: float = 0.0
yaw: float = 0.0
buttons: ButtonState = field(default_factory=lambda: ButtonState([]))

# indices 0 and 14

'''
import termios
import time
import sys
import tty

import pyspacemouse
import rclpy 
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray


# device = pyspacemouse.open()

# if device is None:
#     print('Could one open Spacemouse')
#     exit()

# print('Spacemouse connected!')


# try:
#     while True:
#         state = device.read()

#         print(state.x, state.y, state.z, state.roll, state.pitch, state.yaw, state.buttons)


# except KeyboardInterrupt:
#     pass

# finally:
#     device.close()




class RG2SpaceMouseControl(Node):
    def __init__(self):
        super().__init__('onrobot_teleop_control')

        self.step = 0.005
        self.min_width = 0.0
        self.max_width = 0.110
        self.current_width = None
        self.gripper_repeat_time = 0.1

        self.command_pub = self.create_publisher(Float64MultiArray, '/onrobot/finger_width_controller/commands', 10)
        self.joint_sub = self.create_subscription(JointState, '/onrobot/joint_states', self.joint_state_callback, 10)

    def joint_state_callback(self, msg):
        if 'finger_width' in msg.name and self.current_width is None:
            index = msg.name.index('finger_width')
            self.current_width = msg.position[index]

    def publish_width(self, width):
        width = max(self.min_width, min(self.max_width, width))
        self.current_width = width

        msg = Float64MultiArray()
        msg.data = [width]
        self.command_pub.publish(msg)

        self.get_logger().info(f'RG2 width: {width * 1000:.1f} mm')


    def increase_width(self):
        if self.current_width is not None:
            self.publish_width(self.current_width + self.step)

    def decrease_width(self):
        if self.current_width is not None:
            self.publish_width(self.current_width - self.step)



def main(args=None):
    rclpy.init(args=args)
    node = RG2SpaceMouseControl()

    while rclpy.ok() and node.current_width is None:
        rclpy.spin_once(node, timeout_sec=0.1)

    if node.current_width is None:
        node.get_logger().error('Could not get RG2 joint state.')
        node.destroy_node()
        rclpy.shutdown()
        return

    print('\nRG2 Spacemouse Control')
    print('--------------------')

    print('Left button : open 5 mm')
    print('Right button : close 5 mm')
    print('q : quit')
    print(f'\nCurrent width: {node.current_width * 1000:.1f} mm\n')

    device = None
    try:
        device = pyspacemouse.open()

        if device ==None:
            node.get_logger().error('Could not open Spacemouse')
            return

        node.get_logger().info('Spacemouse Connected')

        while rclpy.ok():
            state = device.read()
            button = state.buttons

            if bool(button[0]) and bool(button[14]):
                pass 
            elif bool(button[0]):
                node.increase_width()
            elif bool(button[14]):
                node.decrease_width()

            rclpy.spin_once(node, timeout_sec=0.01)
            time.sleep(node.gripper_repeat_time)

    except KeyboardInterrupt:
        pass
    finally:

        if device is not None:
            device.close()

        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()