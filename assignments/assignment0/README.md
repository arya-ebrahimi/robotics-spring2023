# Assignment1
----
## Distrobox Installation
Initially, the installation of distrobox is required, which can be accomplished through the utilization of the PPA repository in the following manner:
````bash
sudo add-apt-repository ppa:michel-slm/distrobox
sudo apt update
sudo apt install distrobox
````
For distrobox to function properly, container managers like Docker or Podman are necessary. In this instance, Docker was employed and can be installed and set up for non-sudo execution as outlined below:

1. Install docker:
````bash
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt install docker-ce
````
2. Execute without sudo
```` bash
sudo usermod -aG docker user
su - user
````
----
## Create and Enter rosbox
After installing Docker, you can create a distrobox environment with ros2-humble pre-installed using the following commands.

Note that by default, distrobox uses Podman. To use Docker insted, a configuration file should be created in `/usr/share/distrobox/distrobox.conf`, containing `container_manager="docker"` to specify Docker as the container manager which is used.

```` bash
docker pull osrf/ros:humble-desktop
distrobox create --image osrf/ros:humble-desktop --name rosbox
````
Finally, enter rosbox and source ros2 by executing the following commands:
```` bash
distrobox enter rosbox -- bash
. /opt/ros/humble/setup.bash
````

----
## Exercise
Create three terminals, enter rosbox and source ros2 in all of them. 
- First terminal:
  ```` bash
  ros2 run turtlesim turtlesim_node
  ````
- Second terminal:
  ```` bash
  rqt
  ````
  After running this command, a window will popup. select spawn service and spawn a turtle named turtle2.
  ![](https://github.com/Arya-Ebrahimi/robotics-spring2023/blob/main/assets/assignments/assignment0/1.png)
  
- third terminal:
  For controlling the first turtle, simply run the following command:
  ```` bash
  ros2 run turtlesim turtle_teleop_key
  ````
  Since `turtle_teleop_key` default subscribed topic is `turtle1/cmd_vel`, a remapping should be made to controll turtle2.
  ```` bash
  ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=turtle2/cmd_vel
  ````
