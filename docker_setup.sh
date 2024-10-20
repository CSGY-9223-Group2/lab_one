#!/bin/bash

if ! docker network ls | grep -q pastebin_iso_network; then
    echo "Creating pastebin isolated Docker Network..."
    docker network create pastebin_iso_network
else
    echo "Docker network 'pastebin_iso_network' already exists."
fi


if [ "$(docker ps -a -q -f name=pastebin_container)" ]; then
    echo "Stopping and removing existing container..."
    docker stop pastebin_container
    docker rm pastebin_container
fi

echo "Building Docker image..."
docker build -t pastebin_app .

echo "Running Docker container..."
docker run -d -p 5000:5000 \
    --network=pastebin_iso_network \
    --read-only \
    --tmpfs /app/instance \
    --security-opt=no-new-privileges \
    --cap-drop=ALL \
    --cap-add=NET_BIND_SERVICE \
    --name pastebin_container \
    pastebin_app

echo "Docker container is up and running."

docker network connect bridge pastebin_container
