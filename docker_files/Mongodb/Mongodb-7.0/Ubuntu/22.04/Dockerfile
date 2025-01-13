# Ubuntu 22.04 Dockerfile
FROM ubuntu:22.04

# Install curl to download the script
RUN apt-get update && apt-get install -y curl wget

# Download the install_mongodb_common.sh from the provided URL
RUN curl -o /usr/local/bin/install_mongodb_common.sh https://raw.githubusercontent.com/SubhiramGurlinka/bigfix_scripts/refs/heads/main/common_installation_bash_scripts/install_mongodb_common.sh

# Make sure the script is executable
RUN chmod +x /usr/local/bin/install_mongodb_common.sh

# Run the script with arguments for Ubuntu 22.04 (jammy) and MongoDB version 7.0.5
RUN bash /usr/local/bin/install_mongodb_common.sh ubuntu jammy 7.0.5

# clear the files
WORKDIR /
RUN rm -rf /tmp/*