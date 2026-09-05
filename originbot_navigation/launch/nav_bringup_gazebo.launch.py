#!/usr/bin/python3

# Copyright (c) 2022, www.guyuehome.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue



def generate_launch_description():
    navigation2_dir = get_package_share_directory('originbot_navigation')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    default_map_yaml_path = os.path.join(navigation2_dir,'maps','my_map.yaml')
    default_nav2_param_path = os.path.join(navigation2_dir,'param','originbot_nav2.yaml')
    default_rviz_config_path = os.path.join(navigation2_dir,'rviz','navigation.rviz')
    rviz_config_path = LaunchConfiguration('rvizconfig', default=default_rviz_config_path)
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    use_sim_time_bool = ParameterValue(use_sim_time, value_type=bool)
    map_yaml_path = LaunchConfiguration('map', default=default_map_yaml_path)
    nav2_param_path = LaunchConfiguration('params_file', default=default_nav2_param_path)
    use_composition = LaunchConfiguration('use_composition', default='False')
    slam = LaunchConfiguration('slam', default='False')  
    # slam = LaunchConfiguration('slam', default='True')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time',default_value='true',description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument('map',default_value=default_map_yaml_path,description='Full path to map file to load'),
        DeclareLaunchArgument('params_file',default_value=default_nav2_param_path,description='Full path to param file to load'),
        DeclareLaunchArgument('use_composition',default_value='False',description='Use composed bringup if true'),
        DeclareLaunchArgument('rvizconfig',default_value=default_rviz_config_path,description='Full path to rviz config file'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_bringup_dir,'/launch','/bringup_launch.py']),
            launch_arguments={
                'map': map_yaml_path,
                'use_sim_time': use_sim_time,
                'params_file': nav2_param_path,
                'use_composition': use_composition,
                'slam': slam,}.items(),
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_path, '--ros-args', '-p', 'use_sim_time:=true'],
            parameters=[{'use_sim_time': use_sim_time_bool}],
            output='screen'),
    ])
