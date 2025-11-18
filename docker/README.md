# nvblox on Jetson Orin NX (Dockerized Setup)

This guide explains how to build and run **nvblox** inside a Docker container on a **Jetson Orin NX**.
The docker container includes ROS Jazzy and Cuda 12.8.

## 1. Clone the Repository

    git clone https://github.com/nvidia-isaac/nvblox.git

## 2. Launch the Docker Environment

    cd nvblox/docker
    docker compose up --build -d --remove-orphans --force-restart

Attach to the running container:

    docker exec -it <container_name> bash

## 3. Build nvblox Inside the Container

    mkdir -p /workspaces/nvblox/build
    cd /workspaces/nvblox/build
    cmake .. -DBUILD_PYTORCH_WRAPPER=0
    make -j"${nproc}"