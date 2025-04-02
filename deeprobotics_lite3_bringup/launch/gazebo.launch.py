import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

os.environ['LIBGL_ALWAYS_INDIRECT'] = '1'

# export GAZEBO_MODEL_PATH=/home/robert/ROS/deep_ws/build
# export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:/home/robert/ROS/deep_ws/build/

def generate_launch_description():

    description_pkg_share_dir = get_package_share_directory('deeprobotics_lite3_description')

    xacro_file = os.path.join(description_pkg_share_dir, 'urdf', 'robot.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_urdf = robot_description_config.toxml()

    rviz_config_file = os.path.join(description_pkg_share_dir, 'rviz', 'display.rviz')

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'robot_description': robot_urdf}
        ]
    )

    gazebo_sim_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py"
            ])
        ]),
        launch_arguments={
            "gz_args": PathJoinSubstitution([
                get_package_share_directory("deeprobotics_lite3_bringup"),
                "worlds",
                "tugbot_warehouse.sdf"
            ]).perform({}) + " -r"
        }.items()
    )

    gazebo_sim_create_node = Node(
        package="ros_gz_sim",
        executable="create",
        name='spawn_lite3_robot',
        arguments=[
            "-z", "0.5",
            "-topic", "robot_description",
        ]
    )

    gazebo_bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[{
            # "config_file": gazebo_config_path
        }]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        gazebo_sim_node,
        gazebo_sim_create_node,
        gazebo_bridge_node,
        #rviz_node
    ])
