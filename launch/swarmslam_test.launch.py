from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import PushRosNamespace
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import ThisLaunchFileDir

def one_robot(ns, robot_id, rgb, depth, info, odom, base_link, camera_link):
    # include the official RGB-D experiment launch and remap inputs to your bag topics
    exp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            get_package_share_directory('cslam_experiments') + '/launch/robot_experiments/experiment_realsense.launch.py'
        ),
        launch_arguments={
            'robot_id': str(robot_id),
            'use_sim_time': 'true'
        }.items()
    )
    return GroupAction([
        PushRosNamespace(ns.strip('/')),
        # Remap the topics that Swarm-SLAM’s RGB-D pipeline subscribes to:
        # (these names are the *generic* inputs used inside the experiment launch)
        SetEnvironmentVariable(name='ROS_ARGUMENTS', value=
            f'--ros-args'
            f' -r rgb:={rgb}'
            f' -r depth:={depth}'
            f' -r camera_info:={info}'
            f' -r odom:={odom}'
            f' -r base_link:={base_link}'
            f' -r camera_link:={camera_link}'
        ),
        exp
    ])

def generate_launch_description():
    r1 = one_robot('/drone1', 0,
                   '/drone1/rgb_camera', '/drone1/depth_camera', '/drone1/camera_info',
                   '/drone1/odom', '/drone1/base_link', '/drone1/camera_link')
    r2 = one_robot('/drone2', 1,
                   '/drone2/rgb_camera', '/drone2/depth_camera', '/drone2/camera_info',
                   '/drone2/odom', '/drone2/base_link', '/drone2/camera_link')
    return LaunchDescription([r1, r2])
