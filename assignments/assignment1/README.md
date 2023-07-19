# Assignment1
----
## Exercise1

1. To change a node's name, the `--remap` argument can be used with the following command, which renames the node `turtle1` to `my_turtle01`:
   ```` bash
   ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle01
   ````
This command creates a new node named `my_turtle01`. By running `ros2 node list` command, we can observe the newly created node in the list.
![](https://github.com/Arya-Ebrahimi/robotics-spring2023/blob/main/assets/assignments/assignment1/1.png)

2. 
