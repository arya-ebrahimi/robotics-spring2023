from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch

from launch_ros.actions import Node 
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

from moveit_configs_utils.launches import DeclareBooleanLaunchArg

def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("FUMTI", package_name="fumti_config").to_moveit_configs()
    
    ld = generate_demo_launch(moveit_config)
    ld.add_action(
        DeclareBooleanLaunchArg(
            'use_sim_time', 
            default_value=True, 
            description='by default, we are not in debug mode', 
        )
    )
    
    
    return ld