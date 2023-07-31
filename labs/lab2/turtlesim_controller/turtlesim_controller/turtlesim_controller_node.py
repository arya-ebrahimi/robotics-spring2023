import rclpy
from rclpy.node import Node
import time
import random 
from rclpy.action import ActionClient
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.action import RotateAbsolute


class Controller(Node):
    def __init__(self):
        super().__init__('controller')
        
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.call_timer = self.create_timer(0.05, self._timer_cb)
        self.action_cli = ActionClient(self, RotateAbsolute, '/turtle1/rotate_absolute')

        self.declare_parameter('stop', False)
        self.reset_state()
        
    def reset_state(self):
        self.forward = True
        self.backward = False
        self.rotate = False
        self.hit_time = 0
        self.theta = 0


    def pose_callback(self, position):
        self.x = position.x
        self.y = position.y
        
        if (self.x > 11 or self.x < 0.5 or self.y > 11 or self.y < 0.5):
            self.forward = False
            self.backward = True
            self.hit_time = time.time()
                
    def feedback_callback(self, feedback_msg):
        self.get_logger().info(str(feedback_msg.feedback.remaining))
        
        if (abs(feedback_msg.feedback.remaining) < 0.05):
            self.reset_state()
        
    def _timer_cb(self):
        stop = self.get_parameter('stop').get_parameter_value().bool_value
        if stop:
            self.reset_state()
        else:
            if (self.rotate):
                goal = RotateAbsolute.Goal()
                goal.theta = self.theta
                                
                self.action_cli.wait_for_server()
                self.send_goal_future = self.action_cli.send_goal_async(goal=goal, feedback_callback=self.feedback_callback)

            else:
                velocity = Twist()
                if (self.forward):
                    velocity.angular.z = 0.0
                    velocity.linear.x = 1.0
                        
                if (self.backward):
                    velocity.angular.z = 0.0
                    velocity.linear.x = -1.0
                    if (time.time() - self.hit_time > 2):
                        self.forward=False
                        self.backward = False
                        self.rotate = True
                        self.theta = random.random()*360
                
                self.pub.publish(velocity)


        
        
        
    
def main(args=None):    
    rclpy.init(args=args)
    controller = Controller()
    rclpy.spin(controller)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
