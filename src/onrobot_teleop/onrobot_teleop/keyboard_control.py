#!/usr/bin/env python3

import sys
import termios
import tty
import time

import pyspacemouse
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

# Keyboard:
#   ros2 run onrobot_teleop keyboard_control

# SpaceMouse:
#   ros2 run onrobot_teleop keyboard_control --ros-args -p control_mode:=spacemouse


class RG2KeyboardControl(Node):
    def __init__(self):
        super().__init__('onrobot_teleop_control')

        self.declare_parameter('control_mode', 'keyboard')
        self.control_mode = self.get_parameter('control_mode').value.lower()

        if self.control_mode not in ('keyboard', 'spacemouse'):
            self.get_logger().error("control_mode must be 'keyboard' or 'spacemouse'.")
            raise ValueError("Invalid control_mode")

        self.step = 0.005
        self.gripper_repeat_time = 0.1
        self.min_width = 0.0
        self.max_width = 0.110
        self.current_width = None

        # spacemouse
        self.command_pub = self.create_publisher(
            Float64MultiArray, '/onrobot/finger_width_controller/commands', 10
        )
        self.joint_sub = self.create_subscription(
            JointState, '/onrobot/joint_states', self.joint_state_callback, 10
        )

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

    def open_gripper(self):
        self.publish_width(self.max_width)

    def close_gripper(self):
        self.publish_width(self.min_width)

    def increase_width(self):
        if self.current_width is not None:
            self.publish_width(self.current_width + self.step)

    def decrease_width(self):
        if self.current_width is not None:
            self.publish_width(self.current_width - self.step)


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def get_arrow_key():
    key = get_key()
    if key == '\x1b':
        key2 = get_key()
        if key2 == '[':
            key3 = get_key()
            if key3 == 'A':
                return 'UP'
            if key3 == 'B':
                return 'DOWN'
    return key


def main(args=None):
    rclpy.init(args=args)
    node = RG2KeyboardControl()

    while rclpy.ok() and node.current_width is None:
        rclpy.spin_once(node, timeout_sec=0.1)

    if node.current_width is None:
        node.get_logger().error('Could not get RG2 joint state.')
        node.destroy_node()
        rclpy.shutdown()
        return

    if node.control_mode == 'keyboard':
        print('\nRG2 Keyboard Control')
        print('--------------------')
        print('o : fully open')
        print('c : fully close')
        print('↑ : open 5 mm')
        print('↓ : close 5 mm')
        print('q : quit')
        print(f'\nCurrent width: {node.current_width * 1000:.1f} mm\n')

        try:
            while rclpy.ok():
                key = get_arrow_key()

                if key == 'o':
                    node.open_gripper()
                elif key == 'c':
                    node.close_gripper()
                elif key == 'UP':
                    node.increase_width()
                elif key == 'DOWN':
                    node.decrease_width()
                elif key in ('q', '\x03'):  # q or Ctrl+C
                    break

                rclpy.spin_once(node, timeout_sec=0.0)

        except KeyboardInterrupt:
            pass

    # SPACEMOUSE CONTROL
    else:
        print('\nRG2 SpaceMouse Control')
        print('----------------------')
        print('Left button  : open 5 mm')
        print('Right button : close 5 mm')
        print('Ctrl+C       : quit')
        print(f'\nCurrent width: {node.current_width * 1000:.1f} mm\n')

        device = None

        try:
            device = pyspacemouse.open()

            if device is None:
                node.get_logger().error('Could not open SpaceMouse.')
                return

            node.get_logger().info( 'SpaceMouse connected.' )

            while rclpy.ok():
                state = device.read()
                buttons = state.buttons
                # print("buttons:", buttons)
                # pyspacemouse reports at idx 0 and 14                
                # if buttons[0]:
                #     node.increase_width()
                # elif buttons[14]:
                #     node.decrease_width()

                if bool(buttons[0]) and bool(buttons[14]):
                    pass
                elif bool(buttons[0]):
                    node.increase_width()
                elif bool(buttons[14]):
                    node.decrease_width()



                rclpy.spin_once(node, timeout_sec=0.01)
                time.sleep(node.gripper_repeat_time)

        except KeyboardInterrupt:
            pass
        finally:
            if device is not None:
                device.close()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
