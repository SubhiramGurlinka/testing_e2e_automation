# Ubuntu 20.04 Dockerfile
FROM ubuntu:22.04

# Install curl to download the script
RUN apt-get update
RUN apt-get install -y curl wget

WORKDIR /usr/local/bin/

RUN wget https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/8.0/multiverse/binary-amd64/mongodb-database-tools_100.10.0_amd64.deb

RUN wget https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/8.0/multiverse/binary-amd64/mongodb-mongosh_2.3.1_amd64.deb

RUN dpkg -i mongodb-mongosh_2.3.1_amd64.deb

RUN dpkg -i mongodb-database-tools_100.10.0_amd64.deb

# Download the install_mongodb_common.sh from the provided URL
RUN curl -o /usr/local/bin/install_mongodb_common.sh https://raw.githubusercontent.com/SubhiramGurlinka/testing_automation/refs/heads/main/fixlet_testing/bash%20scripts/install_mongodb_common.sh

# Make sure the script is executable
RUN chmod +x /usr/local/bin/install_mongodb_common.sh

# Run the script with arguments for RHEL 9 and MongoDB version 7.0.5
RUN bash /usr/local/bin/install_mongodb_common.sh ubuntu jammy 8.0.1

# clear the files
WORKDIR /
RUN rm -rf /tmp/*

# Set the default command
CMD ["echo", "MongoDB installation completed successfully!"]