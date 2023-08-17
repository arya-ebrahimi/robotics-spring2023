from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import ExecuteProcess
from launch import LaunchDescription
from launch.conditions import IfCondition

import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource



def generate_launch_description():
    
    
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    
    ld = LaunchDescription()
    
    ld.add_action(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': '-r default.sdf'
        }.items(),
            ),
        )
    
    xacro_file = ('src/fumti/urdf/FUMTI.urdf.xacro')
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    
    params = {'robot_description' : doc.toxml()}
    
    ld.add_action(
        Node(
            package='robot_state_publisher', 
            executable='robot_state_publisher',
            output='screen',
            respawn=True,
            parameters=[params]
        )
    )
    
    ld.add_action(
        ExecuteProcess(
            cmd = ['ros2', 'control', 'load_controller', '--set-state', 'configured', 'joint_state_broadcaster'],
            output = 'screen'
        )
    )
    ld.add_action(
        ExecuteProcess(
            cmd = ['ros2', 'control', 'load_controller', '--set-state', 'configured', 'robot_controller'],
        )
    )

    ld.add_action(
        Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-string', doc.toxml(),
                #    '-name', 'FUMTI',
                #    '-allow_renaming', 'true',
                    # '-x', '1.2',
                    # '-z', '2.3',
                    # '-Y', '3.4',
                    '-topic', '/robot_description'],
        ) 
    )
    
    
    # ld.add_action(
    #     Node(
    #         package="ros_gz_sim",
    #         executable="create",
    #         output="screen",
    #         arguments=[
    #             # {"world": "empty.sdf"},
    #             "-string", doc.toxml()
    #         ],
    #     )
    # )
  
    return ld