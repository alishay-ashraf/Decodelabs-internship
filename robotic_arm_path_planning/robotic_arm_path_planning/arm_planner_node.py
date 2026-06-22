import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from geometry_msgs.msg import Pose

# Import MoveIt 2 bindings
from moveit.planning import MoveItPy

class ArmPlannerNode(Node):
    def __init__(self):
        super().__init__('arm_planner_node')
        
        # 1. Initialize MoveIt 2 for your specific 6-axis arm
        # Make sure the 'arm_manipulator' group name matches your MoveIt configuration file exactly
        self.moveit = MoveItPy(node_name="arm_planner_node")
        self.planning_component = self.moveit.get_planning_component("arm_manipulator")
        
        # 2. Initialize TF2 Buffer and Listener to monitor coordinate frames
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # 3. Create a timer loop running at 10 Hz
        self.timer = self.create_timer(0.1, self.control_loop)
        
        self.get_logger().info('Robotics Arm Planning Node has been started.')

    def control_loop(self):
        target_frame = 'end_effector'
        source_frame = 'world'
        
        try:
            # Safely look up the transform tree with a 1.0-second timeout buffer
            now = rclpy.time.Time()
            transform = self.tf_buffer.lookup_transform(
                target_frame,
                source_frame,
                now,
                timeout=Duration(seconds=1.0)
            )
            
            x = transform.transform.translation.x
            y = transform.transform.translation.y
            z = transform.transform.translation.z
            
            self.get_logger().info(f'Current Reality -> X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}')
            
            # Run the planning and execution method
            self.plan_and_execute_trajectory()
            
        except TransformException as ex:
            self.get_logger().warn(f'Could not transform {target_frame} to {source_frame}: {ex}')

    def plan_and_execute_trajectory(self):
        # Define Point B target pose parameters
        target_pose = Pose()
        target_pose.position.x = 0.45021  # 450.21 mm in meters
        target_pose.position.y = -0.12055 # -120.55 mm in meters
        target_pose.position.z = 0.31000  # 310.00 mm in meters
        
        # Orientation represented via Quaternions to prevent gimbal lock
        target_pose.orientation.x = 0.13
        target_pose.orientation.y = 0.58
        target_pose.orientation.z = -0.05
        target_pose.orientation.w = 0.84
        
        # Synchronize start state to the current configuration of the robot
        self.planning_component.set_start_state_to_current_state()
        
        # Set the destination goal for our end-effector link
        self.planning_component.set_goal_state(pose_stamped_msg=target_pose, link_name="end_effector")
        
        # Solve Inverse Kinematics and generate a smooth trajectory spline
        motion_plan = self.planning_component.plan()
        
        if motion_plan:
            self.get_logger().info("Trajectory spline successfully generated! Executing muscle control...")
            # Execute asynchronously (blocking=False) to ensure high-level system monitoring can abort if needed
            self.moveit.execute(motion_plan.trajectory, blocking=False)
        else:
            self.get_logger().error("Motion planning failed. Trapped in a local minimum or collision path detected.")

def main(args=None):
    rclpy.init(args=args)
    node = ArmPlannerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()