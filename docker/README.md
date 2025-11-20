# nvblox on Jetson Orin NX (Dockerized Setup)

This guide explains how to build and run **nvblox** inside a Docker container on a **Jetson Orin NX**.
The docker container includes ROS Jazzy and Cuda 12.8.

## 1. Clone the Repository
```bash
mkdir -p nvblox_ros2_ws/src
cd nvblox_ros2_ws/src
git clone --recursive https://github.com/ethz-mrl/nvblox_ros2.git
```
## 2. Launch the Docker Environment
```bash
cd nvblox_ros2/docker
export NVBLOX_ARCH=$(uname -m)
docker compose up --build -d
```
Attach to the running container:
```bash
docker exec -it <container_name> bash
```
## 3. Build nvblox Inside the Container
```bash
cd /workspaces/nvblox
colcon build --symlink-install
```
