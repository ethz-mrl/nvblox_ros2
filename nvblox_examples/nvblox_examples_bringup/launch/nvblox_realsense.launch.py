# SPDX-FileCopyrightText: NVIDIA CORPORATION & AFFILIATES
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

NVBLOX_EXAMPLES_SHARE = get_package_share_directory('nvblox_examples_bringup')
NVBLOX_BASE_CONFIG = os.path.join(
    NVBLOX_EXAMPLES_SHARE, 'config', 'nvblox', 'nvblox_base.yaml')
NVBLOX_REALSENSE_CONFIG = os.path.join(
    NVBLOX_EXAMPLES_SHARE, 'config', 'nvblox', 'specializations', 'nvblox_humanoid.yaml')
DEFAULT_CONTAINER_NAME = 'nvblox_container'
RS_EMITTER_ON_CONFIG_FILE_PATH = os.path.join(
    NVBLOX_EXAMPLES_SHARE, 'config', 'sensors', 'realsense_emitter_on.yaml')


def generate_launch_description() -> LaunchDescription:
    log_level = LaunchConfiguration('log_level')
    container_name = LaunchConfiguration('container_name')
    camera_namespace = LaunchConfiguration('camera_namespace') 
    camera_name = LaunchConfiguration('camera_name') 

    nvblox_node = ComposableNode(
        name='nvblox_node',
        package='nvblox_ros',
        plugin='nvblox::NvbloxNode',
        remappings=[
            ('camera_0/color/camera_info', [camera_namespace, camera_name, '/color/camera_info']),
            ('camera_0/color/image', [camera_namespace, camera_name, '/color/image_raw']),
            ('camera_0/depth/camera_info', [camera_namespace, camera_name, '/depth/camera_info']),
            ('camera_0/depth/image', [camera_namespace, camera_name, '/depth/image_rect_raw']),
        ],
        parameters=[
            NVBLOX_BASE_CONFIG,
            NVBLOX_REALSENSE_CONFIG,
        ],
    )
    
    realsense_node = ComposableNode(
        name=camera_name,
        namespace=camera_namespace, 
        package='realsense2_camera',
        plugin='realsense2_camera::RealSenseNodeFactory',
        parameters = [
            RS_EMITTER_ON_CONFIG_FILE_PATH,
            {'camera_name': camera_name}
        ],
        condition=UnlessCondition(LaunchConfiguration('standalone')),
    )
    
    container = ComposableNodeContainer(
        name=container_name,
        namespace='',
        package='rclcpp_components',
        executable='component_container_mt',
        composable_node_descriptions=[
            nvblox_node,
            realsense_node,
        ],
        output='screen',
        arguments=['--ros-args', '--log-level', log_level],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'log_level', default_value='info',
            description='Logging level for the component container.'),
        DeclareLaunchArgument(
            'container_name', default_value=DEFAULT_CONTAINER_NAME,
            description='Name of the component container to start.'),
        DeclareLaunchArgument(
            'standalone', default_value='false',
            description='Whether to launch nvblox standalone or to also launch the realsense camera node.'),
        DeclareLaunchArgument(
            'camera_namespace', default_value='/camera/',
            description='Namespace of the RealSense camera to use.'),
        DeclareLaunchArgument(
            'camera_name', default_value='d435',
            description='Prefix used for fully-qualified RealSense topics.'),
        container,
    ])