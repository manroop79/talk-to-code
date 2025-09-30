#!/bin/bash
cd ./docker

# Config
PORT=8501
DOCKER_IMAGE_NAME="trustworthy_llm_demo"
DOCKER_CONTAINER_NAME="twllm_demo"

# Get user and location information automatically
repo_root=$(dirname `pwd`)
uid=$(id -u ${USER})
gid=$(id -g ${USER})

# Build Docker
docker build -t $DOCKER_IMAGE_NAME .

# Run the docker container, forwarding the given PORT, and mounting the main repository under /app.
docker run -it --rm --name $DOCKER_CONTAINER_NAME -p $PORT:$PORT -v $repo_root:/app --env PORT=$PORT $DOCKER_IMAGE_NAME /bin/bash