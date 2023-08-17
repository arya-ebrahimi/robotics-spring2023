import rclpy
from rclpy.node import Node
import time
import random 
from rclpy.action import ActionClient
from geometry_msgs.msg import Twist


class Lab7(Node):
    def __init__(self):
        super().__init__('simple_differntial_drive')
        
        self.forward = True
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.call_timer = self.create_timer(2.0, self._timer_cb)


    def _timer_cb(self):
        
        velocity = Twist()
        if (self.forward):
            velocity.angular.z = 0.0
            velocity.linear.x = 1.0
            self.forward=False
                
        else:
            velocity.angular.z = 0.0
            velocity.linear.x = -1.0
            self.forward=True            
        
        self.pub.publish(velocity)
    
def main(args=None):    
    rclpy.init(args=args)
    lab7 = Lab7()
    rclpy.spin(lab7)
    rclpy.shutdown()


if __name__ == '__main__':
    main()