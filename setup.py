from setuptools import find_packages, setup

package_name = 'md_swarm_slam'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name + '/launch', ['launch/swarmslam_two_rgbd.launch.py', 
        'launch/patch_static_transforms.launch.py',
        'launch/swarmslam_test.launch.py',
        'launch/rtabmap_slam.launch.py']),
        ('share/' + package_name + '/config', ['config/drone1_rgbd.yaml',
                                               'config/drone2_rgbd.yaml',
        'config/global.yaml']),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='frazergene',
    maintainer_email='khushalrs@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pose_to_tf = md_swarm_slam.pose_to_tf:main',
        ],
    },
)
