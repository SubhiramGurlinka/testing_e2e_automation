import docker

def is_bes_client_installed(container_name):
    try:
        # Initialize Docker client
        client = docker.from_env()
        
        # Get the container by name
        container = client.containers.get(container_name)
        
        # Use `bash -c` to run the command
        result = container.exec_run("bash -c 'test -f /opt/BESClient/bin/BESClient && echo exists'")

        if result.exit_code == 0 and b"exists" in result.output:
            #print(f"BES Client is installed in the container '{container_name}'.")
            return True
        else:
            print(f"BES Client is not installed in the container '{container_name}'.")
            return False
    except docker.errors.NotFound:
        print(f"Container '{container_name}' not found.")
    except docker.errors.APIError as e:
        print(f"Error interacting with Docker: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False

def is_bes_client_running(container_name):
    try:
        # Initialize Docker client
        client = docker.from_env()
        
        # Get the container by name
        container = client.containers.get(container_name)
        
        # Check if the BESClient process is running in the container
        result = container.exec_run("pgrep -f BESClient")
        if result.exit_code == 0:
            #print(f"BES Client is running in the container '{container_name}'.")
            return True
        else:
            print(f"BES Client is not running in the container '{container_name}'.")
            return False
    except docker.errors.NotFound:
        print(f"Container '{container_name}' not found.")
    except docker.errors.APIError as e:
        print(f"Error interacting with Docker: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False

def verify_bes_client_in_container(container_name):
    if not is_bes_client_installed(container_name):
        print("Verification failed: BES Client is not installed.")
        return False
    if not is_bes_client_running(container_name):
        print("Verification failed: BES Client is not running.")
        return False
    #print("BES Client is properly installed and running in the container.")
    return True
