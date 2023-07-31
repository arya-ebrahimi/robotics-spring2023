from launch_ros.actions import Node
from launch import LaunchDescription

def generate_launch_description():
    ld = LaunchDescription()
    
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node'
    )
    
    spawner_node = Node(
        package='turtle_chaser',
        executable='spawner'
    )
    
    chaser_node = Node(
        package='turtle_chaser',
        executable='chaser'
    )
    
    ld.add_action(turtlesim_node)
    ld.add_action(spawner_node)
    
    ld.add_action(chaser_node)   
    return ld
