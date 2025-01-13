"""
This script will stop and remove all the containers that were created by the e2e python scripts
The docker containers that have _e2e at the end of their names will be stopped and removed

"""
import subprocess
import os
import sys
import docker
from docker_details import get_all_docker_containers

client = docker.from_env()

# get the list of all the containers
all_container_list = get_all_docker_containers()

# add the e2e containers from the all containers to the e2e_containers list
e2e_containers = [name for name in all_container_list if name.endswith('_e2e')]

# Loop through the container names
for container_name in e2e_containers:
    try:
        # Get the container by name
        container = client.containers.get(container_name)

        # Stop the container
        print(f"Stopping container: {container_name}")
        container.stop()

        # Remove the container
        print(f"Removing container: {container_name}")
        container.remove()

    except docker.errors.NotFound:
        print(f"Container {container_name} not found.")
    except Exception as e:
        print(f"Error with container {container_name}: {str(e)}")

print("Process completed.")

