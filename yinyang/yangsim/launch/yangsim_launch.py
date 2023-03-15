from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="yangsim",
            executable="yangnode",
            name="custom_yangnode",
            output="screen",
            emulate_tty=True,
            parameters=[
                {"shout": True}
            ]
        )
    ])