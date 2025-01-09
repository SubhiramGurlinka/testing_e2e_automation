# This py file contains the function to get the details and data about the docker
import subprocess
import json

def get_docker_images():
    """
    Returns a list of all locally available Docker images.

    Returns:
        List[dict]: A list of dictionaries, each containing details about a Docker image.
    """
    # Run the 'docker images' command with JSON format
    result = subprocess.run(
        ["docker", "images", "--format", "{{json .}}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"Error: {result.stderr.strip()}")
    # Parse the output
    images = []
    image_names = []
    for line in result.stdout.strip().split("\n"):
        if line:
            line_json = json.loads(line)
            image_names.append(f"{line_json['Repository']}:{line_json['Tag']}") 
    return image_names

def get_all_docker_containers():
    """
    Returns a list of names of all Docker containers (running or stopped).

    Returns:
        List[str]: A list of names of all Docker containers.
    """
        # Run the 'docker ps -a' command to get details of all containers
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"Error: {result.stderr.strip()}")

    # Split the output into lines and return as a list
    container_names = result.stdout.strip().split("\n") if result.stdout.strip() else []
    return container_names

def check_docker_image_exists(image_name):
    """
    Checks if a Docker image with the specified name exists locally.

    Args:
        image_name (str): The name of the Docker image (e.g., "nginx:latest").

    Returns:
        bool: True if the image exists, False otherwise.
    """
    # Get the list of all local Docker images
    local_images = get_docker_images()

    # Check if the specified image exists in the list
    if image_name in local_images:
        return True
    else:
        return False

def check_docker_container_exists(container_name):
    """
    Checks if a Docker container with the specified name exists locally.

    Args:
        container_name (str): The name of the Docker image (e.g., "nginx:latest").

    Returns:
        bool: True if the container exists, False otherwise.
    """
    # Get the list of all local Docker images
    local_containers = get_all_docker_containers()
    # Check if the specified image exists in the list
    if container_name in local_containers:
        return True
    else:
        return False
