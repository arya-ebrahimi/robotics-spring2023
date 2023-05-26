# Robotics-Spring2023
### This repository contains my projects and homeworks for the Robotics-Spring2023 course at the Ferdowsi University of Mashhad.

1. Introduction to ROS2
	- [ **Multi language publisher and subscriber**](https://github.com/Arya-Ebrahimi/Robotics-Spring2023/tree/main/multi_language_publisher_subscriber " **Multi language publisher and subscriber**") -> Two superficial nodes which are communicating with topics. Subscriber is developed using Python, and the publisher is programmed in C++. 

	- [ **Turtlesim controller**](https://github.com/Arya-Ebrahimi/Robotics-Spring2023/tree/main/turtlesim_controller " **Turtlesim controller**") -> A simple controller for turtlesim.

	- [ **Yin and Yang**](https://github.com/Arya-Ebrahimi/Robotics-Spring2023/tree/main/yinyang " **Yin and Yang**") -> Two packages, one in python and one in c++ that are communicating with each other using services and actions.

2. Introduction to TF2
	- [**Turtlemania**](https://github.com/Arya-Ebrahimi/Robotics-Spring2023/tree/main/turtlemania) -> turtles chasing each other using tf2 transforms.
3. Motion Planning using Moveit2
	- [**FUMTI**](https://github.com/Arya-Ebrahimi/Robotics-Spring2023/tree/main/FUMTI) -> motion planning using moveit, rviz and gazebo. 

4. Mobile Robots
	- [**Simple Differential Drive**](https://github.com/Arya-Ebrahimi/Robotics-Spring2023/tree/main/simple_differntial_drive) -> simple diff drive, forward and backward Twist published using ros2 topic and converted to gz topic using ros_gz_bridge.\
	![](https://github.com/Arya-Ebrahimi/Robotics-Spring2023/blob/main/simple_differntial_drive/gif/out.gif)
	

	- [**Maze**](https://github.com/Arya-Ebrahimi/Robotics-Spring2023/tree/main/maze) -> previous diff-drive in a maze, using LIDAR sensor to detect walls and preventing the collision.\
	![](https://github.com/Arya-Ebrahimi/Robotics-Spring2023/blob/main/maze/gif/out.gif)
	
	- [**RGB-Navigate**](https://github.com/Arya-Ebrahimi/Robotics-Spring2023/tree/main/rgb_navigate) -> Navigate eddiebot in a maze using RGB signs. first clone and build [eddiebot-ros](https://github.com/arashsm79/eddiebot-ros).\
	![](https://github.com/Arya-Ebrahimi/Robotics-Spring2023/blob/main/rgb_navigate/gif/out.gif)

