import rclpy
from rclpy.node import Node

from std_msgs.msg import Char


class Alice(Node):
    def __init__(self):
        self.count = 0
        self.delimeter = ','
        super().__init__('Alice')
        self.subscription = self.create_subscription(
            Char,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        key = '9822762175'
        def xor_decrypt(msg):
            j = self.count % len(key)
            xor = ord(msg) ^ ord(key[j])
            return chr(xor)
        
        de = xor_decrypt(chr(msg.data))
        
        if de == self.delimeter:
            self.get_logger().info('END OF PM')
            self.count = 0
            
        else:
            self.get_logger().info('I heard: "%c"' % de)
            self.count = self.count+1
            
def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = Alice()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
