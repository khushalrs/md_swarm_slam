# from launch import LaunchDescription
# from launch_ros.actions import Node
# from launch.substitutions import LaunchConfiguration
# from launch.actions import DeclareLaunchArgument
# from launch_ros.actions import Node as ROSNode
# from launch_ros.actions import SetParameter
# from launch.conditions import IfCondition
# from ament_index_python.packages import get_package_share_directory
# import os

# def pgo_node(ns, cfg, robot_id):
#     return Node(
#         package='cslam',
#         executable='pose_graph_manager',
#         namespace=ns,
#         name='pose_graph_manager',
#         output='screen',
#         parameters=[cfg, {'robot_id': robot_id}]
#     )

# def map_node(ns, cfg, robot_id):
#     # One map_manager per robot so topics line up per namespace
#     return Node(
#         package='cslam',
#         executable='map_manager',
#         namespace=ns,
#         name='map_manager',
#         output='screen',
#         parameters=[cfg, {'robot_id': robot_id}]
#     )

# def lcd_node(ns, cfg, robot_id, condition=None):
#     # loop-closure detection (often per robot; check your config)
#     return Node(
#         package='cslam',
#         executable='loop_closure_detection_node.py',
#         namespace=ns,
#         name='loop_closure_detection',
#         output='screen',
#         parameters=[cfg, {'robot_id': robot_id}],
#         condition=condition
#     )

# def generate_launch_description():
#     pkg_share = get_package_share_directory('md_swarm_slam')

#     drone1_cfg = DeclareLaunchArgument('drone1_cfg',
#         default_value=os.path.join(pkg_share, 'config', 'drone1_rgbd.yaml'))
#     drone2_cfg = DeclareLaunchArgument('drone2_cfg',
#         default_value=os.path.join(pkg_share, 'config', 'drone2_rgbd.yaml'))
#     global_cfg = DeclareLaunchArgument('global_cfg',
#         default_value=os.path.join(pkg_share, 'config', 'global.yaml'))

#     d1_cfg = LaunchConfiguration('drone1_cfg')
#     d2_cfg = LaunchConfiguration('drone2_cfg')
#     gcfg  = LaunchConfiguration('global_cfg')

#     enable_lcd = DeclareLaunchArgument('enable_lcd', default_value='true')
#     world_frame = DeclareLaunchArgument('world_frame', default_value='map')
#     use_sim_time = DeclareLaunchArgument('use_sim_time', default_value='true')
#     enable_pose_to_tf = DeclareLaunchArgument('enable_pose_to_tf', default_value='true')
#     patch_drone2_camera_tf = DeclareLaunchArgument('patch_drone2_camera_tf', default_value='true')

#     return LaunchDescription([
#         drone1_cfg, drone2_cfg, global_cfg, enable_lcd, world_frame, use_sim_time, enable_pose_to_tf, patch_drone2_camera_tf,
#         # Use simulation time from rosbag /clock for all nodes
#         SetParameter(name='use_sim_time', value=LaunchConfiguration('use_sim_time')),
#         # Robot 1
#         map_node('drone1', d1_cfg, 1),
#         pgo_node('drone1', d1_cfg, 1),
#         lcd_node('drone1', d1_cfg, 1, IfCondition(LaunchConfiguration('enable_lcd'))),
#         # Robot 2
#         map_node('drone2', d2_cfg, 2),
#         pgo_node('drone2', d2_cfg, 2),
#         lcd_node('drone2', d2_cfg, 2, IfCondition(LaunchConfiguration('enable_lcd'))),
#         # Anchor CSLAM world to a chosen global frame (identity)
#         ROSNode(package='tf2_ros', executable='static_transform_publisher',
#                 name='anchor_world_to_robot1_map',
#                 arguments=['0','0','0','0','0','0', LaunchConfiguration('world_frame'), 'robot1_map']),
#         # Bridge current pose estimates to map->odom transforms per robot
#         ROSNode(package='md_swarm_slam', executable='pose_to_tf', name='pose_to_tf_r1',
#                 parameters=[{'world_frame': LaunchConfiguration('world_frame')},
#                             {'odom_frame': 'drone1/odom'},
#                             {'base_frame': 'drone1/base_link'},
#                             {'input_topic': '/r1/cslam/current_pose_estimate'}],
#                 condition=IfCondition(LaunchConfiguration('enable_pose_to_tf'))),
#         ROSNode(package='md_swarm_slam', executable='pose_to_tf', name='pose_to_tf_r2',
#                 parameters=[{'world_frame': LaunchConfiguration('world_frame')},
#                             {'odom_frame': 'drone2/odom'},
#                             {'base_frame': 'drone2/base_link'},
#                             {'input_topic': '/r2/cslam/current_pose_estimate'}],
#                 condition=IfCondition(LaunchConfiguration('enable_pose_to_tf'))),
#         # Patch missing static TF for drone2 camera chain if needed
#         ROSNode(package='tf2_ros', executable='static_transform_publisher',
#                 name='static_tf_drone2_camera_to_imx214',
#                 arguments=['0','0','0','0','0','0','drone2/camera_link','x500_depth_mono_1/camera_link/IMX214'],
#                 condition=IfCondition(LaunchConfiguration('patch_drone2_camera_tf'))),
#     ])


# # import os
# # from ament_index_python.packages import get_package_share_directory
# # from launch import LaunchDescription
# # from launch_ros.actions import Node
# # from launch.substitutions import LaunchConfiguration
# # from launch.actions import DeclareLaunchArgument

# # def cslam_node(ns, cfg_path, robot_id):
# #     return Node(
# #         package='cslam',
# #         executable='cslam_node',
# #         namespace=ns,
# #         name='cslam',
# #         output='screen',
# #         parameters=[cfg_path, {'robot_id': robot_id}],
# #         # If you want to restrict to only needed remaps, add here.
# #     )

# # def generate_launch_description():
# #     pkg_share = get_package_share_directory('md_swarm_slam')

# #     drone1_cfg = DeclareLaunchArgument('drone1_cfg',
# #         default_value=os.path.join(pkg_share, 'config', 'drone1_rgbd.yaml'))
# #     drone2_cfg = DeclareLaunchArgument('drone2_cfg',
# #         default_value=os.path.join(pkg_share, 'config', 'drone2_rgbd.yaml'))

# #     return LaunchDescription([
# #         drone1_cfg, drone2_cfg,
# #         cslam_node('drone1', LaunchConfiguration('drone1_cfg'), 1),
# #         cslam_node('drone2', LaunchConfiguration('drone2_cfg'), 2),
# #     ])


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.actions import Node as ROSNode
from launch_ros.actions import SetParameter
from launch.conditions import IfCondition
from ament_index_python.packages import get_package_share_directory
import os

def pgo_node(ns, cfg, robot_id):
    # Pose-graph backend (one per robot, in its namespace)
    return Node(
        package='cslam',
        executable='pose_graph_manager',
        namespace=ns,
        name='pose_graph_manager',
        output='screen',
        parameters=[cfg, {'robot_id': robot_id}]
    )

def map_node(ns, cfg, robot_id):
    # Map manager (one per robot, in its namespace)
    return Node(
        package='cslam',
        executable='map_manager',
        namespace=ns,
        name='map_manager',
        output='screen',
        parameters=[cfg, {'robot_id': robot_id}]
    )

def lcd_node(ns, cfg, robot_id, condition=None):
    # Appearance-based loop-closure (CosPlace) – optional but recommended for RGB-D multi-robot
    # This executable name matches the upstream Python script; keep it if it already works on your machine.
    return Node(
        package='cslam',
        executable='loop_closure_detection_node.py',
        namespace=ns,
        name='loop_closure_detection',
        output='screen',
        parameters=[cfg, {'robot_id': robot_id}],
        condition=condition
    )

def generate_launch_description():
    pkg_share = get_package_share_directory('md_swarm_slam')

    # Per-robot configs: put your RGB-D + topics/frames + CosPlace checkpoint here
    drone1_cfg = DeclareLaunchArgument(
        'drone1_cfg',
        default_value=os.path.join(pkg_share, 'config', 'drone1_rgbd.yaml')
    )
    drone2_cfg = DeclareLaunchArgument(
        'drone2_cfg',
        default_value=os.path.join(pkg_share, 'config', 'drone2_rgbd.yaml')
    )
    # Global settings (if you have one)
    global_cfg = DeclareLaunchArgument(
        'global_cfg',
        default_value=os.path.join(pkg_share, 'config', 'global.yaml')
    )

    d1_cfg = LaunchConfiguration('drone1_cfg')
    d2_cfg = LaunchConfiguration('drone2_cfg')
    gcfg  = LaunchConfiguration('global_cfg')  # available if some nodes read it

    enable_lcd        = DeclareLaunchArgument('enable_lcd', default_value='true')
    world_frame       = DeclareLaunchArgument('world_frame', default_value='map')
    use_sim_time      = DeclareLaunchArgument('use_sim_time', default_value='true')
    enable_pose_to_tf = DeclareLaunchArgument('enable_pose_to_tf', default_value='true')

    return LaunchDescription([
        drone1_cfg, drone2_cfg, global_cfg,
        enable_lcd, world_frame, use_sim_time, enable_pose_to_tf,

        # Make all nodes use /clock from rosbag
        SetParameter(name='use_sim_time', value=LaunchConfiguration('use_sim_time')),

        # ---------------- Robot 1 (robot_id = 0) ----------------
        map_node('drone1', d1_cfg, 0),
        pgo_node('drone1', d1_cfg, 0),
        lcd_node('drone1', d1_cfg, 0, IfCondition(LaunchConfiguration('enable_lcd'))),

        # Convert Swarm-SLAM pose to TF map->odom for R1
        # Subscribes to /drone1/cslam/current_pose_estimate (topic inside the namespace)
        ROSNode(
            package='md_swarm_slam', executable='pose_to_tf', name='pose_to_tf_r1',
            parameters=[{'odom_frame':'drone1/odom'},{'base_frame':'drone1/base_link'}],
            namespace='drone1'),

        # ---------------- Robot 2 (robot_id = 1) ----------------
        map_node('drone2', d2_cfg, 1),
        pgo_node('drone2', d2_cfg, 1),
        lcd_node('drone2', d2_cfg, 1, IfCondition(LaunchConfiguration('enable_lcd'))),

        # Convert Swarm-SLAM pose to TF map->odom for R2
        ROSNode(
            package='md_swarm_slam', executable='pose_to_tf', name='pose_to_tf_r2',
            parameters=[{'odom_frame':'drone2/odom'},{'base_frame':'drone2/base_link'}],
            namespace='drone2'),

        # NOTE:
        # We do NOT publish any static TF "world -> robot1_map". The map frame is global/shared and
        # produced/optimized by Swarm-SLAM; anchoring it manually often causes frame conflicts.
    ])
