# Yin-Yang
simple ROS2 packages, one in python and one in c++ that are communicating with each other using services


It contains two nodes that are communicating using services. Each node has its own service alongside a client to send requests to another's service.
Yin(first node) starts by sending a request to the Yang(second node), and when Yang receives the message, it replies with its request. This process continues till it reaches the end of the predefined messages. Each node publishes the received message to the /conversation topic. 
