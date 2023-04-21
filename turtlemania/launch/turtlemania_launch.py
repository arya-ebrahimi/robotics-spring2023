from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),

        Node(
            package='turtlemania',
            executable='tf2_broadcaster',
            name='broadcaster1',
            parameters=[
                {'turtlename': 'turtle1'}
            ]
        ),
        Node(
            package='turtlemania',
            executable='tf2_broadcaster',
            name='broadcaster2',
            parameters=[
                {'turtlename': 'turtle2'}
            ]
        ),
        Node(
            package='turtlemania',
            executable='tf2_broadcaster',
            name='broadcaster3',
            parameters=[
                {'turtlename': 'turtle3'}
            ]
        ),
        Node(
            package='turtlemania',
            executable='tf2_broadcaster',
            name='broadcaster4',
            parameters=[
                {'turtlename': 'turtle4'}
            ]
        ),

        Node(
            package='turtlemania',
            executable='tf2_listener',
            name='listener1',
            parameters=[
                {'target_frame':'turtle1'},
                {'source_frame' : 'turtle2'}
            ]
        ),
        

        Node(
            package='turtlemania',
            executable='tf2_listener',
            name='listener2',
            parameters=[
                {'target_frame':  'turtle2'},
                {'source_frame' : 'turtle3'}
            ]
        ),        
        

        Node(
            package='turtlemania',
            executable='tf2_listener',
            name='listener3',
            parameters=[
                {'target_frame': 'turtle3'},
                {'source_frame' : 'turtle4'}
            ]
        ),        

    ])