from setuptools import find_packages, setup

package_name = 'onrobot_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hanh',
    maintainer_email='hanhpt.phamtan@gmail.com',
    description='OnRobot Ros2 Control',
    license='MIT License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'keyboard_control = onrobot_teleop.keyboard_control:main',
            'keyboard_only = onrobot_teleop.keyboard_only:main',
            'spacemouse_only = onrobot_teleop.spacemouse_only:main',
        ],
    },
)
