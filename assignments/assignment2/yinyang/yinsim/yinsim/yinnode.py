import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String
import time

from yinyang_msgs.action import Bye
from yinyang_msgs.srv import Pipi


class Yin(Node):
    
    def __init__(self):
        super().__init__('yin')
                
        client_cb_group = None
        timer_cb_group = None
        self.srv = self.create_service(Pipi, 'yin_service', self.srv_callback)
        self.cli = self.create_client(Pipi, 'yang_service', callback_group=client_cb_group)
        self.call_timer = self.create_timer(1, self._timer_cb, callback_group=timer_cb_group)

        self.publisher_ = self.create_publisher(String, 'conversation', 10)
        
        self.action_server = ActionServer(
            self, 
            Bye,
            'bye',
            execute_callback=self.execute_callback
        )
        
        self.declare_parameter('shout', True)
        self.declare_parameter('opacity', 100)
        
        self.req = Pipi.Request()
        self.count = 0
        self.str = [
            "I am Yin, some mistake me for an actual material entity but I am more of a concept",
            "Interesting Yang, so one could say, in a philosophical sense, we are two polar elements",
            "We, Yang, are therefore the balancing powers in the universe.",
            "Difficult and easy complete each other.",
            "Long and short show each other.",
            "Noise and sound harmonize each other.",
            "You shine your light."
        ]
        
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting...')

        self.time_to_send = True
        self.finish = False
        
        
    def execute_callback(self, goal_handle):
        
        if 'bye' in goal_handle.request.a:
            self.get_logger().info('accepted')
            self.get_logger().info(goal_handle.request.a)
            feedback_msg = Bye.Feedback()
            opacity = self.get_parameter('opacity').get_parameter_value().integer_value
            
            for i in range (opacity, -1, -1):
                feedback_msg.opacity = i
                goal_handle.publish_feedback(feedback_msg)
                time.sleep(0.01)
            
            goal_handle.succeed()
            result = Bye.Result()
            result.b = 'farewell'
            self.finish = True
            self.time_ = time.time()
            return result            


    def _timer_cb(self):
        if self.finish:
            if (time.time() - self.time_ > 2):
                raise SystemExit
            
        if(self.time_to_send and self.count < len(self.str)):
            shout = self.get_parameter('shout').get_parameter_value().bool_value
            
            req_str = self.str[self.count]
            l = len(req_str)
            if shout:
                req_str = '**' + req_str + '**'
                l += 4
            
            self.req.a = req_str
            self.req.len = l
            self.count +=1
            _ = self.cli.call_async(self.req)
            self.get_logger().info('request sent')
            self.time_to_send = False


    def srv_callback(self, req, res):
        self.get_logger().info(req.a)
        msg = String()
        
        s = 'Yang said: '+ req.a + ', ' + str(req.len)
        sum = 0
        for word in req.a:
            for ch in word:
                sum += ord(ch)
        s = s + ', ' + str(sum)
                
        msg.data = s
        self.publisher_.publish(msg)
        res.checksum = sum
        self.time_to_send = True
        return res


def main(args=None):
    rclpy.init(args=args)
    # executor = MultiThreadedExecutor()

    yin = Yin()
    
    try:
        rclpy.spin(yin)
    except SystemExit:
        rclpy.logging.get_logger("Quitting").info('Done')
    # executor.add_node(yin)
    # executor.spin()
    
    yin.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
