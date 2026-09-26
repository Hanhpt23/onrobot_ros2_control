# OnRobot ROS2 Control (RG2/RG6) - 3D Spacemouse - Keyboard

3D Spacemouse and Keyboard control for OnRobot Grippers.

## 🎥 Demo

[![OnRobot RG2 Gripper - 3D SpaceMouse & Keyboard Control](https://img.youtube.com/vi/P3mi2jNRtLs/maxresdefault.jpg)](https://www.youtube.com/watch?v=P3mi2jNRtLs)

Click the image above to watch the demo on YouTube.

## Installation

```bash
cd ~/AI
git clone https://github.com/Hanhpt23/onrobot_ros2_control.git
cd onrobot_ros2_control
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash

```


## Usage
### Launch the driver
Launch the driver with `onrobot_type` [`rg2`,`rg6`] and `connection_type` [`serial` (UR Tool I/O) or `tcp` (Control Box)] arguments.
```sh
# Fake hardware
ros2 launch onrobot_driver onrobot_control.launch.py \
   onrobot_type:=rg2 \
   connection_type:=serial \
   use_fake_hardware:=true

# Real hardware
ros2 launch onrobot_driver onrobot_control.launch.py \
   onrobot_type:=rg2 \ 
   connection_type:=tcp \
   use_fake_hardware:=false \
   target_force:=20 
```

Other arguments:
- `use_fake_hardware` (default: `false`): Use mock hardware interface for testing
- `target_force` (default: 20 N): Target force of the gripper
- `launch_rviz` (default: `true`): Launch RViz with the gripper model
- `launch_rsp` (default: `true`): Launch the Robot State Publisher node (publishes to `/tf`)
- `device` (default: `/tmp/ttyUR`): Virtual Serial device path (if using Modbus Serial)
- `ip_address` (default: `192.168.1.1`): IP address of the Compute Box (if using Modbus TCP)
- `port` (default: `502`): Port of the Compute Box (if using Modbus TCP)

### Get the `finger_width` joint state (metres)
   ```sh
   ros2 topic echo /finger_width_controller/commands
   ```
### CLI - Manual Joint Position Control with `finger_width_controller`(JointGroupPositionController)
   ```sh
   ros2 topic pub --once /onrobot/finger_width_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.05]}"
   ```

### Controlling the gripper by 3D Spacemouse and Keyboard

```bash
source install/setup.bash

# Keyboard:
ros2 run onrobot_teleop keyboard_control

# SpaceMouse:
ros2 run onrobot_teleop keyboard_control --ros-args -p control_mode:=spacemouse

```

## Author

Developed by [Hanh Pham](https://hanhpt23.github.io/)

## License

This software is released under the MIT License, see [LICENSE](./LICENSE).


