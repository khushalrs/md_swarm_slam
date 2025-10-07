from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Publishes identity static transforms to patch missing TFs from rosbag2
    return LaunchDescription([
        # World (map) -> drone1/map (spawn at origin)
        # Node(
        #     package='tf2_ros',
        #     executable='static_transform_publisher',
        #     name='static_tf_world_to_drone1_map',
        #     arguments=['0', '0', '0', '0', '0', '0', 'map', 'robot0_map'],
        #     output='screen',
        # ),
        # # World (map) -> drone2/map (spawn at -3, 0, 0)
        # Node(
        #     package='tf2_ros',
        #     executable='static_transform_publisher',
        #     name='static_tf_world_to_drone2_map',
        #     arguments=['-3', '0', '0', '0', '0', '0', 'map', 'robot1_map'],
        #     output='screen',
        # ),
        # drone1: map -> odom (identity)
        # Node(
        #     package='tf2_ros',
        #     executable='static_transform_publisher',
        #     name='static_tf_drone1_map_to_odom',
        #     arguments=['0', '0', '0', '0', '0', '0', 'drone1/map', 'drone1/odom'],
        #     output='screen',
        # ),
        # # drone2: map -> odom (identity)
        # Node(
        #     package='tf2_ros',
        #     executable='static_transform_publisher',
        #     name='static_tf_drone2_map_to_odom',
        #     arguments=['0', '0', '0', '0', '0', '0', 'drone2/map', 'drone2/odom'],
        #     output='screen',
        # ),
        # drone2: camera_link -> x500_depth_mono_1/camera_link/IMX214 (identity)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_tf_drone2_camera_to_imx214',
            arguments=['0', '0', '0', '0', '0', '0', 'drone2/camera_link', 'x500_depth_mono_1/camera_link/IMX214'],
            output='screen',
        ),
    ])
