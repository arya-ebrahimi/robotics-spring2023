import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import numpy as np


ROTATE_90_DEGREE = 60
TIMER = 0.1
ANGULAR_VEL = 0.5
ANGULAR_VEL_RATIO = 0.001


class RGB_NAV(Node):
    def __init__(self):
        super().__init__('rgb_navigate')
        
        self.pub = self.create_publisher(Twist, '/model/eddiebot/cmd_vel', 10)
        self.eddie_camera = self.create_subscription(Image, '/kinect_rgbd_camera/image', self.eddie_camera_cb, 10)
        
        self.call_timer = self.create_timer(TIMER, self._timer_cb)
        self.forward = True
        self.red = False
        self.yellow = False
        self.green = False
        self.rotate_counter = 0
        self.ang_vel_from_image = 0.0
        self.finished = False
 
    def _timer_cb(self):
        velocity = Twist()
        
        if self.red:
            velocity.angular.z = ANGULAR_VEL
            velocity.linear.x = 0.0
            self.rotate_counter += 1
            if self.rotate_counter == ROTATE_90_DEGREE:
                self.red = False
                self.forward = True
                self.rotate_counter = 0
                
        if self.yellow:
            velocity.angular.z = -ANGULAR_VEL
            velocity.linear.x = 0.0
            self.rotate_counter += 1
            if self.rotate_counter == ROTATE_90_DEGREE:
                self.yellow = False
                self.forward = True
                self.rotate_counter = 0
                
        if self.green:
            self.finished = True
            self.green = False
            
        if self.finished:
            velocity.linear.x = 0.0
            velocity.angular.z = ANGULAR_VEL
        
        if self.forward:
            velocity.linear.x = 1.0
            velocity.angular.z = -ANGULAR_VEL_RATIO * self.ang_vel_from_image
            self.get_logger().info(str(velocity.angular.z))

        
        
        self.pub.publish(velocity)
        
    def eddie_camera_cb(self, msg):
        
        height = msg.height
        width = msg.width

                    
        channel = msg.step//msg.width
        frame = np.reshape(msg.data, (height, width, channel))
        
        if not self.finished:
            if frame[:, :, 2].max() < 20:
                self.forward = False
                # red
                if frame[:, :, 1].max() < 20:
                    self.red = True
                    self.get_logger().info('RED')

                # green
                elif frame[:, :, 0].max() < 20:
                    self.green = True
                    self.get_logger().info('GREEN')
                    
                # yellow    
                else:
                    self.yellow = True
                    self.get_logger().info('YELLOW')
                    
            if self.forward:
                mid_row = frame[int(height/2), :, 2]
                left = mid_row[0:int(width/2)]
                right = mid_row[int(width/2):]            
                
                la = (left<20).sum()
                ra = (right<20).sum()
                        
                self.ang_vel_from_image = ra - la
            
                
        
                

        
        
        


        
    
def main(args=None):    
    rclpy.init(args=args)
    nav = RGB_NAV()
    rclpy.spin(nav)
    rclpy.shutdown()


if __name__ == '__main__':
    main()