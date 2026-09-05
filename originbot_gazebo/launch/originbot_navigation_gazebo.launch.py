import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='originbot_gazebo' #<--- CHANGE ME
    pkg_path = os.path.join(get_package_share_directory(package_name))
    navigation_dir = get_package_share_directory('originbot_navigation')

    default_world_path = os.path.join(pkg_path, 'worlds', 'my_map.world')
    default_map_yaml_path = os.path.join(navigation_dir, 'maps', 'my_map.yaml')
    world_path = LaunchConfiguration('world')
    map_yaml_path = LaunchConfiguration('map')
    
    # Pose where we want to spawn the robot
    spawn_x_val = '0.0'
    spawn_y_val = '0.0'
    spawn_z_val = '0.0'
    spawn_yaw_val = '0.0'
  
    originbot = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','originbot.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                launch_arguments={'world': world_path}.items()
             )

    navigation = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    navigation_dir, 'launch', 'nav_bringup_gazebo.launch.py')]),
                launch_arguments={
                    'use_sim_time': 'true',
                    'map': map_yaml_path,
                }.items()
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'originbot',
                                   '-x', spawn_x_val,
                                   '-y', spawn_y_val,
                                   '-z', spawn_z_val,
                                   '-Y', spawn_yaw_val],
                        output='screen')



    # Launch them all!
    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value=default_world_path,
            description='Full path to Gazebo world file to load'),
        DeclareLaunchArgument(
            'map',
            default_value=default_map_yaml_path,
            description='Full path to map yaml file to load in Nav2'),
        originbot,
        gazebo,
        spawn_entity,
        navigation,
    ])
