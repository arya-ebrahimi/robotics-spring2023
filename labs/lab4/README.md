# Lab4
----

MoveIt is a popular and powerful motion planning framework for robotic systems, widely used in ROS. MoveIt provides a set of high-level APIs and tools to simplify motion planning tasks, allowing robotic systems to plan and execute trajectories for manipulation tasks efficiently and safely.
 
MoveIt2 brings the capabilities of MoveIt to Ros2, enabling developers and roboticists to take advantage of the benefits of Ros2 for motion planning tasks. This includes support for real-time control, better handling of large-scale systems, improved security, and better integration with modern hardware. 
In this lab, we use MoveIt2 with Panda manipulator for motion planning.

## Exercise1
Simple motion plannings in Rviz2.
<p align="center">
  <img src="../../assets/labs/lab4/2.gif" alt="animated" />
</p>

## Exercise2
Motion planning using Ros2 node and package. Four poses are defined in which the panda's end effector tries to reach them one by one. The package is available in [`hello-moveit2`](hello_moveit2)
<p align="center">
  <img src="../../assets/labs/lab4/3.gif" alt="animated" />
</p>

In one terminal run 
```bash
ros2 launch moveit2_tutorials demo.launch.py
``` 
which runs Rviz2 node with panda manipulator, and in another terminal run:
```bash
ros2 run hello_moveit2 hello_moveit
``` 
## Exercise3
Motion planning using Ros2 node and package. The panda manipulator avoids collosion with the cylinder. The package is available in [`hello-moveit`](hello_moveit)
<p align="center">
  <img src="../../assets/labs/lab4/4.gif" alt="animated" />
</p>
