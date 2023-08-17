import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time
import random

class Maze2(Node):
    def __init__(self):
        super().__init__('maze2')
        

        self.allmore = False
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.sub = self.create_subscription(LaserScan, '/lidar', self.sub_callback, 10)
        self.sub
        
        # self.call_timer = self.create_timer(1.0, self._timer_cb)
        self.backward = False
        self.first_time = True
        self.rotate = False
        
    def sub_callback(self, msg):
        # self.get_logger().info(str(msg.ranges))
        self.allmore = True
        counter = 0
        for i in msg.ranges:
            counter+=1
            if i < 0.5:
                self.allmore = False
                break
            
        velocity = Twist()
        
        if self.allmore and not self.backward and not self.rotate:
            velocity.angular.z = 0.0
            velocity.linear.x = 0.7

        else:
            if self.first_time:
                self.time = time.time()
                self.backward = True
                self.first_time = False
                
            if self.backward:
                velocity.angular.z = 0.0
                velocity.linear.x = -0.7
                
                if abs(time.time() - self.time) > 2.0:
                    self.backward = False
                    self.rotate = True
                    self.rotate_time = time.time()

                    
            if self.rotate:
                velocity.angular.z = -0.5
                velocity.linear.x = 0.0
                
                if abs(time.time() - self.rotate_time) > 2.0:
                    self.rotate = False
                    self.first_time = True
                    
        self.pub.publish(velocity)


        
    
def main(args=None):    
    rclpy.init(args=args)
    maze = Maze2()
    rclpy.spin(maze)
    rclpy.shutdown()


if __name__ == '__main__':
    main()