from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    # Build your MoveIt configuration environment components dynamically
    # This automatically loads your URDF and joint geometric tolerances
    moveit_config = (
        MoveItConfigsBuilder("arm_manipulator")
        .robot_description(file_path="config/robot.urdf") # Points to your 3D URDF model geometry
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .to_moveit_configs()
    )

    # Launch your custom planner node wrapped with full access to the robot state parameters
    planner_node = Node(
        package="robotic_arm_path_planning",
        executable="arm_planner_node",
        name="arm_planner_node",
        output="screen",
        parameters=[moveit_config.to_dict()],
    )

    return LaunchDescription([planner_node])
