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
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

NVBLOX_EXAMPLES_SHARE = get_package_share_directory('nvblox_examples_bringup')
NVBLOX_BASE_CONFIG = os.path.join(
    NVBLOX_EXAMPLES_SHARE, 'config', 'nvblox', 'nvblox_base.yaml')
NVBLOX_REALSENSE_CONFIG = os.path.join(
    NVBLOX_EXAMPLES_SHARE, 'config', 'nvblox', 'specializations', 'nvblox_realsense.yaml')
DEFAULT_CONTAINER_NAME = 'nvblox_container'


def generate_launch_description() -> LaunchDescription:
    log_level = LaunchConfiguration('log_level')
    container_name = LaunchConfiguration('container_name')
    camera_prefix = LaunchConfiguration('camera_prefix')

    nvblox_node = ComposableNode(
        name='nvblox_node',
        package='nvblox_ros',
        plugin='nvblox::NvbloxNode',
        remappings=[
            ('camera_0/color/camera_info', [camera_prefix, '/color/camera_info']),
            ('camera_0/color/image', [camera_prefix, '/color/image_raw']),
            ('camera_0/depth/camera_info', [camera_prefix, '/depth/camera_info']),
            ('camera_0/depth/image', [camera_prefix, '/depth/image_rect_raw']),
        ],
        parameters=[
            NVBLOX_BASE_CONFIG,
            NVBLOX_REALSENSE_CONFIG,
            {'num_cameras': 1},
            {'use_lidar': False},
        ],
    )

    container = ComposableNodeContainer(
        name=container_name,
        namespace='',
        package='rclcpp_components',
        executable='component_container_mt',
        composable_node_descriptions=[
            nvblox_node,
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
            'camera_namespace', default_value='camera/d435',
            description='Namespace of the RealSense camera to use.'),
        DeclareLaunchArgument(
            'camera_prefix', default_value='/camera/d435',
            description='Prefix used for fully-qualified RealSense topics.'),
        container,
    ])
