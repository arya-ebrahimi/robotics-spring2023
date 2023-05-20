from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import (
    IncludeLaunchDescription
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    ld = LaunchDescription()
    
    ld.add_action(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
            launch_arguments={'gz_args': '-r /home/arya/gazebo_ws/src/maze/sdf/maze.sdf'}.items(),
        )
    )

    ld.add_action(
        Node(
            package='maze',
            executable='maze'
        )
    )
    
    ld.add_action(
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                       '/lidar@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan'],
        )
    )
    
    # ld.add_action(
    #     Node(
    #         package='rviz2',
    #         executable='rviz2',
    #     )
    # )

    return ld