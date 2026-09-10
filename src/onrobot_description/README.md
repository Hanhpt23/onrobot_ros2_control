# OnRobot_ROS2_Description

## Usage
For using Onrobot gripper alone, see [OnRobot_ROS2_Description](https://github.com/tonydle/OnRobot_ROS2_Description.git)

This package provides a ROS2 URDF description for OnRobot grippers. It uses XACRO macros to generate the URDF and includes a sample launch file to visualise the gripper. 

This package is used as a part of the [MELFA RV2FR ROBOT + ONROBOT RG2](https://github.com/Hanhpt23/melfa_ws)

## Quick Test

Install and build the project, see [README.md](https://github.com/Hanhpt23/melfa_ws/blob/main/README.md#install--build)
```bash
cd ~/AI
git clone https://github.com/Hanhpt23/melfa_ws.git
cd melfa_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

To quickly test the visualisation of the OnRobot gripper model, run the provided launch file:
```sh
ros2 launch onrobot_description view_onrobot.launch.py onrobot_type:=rg2
``` 
This launches RViz2 with the URDF loaded.


## License
This package was developed by [Tony Le](https://github.com/tonydle) and released under the MIT License, see [LICENSE](https://github.com/tonydle/OnRobot_ROS2_Description/blob/main/LICENSE).

The original mesh files and xacros are derived from [Osaka-University-Harada-Laboratory/onrobot](https://github.com/Osaka-University-Harada-Laboratory/onrobot), which is licensed under the MIT License.
