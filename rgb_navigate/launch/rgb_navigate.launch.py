from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import (
    IncludeLaunchDescription
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    eddie = get_package_share_directory('eddiebot_gazebo')

    ld = LaunchDescription()
    
    ld.add_action(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(eddie, 'launch', 'eddiebot_gz_sim.launch.py')),
            launch_arguments={'world': 'maze_marked'}.items(),
        )
    )

    ld.add_action(
        Node(
            package='rgb_navigate',
            executable='rgb_navigate'
        )
    )
    
    ld.add_action(
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                       '/kinect_rgbd_camera/image@sensor_msgs/msg/Image@gz.msgs.Image'],
        )
    )
    
    ld.add_action(
        Node(
            package='rqt_image_view',
            executable='rqt_image_view', 
            arguments=['/kinect_rgbd_camera/image']
        )
    )

    return ld