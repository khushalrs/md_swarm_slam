from launch import LaunchDescription
from launch.actions import GroupAction
from launch_ros.actions import Node, PushRosNamespace
from datetime import datetime


def rgbd_pipeline(ns: str, odom_topic: str, run_ts: str):
    """
    One RGB-D + RTAB-Map pipeline under namespace `ns`.
    Expects:
      /<ns>/rgb_camera       (sensor_msgs/Image)
      /<ns>/depth_camera     (sensor_msgs/Image)
      /<ns>/camera_info      (sensor_msgs/CameraInfo)
      odom_topic (nav_msgs/Odometry), e.g. /drone1/local_position/odom
    Publishes TF:
      <ns>/map -> <ns>/odom   (rtabmap)
      (Note: odom -> base_link should be provided by your odometry source;
             do NOT publish odom->base_link as a static TF.)
    """
    return GroupAction([
        PushRosNamespace(ns),

        # Pack RGB + Depth + Info into /<ns>/rgbd_image
        Node(
            package='rtabmap_sync',
            executable='rgbd_sync',
            name='rgbd_sync',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'approx_sync': True,
                'approx_sync_max_interval': 0.05,
                'qos_image': 'sensor_data',        # match camera publishers
                'qos_camera_info': 'sensor_data',
                'queue_size': 100,
            }],
            remappings=[
                ('rgb/image',        f'/{ns}/rgb_camera'),
                ('depth/image',      f'/{ns}/depth_camera'),
                ('rgb/camera_info',  f'/{ns}/camera_info'),
                ('rgbd_image',       'rgbd_image'),  # output, stays under ns
            ],
        ),

        # RTAB-Map SLAM (consumes rgbd_image + external odom)
        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            output='screen',
            arguments=['--delete_db_on_start'],
            parameters=[{
                'use_sim_time': True,

                # Frames (namespaced)
                'frame_id':      f'{ns}/base_link',
                'odom_frame_id': f'{ns}/odom',
                'map_frame_id':  f'{ns}/map',
                'publish_tf':    True,  # publishes <ns>/map -> <ns>/odom

                'database_path': f'/home/frazergene/drone/drone_ws/src/md_swarm_slam/resource/{ns}_rtabmap_{run_ts}.db',

                # We’re feeding a packed RGB-D image
                'subscribe_depth': False,
                'subscribe_rgbd':  True,
                'topic_queue_size': 30,   # rtabmap’s per-topic queue
                'sync_queue_size': 100,   # rtabmap’s internal sync buffer
                'qos_image': 'sensor_data',
                'qos_camera_info': 'sensor_data',
                'qos_odom': 'sensor_data',

                'approx_sync': True,
                'approx_sync_max_interval': 0.05,
                'queue_size': 30,

                # Same triggers as your ROS1 snippet (optional)
                'RGBD/AngularUpdate':        '0.01',
                'RGBD/LinearUpdate':         '0.01',
                'RGBD/OptimizeFromGraphEnd': 'false',
            }],
            remappings=[
                # External odometry topic from PX4/GZ
                ('odom',        odom_topic),         # e.g. /drone1/local_position/odom
                ('rgbd_image',  'rgbd_image'),
            ],
        ),
    ])

def generate_launch_description():
    run_ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    return LaunchDescription([
        Node(
            package='md_swarm_slam', executable='pose_to_tf', name='pose_to_tf_r2',
            parameters=[{'odom_frame':'drone2/odom'},{'base_frame':'drone2/base_link'}],
            namespace='drone2'),
        Node(
            package='md_swarm_slam', executable='pose_to_tf', name='pose_to_tf_r2',
            parameters=[{'odom_frame':'drone2/odom'},{'base_frame':'drone2/base_link'}],
            namespace='drone2'),
        rgbd_pipeline('drone1', '/drone1/local_position/odom', run_ts),
        rgbd_pipeline('drone2', '/drone2/local_position/odom', run_ts),
    ])
