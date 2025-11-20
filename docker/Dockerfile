ARG ARCH=aarch64

## --- AARCH Stage ---
FROM dustynv/ros:jazzy-desktop-r36.4.0-cu128-24.04 AS aarch64

SHELL ["/bin/bash", "-ic"]
ENV DEBIAN_FRONTEND=noninteractive

# Add ROS 2 apt repository
RUN --mount=type=cache,target=/var/cache/apt \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null && \
    apt-get update

# TZData
ENV TZ Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN --mount=type=cache,target=/var/cache/apt apt-get install -y --no-install-recommends tzdata

# Source ROS in any new bash shell, note that it is built from source in this image
RUN echo "source /opt/ros/jazzy/install/setup.bash" >> /etc/bash.bashrc

# Install realsense2_camera from source using dusty's convenience script
RUN /ros2_install.sh realsense2_camera

## --- X86 Stage ---
FROM nvidia/cuda:12.6.0-devel-ubuntu24.04 AS x86_64

SHELL ["/bin/bash", "-ic"]
ENV DEBIAN_FRONTEND=noninteractive

# Add ROS 2 apt repository
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends curl && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null && \
    apt-get update

# TZData
ENV TZ Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN --mount=type=cache,target=/var/cache/apt apt-get install -y --no-install-recommends tzdata

# Install ROS 2 Jazzy base (minimal)
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get install -y --no-install-recommends \
    ros-jazzy-ros-base \
    ros-jazzy-cv-bridge \ 
    ros-jazzy-rviz2 \
    ros-jazzy-rviz-common \
    ros-jazzy-rmw-cyclonedds-cpp \
    ros-jazzy-realsense2-camera

# Source ROS in any new bash shell
RUN echo "source /opt/ros/jazzy/setup.bash" >> /etc/bash.bashrc

## --- FINAL Stage with common dependencies ---
ARG ARCH
FROM ${ARCH} AS final

# Install basics.
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
    ssh \
    git \
    jq \
    gnupg \
    apt-utils \
    software-properties-common \
    build-essential \
    python3-pip \
    sudo \
    python3-venv \
    unzip

# Install dependencies.
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get install -y --no-install-recommends \ 
    libgoogle-glog-dev \
    libgtest-dev \
    libbenchmark-dev \
    libsqlite3-dev

# Setup env variables by adding them to the global bashrc.
RUN touch /etc/nvblox_env.sh
RUN echo 'PATH=$PATH:/usr/local/cuda/bin' | tee --append /etc/nvblox_env.sh && \
    echo 'export CUDA_PATH=/usr/local/cuda' | tee --append /etc/nvblox_env.sh
RUN echo 'source /etc/nvblox_env.sh' | tee --append /etc/bash.bashrc
    
# (Optional but usually needed) Colcon & dev tools
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions \
    python3-rosdep \
    && rm -rf /var/lib/apt/lists/*

# rosdep init (safe in container; if it exists it will just warn)
RUN rosdep init 2>/dev/null || true && \
    rosdep update