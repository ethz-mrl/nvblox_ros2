# https://hub.docker.com/r/dustynv/ros/tags
# https://github.com/dusty-nv/jetson-containers/tree/master/packages/robots/ros
#FROM dustynv/ros:jazzy-desktop-r36.4.0-cu128-24.04

FROM nvidia/cuda:12.6.0-devel-ubuntu24.04


ARG ROS_WS=/root/ros_ws
ENV ROS_WS=${ROS_WS}
ENV ROS_WS_SRC=${ROS_WS}/src

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-ic"]

RUN apt-get update && apt-get install -y curl

# Add ROS 2 apt repository
RUN --mount=type=cache,target=/var/cache/apt \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null \
    && apt-get update

# TZData goes first.
RUN apt-get update
ENV TZ Europe/Berlin
ENV DEBIAN_FRONTEND noninteractive
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y tzdata

# Install basics.
RUN apt-get update && apt-get install -y ssh  git jq gnupg apt-utils software-properties-common build-essential python3-pip sudo python3-venv unzip

# Install dependencies.
RUN apt-get update && apt-get install -y libgoogle-glog-dev libgtest-dev libbenchmark-dev curl libsqlite3-dev

# Setup env variables by adding them to the global bashrc.
RUN touch /etc/nvblox_env.sh
RUN echo 'PATH=$PATH:/usr/local/cuda/bin' | tee --append /etc/nvblox_env.sh && \
    echo 'export CUDA_PATH=/usr/local/cuda' | tee --append /etc/nvblox_env.sh
RUN echo 'source /etc/nvblox_env.sh' | tee --append /etc/bash.bashrc


# Install all of ROS, thanks GPT!
# Install ROS 2 Jazzy base (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-ros-base ros-jazzy-cv-bridge ros-jazzy-rviz2 ros-jazzy-rviz-common \
    && rm -rf /var/lib/apt/lists/*

# Environment setup
# Source ROS in any new bash shell
RUN echo "source /opt/ros/jazzy/setup.bash" >> /etc/bash.bashrc
ENV ROS_DISTRO=jazzy

# (Optional but usually needed) Colcon & dev tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions \
    python3-rosdep \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# rosdep init (safe in container; if it exists it will just warn)
RUN rosdep init 2>/dev/null || true && \
    rosdep update


# mkdir -p /workspaces/nvblox/build
# cd /workspaces/nvblox/build
# cmake .. -DBUILD_PYTORCH_WRAPPER=0
# make -j${nproc}