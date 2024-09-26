#!/bin/bash

if [ "$(docker ps -q -f name=pastebin_container)" ]; then
    echo "Stopping and removing existing container..."
    docker stop pastebin_container
    docker rm pastebin_container
fi

echo "Building Docker image..."
docker build -t pastebin_app .

echo "Running Docker container..."
docker run -d -p 5000:5000 --name pastebin_container pastebin_app

echo "Docker container is up and running."