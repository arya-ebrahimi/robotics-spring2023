#include <chrono>
#include <memory>
#include <sstream>
#include <future>
#include <string>
#include <functional>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "rclcpp_components/register_node_macro.hpp"

#include "yinyang_msgs/srv/pipi.hpp"
#include "yinyang_msgs/action/bye.hpp"
#include "std_msgs/msg/string.hpp"


#define MAX 7

using namespace std::chrono_literals;
using namespace std::placeholders;

using Bye = yinyang_msgs::action::Bye;
using GoalHandle = rclcpp_action::ClientGoalHandle<Bye>;

    char* str[] = {
      "Hi Yin, I am Yang the opposite of you.",
      "Yes, Yin; we ourselves, do not mean anything since we are only employed to express a relation",
      "Precisely, Yin; we are used to describe how things function in relation to each other and to the universe.",
      "For what is and what is not beget each other.",
      "High and low place each other.",
      "Before and behind follow each other.",
      "And you fade into the darkness."
    };

namespace cb_group_demo
{
class DemoNode : public rclcpp::Node
{
public:



    DemoNode() : Node("client_node")
    {
        client_cb_group_ = nullptr;
        timer_cb_group_ = nullptr;
        this->declare_parameter("shout", false);
        publisher_ = this->create_publisher<std_msgs::msg::String>("conversation", 10);

        client_ptr_ = this->create_client<yinyang_msgs::srv::Pipi>(
          "yin_service", 
          rmw_qos_profile_services_default, client_cb_group_);
        
        service_ptr_ = this->create_service<yinyang_msgs::srv::Pipi>(
          "yang_service",
          std::bind(&DemoNode::service_callback, this, _1, _2, _3)
        );
        timer_ptr_ = this->create_wall_timer(1s, std::bind(&DemoNode::timer_callback, this),
                                            timer_cb_group_);
                            
        action_client_ptr_ = rclcpp_action::create_client<Bye>(
          this,
          "bye");
        
    }

private:

    int count = 0;
    bool time_to_send = false;
    bool goal_sent = false;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;

    rclcpp::CallbackGroup::SharedPtr client_cb_group_;
    rclcpp::CallbackGroup::SharedPtr timer_cb_group_;
    rclcpp::Client<yinyang_msgs::srv::Pipi>::SharedPtr client_ptr_;
    rclcpp::TimerBase::SharedPtr timer_ptr_;
    rclcpp::Service<yinyang_msgs::srv::Pipi>::SharedPtr service_ptr_;

    rclcpp_action::Client<Bye>::SharedPtr action_client_ptr_;


    void service_callback(
            const std::shared_ptr<rmw_request_id_t> request_header,
            const std::shared_ptr<yinyang_msgs::srv::Pipi::Request> request,
            const std::shared_ptr<yinyang_msgs::srv::Pipi::Response> response)
    {
        
        std::stringstream ss;
        ss << "";
        ss << request->a;
        RCLCPP_INFO(this->get_logger(), ss.str().c_str());
        
        int checksum = 0;
        for (int i = 0; i < (int)request->len; i++) {
          checksum += request->a[i];
        }
        response->checksum = checksum;
        auto message = std_msgs::msg::String();
        message.data = "Yin said: " + request->a + ", " + std::to_string(request->len) + ", " + std::to_string(checksum);

        publisher_->publish(message);
        this->time_to_send = true;
    }

    void goal_response_callback(const GoalHandle::SharedPtr & goal_handle) {
      if (!goal_handle) {
        RCLCPP_ERROR(this->get_logger(), "Goal was rejected by server");
      } else {
        RCLCPP_INFO(this->get_logger(), "Goal accepted by server, waiting for result");
      }
    }

    void feedback_callback(GoalHandle::SharedPtr, const std::shared_ptr<const Bye::Feedback> feedback) {
      
      std::stringstream ss;
      auto number = feedback->opacity;
      ss << number << " ";
      RCLCPP_INFO(this->get_logger(), ss.str().c_str());
    }

    void result_callback(const GoalHandle::WrappedResult & result) {
      switch (result.code) {
        case rclcpp_action::ResultCode::SUCCEEDED:
          break;
        case rclcpp_action::ResultCode::ABORTED:
          RCLCPP_ERROR(this->get_logger(), "Goal was aborted");
          return;
        case rclcpp_action::ResultCode::CANCELED:
          RCLCPP_ERROR(this->get_logger(), "Goal was canceled");
          return;
        default:
          RCLCPP_ERROR(this->get_logger(), "Unknown result code");
          return;
      }
      std::stringstream ss;
      ss << "Result received: ";
      ss << result.result->b;
      RCLCPP_INFO(this->get_logger(), ss.str().c_str());

      throw 0;
      // rclcpp::shutdown();
    }

    void timer_callback()
    {
      // RCLCPP_INFO(this->get_logger(), " ");

      if (this->time_to_send && this->count < MAX) {
        bool shout = this->get_parameter("shout").get_parameter_value().get<bool>();
        auto request = std::make_shared<yinyang_msgs::srv::Pipi::Request>();
        // request->a = str[this->count];

        std::string pm(str[this->count]);
        
        request->a = pm;
        request->len = std::strlen(str[this->count]);

        if (shout) {
          request->a = "**" + pm + "**";
          request->len = std::strlen(str[this->count]) + 4;
        } 

        this->count = this->count + 1;
        auto result_future = client_ptr_->async_send_request(request);
        this->time_to_send = false;
        RCLCPP_INFO(this->get_logger(), "request sent");
      }

      if (this->count == MAX && !this->goal_sent) {
        auto goal_msg = Bye::Goal();
        goal_msg.a = "Good bye";

        RCLCPP_INFO(this->get_logger(), "Sending goal");

        auto send_goal_options = rclcpp_action::Client<Bye>::SendGoalOptions();

        send_goal_options.goal_response_callback =
          std::bind(&DemoNode::goal_response_callback, this, _1);
        send_goal_options.feedback_callback =
          std::bind(&DemoNode::feedback_callback, this, _1, _2);
        send_goal_options.result_callback =
          std::bind(&DemoNode::result_callback, this, _1);
        this->action_client_ptr_->async_send_goal(goal_msg, send_goal_options);

        this->goal_sent = true;
      
      }

    }
};  // class DemoNode
}   // namespace cb_group_demo

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    auto client_node = std::make_shared<cb_group_demo::DemoNode>();
    rclcpp::executors::MultiThreadedExecutor executor;
    executor.add_node(client_node);

    try
    {
      executor.spin();

    }
    catch(int error)
    {
      rclcpp::shutdown();
    }
    

    return 0;
}