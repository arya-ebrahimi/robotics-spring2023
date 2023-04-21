import math
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from turtlesim.srv import Spawn

class FrameListener(Node):

    def __init__(self):
        super().__init__('turtlemania_tf2_frame_listener')
        self.target_frame = self.declare_parameter(
            'target_frame', 'turtle').get_parameter_value().string_value

        self.source_frame = self.declare_parameter(
            'source_frame', 'turtle').get_parameter_value().string_value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.spawner = self.create_client(Spawn, 'spawn')
        self.turtle_spawning_service_ready = False
        self.turtle_spawned = False

        self.publisher = self.create_publisher(Twist,self.source_frame+'/cmd_vel',1)

        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):

        from_frame_rel = self.target_frame
        to_frame_rel = self.source_frame

        if self.turtle_spawning_service_ready:
            if self.turtle_spawned:
                try:
                    when = self.get_clock().now() - rclpy.time.Duration(seconds=2.0)
                    t = self.tf_buffer.lookup_transform_full(
                        target_frame=to_frame_rel,
                        target_time=rclpy.time.Time(),
                        source_frame=from_frame_rel,
                        source_time=when,
                        fixed_frame='world')
                except (LookupException, ConnectivityException, ExtrapolationException):
                    self.get_logger().info('transform not ready')
                    return

                msg = Twist()
                scale_rotation_rate = 1.0
                msg.angular.z = scale_rotation_rate * math.atan2(
                    t.transform.translation.y,
                    t.transform.translation.x)

                scale_forward_speed = 0.5
                msg.linear.x = scale_forward_speed * math.sqrt(
                    t.transform.translation.x ** 2 +
                    t.transform.translation.y ** 2)

                self.publisher.publish(msg)
            else:
                if self.result.done():
                    self.get_logger().info(
                        f'Successfully spawned {self.result.result().name}')
                    self.turtle_spawned = True
                else:
                    self.get_logger().info('Spawn is not finished')
        else:
            if self.spawner.service_is_ready():
                request = Spawn.Request()
                request.name = self.source_frame
                request.x = 4.0
                request.y = 2.0
                request.theta = 0.0
                self.result = self.spawner.call_async(request)
                self.turtle_spawning_service_ready = True
            else:
                self.get_logger().info('Service is not ready')


def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
