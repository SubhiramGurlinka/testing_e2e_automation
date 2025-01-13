# Ubuntu 20.04 Dockerfile
FROM ubuntu:20.04

# Install curl to download the script
#RUN apt-get install -y curl
RUN apt-get update && apt-get install -y curl wget

WORKDIR /tmp
# Download the install_mongodb_common.sh from the provided URL
RUN curl -o install_mongodb_common.sh https://raw.githubusercontent.com/SubhiramGurlinka/bigfix_scripts/refs/heads/main/common_installation_bash_scripts/install_mongodb_common.sh

# Make sure the script is executable
RUN chmod +x install_mongodb_common.sh

# Run the script with arguments for RHEL 9 and MongoDB version 7.0.5
RUN bash install_mongodb_common.sh ubuntu focal 7.0.5

# clear the files
WORKDIR /
RUN rm -rf /tmp/*

# Set the default command
CMD ["echo", "MongoDB installation completed successfully!"]