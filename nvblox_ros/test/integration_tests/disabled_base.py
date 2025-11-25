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

"""Lightweight stub replacing the removed Isaac ROS test base class."""

import functools


class IsaacROSBaseTest:  # pylint: disable=too-few-public-methods
    """Placeholder to keep legacy tests importable without isaac_ros_test."""

    @staticmethod
    def generate_test_description(_actions):
        raise RuntimeError(
            'Isaac ROS integration tests are disabled (external harness removed).')

    @staticmethod
    def generate_test_description_wrapper(_actions):
        raise RuntimeError(
            'Isaac ROS integration tests are disabled (external harness removed).')

    @staticmethod
    def generate_namespace(prefix):
        return prefix

    @staticmethod
    def for_each_test_case(*_args, **_kwargs):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*__args, **__kwargs):
                raise RuntimeError(
                    'Isaac ROS integration tests are disabled (external harness removed).')
            return wrapper
        return decorator
