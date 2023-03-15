#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/char.hpp"

#define DELIMETER ','

using namespace std::chrono_literals;
using namespace std;

/* This example creates a subclass of Node and uses std::bind() to register a
 * member function as a callback from the timer. */

class Bob : public rclcpp::Node {

public:
  Bob() : Node("Bob")
  {
    publisher_ = this->create_publisher<std_msgs::msg::Char>("topic", 10);
    timer_ = this->create_wall_timer(1000ms, bind(&Bob::timer_callback, this));
  }


private:
  
  int count = 0;

  char xor_encrypt(char x, int i) {
    char key[] = "9822762175";
    int j = i % strlen(key);
    return x ^ key[j];
  }

  void timer_callback() {
    char msg[] = "NEED_HELP!,";
    auto message = std_msgs::msg::Char();
    char pm = xor_encrypt(msg[count], count);
    message.data = pm;
    publisher_->publish(message);

    if (msg[count] == DELIMETER) {
      count = 0;
    } else {
      count = (count+1) % strlen(msg);
    }
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::Char>::SharedPtr publisher_;
};

int main(int argc, char *argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(make_shared<Bob>());
  rclcpp::shutdown();
  return 0;
}
