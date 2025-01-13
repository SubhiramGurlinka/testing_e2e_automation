# RHEL 7 Dockerfile
FROM oraclelinux:7

# Install curl to download the script
#RUN yum install -y curl

# Download the install_mongodb_common.sh from the provided URL
RUN curl -o /tmp/install_mongodb_common.sh https://raw.githubusercontent.com/SubhiramGurlinka/bigfix_scripts/refs/heads/main/common_installation_bash_scripts/install_mongodb_common.sh

# Make sure the script is executable
RUN chmod +x /tmp/install_mongodb_common.sh

# Run the script with arguments for RHEL 7 and MongoDB version 7.0.5
RUN bash /tmp/install_mongodb_common.sh rhel 7 7.0.5

# clear the files
WORKDIR /
RUN rm -rf /tmp/*

# Set the default command
CMD ["echo", "MongoDB installation completed successfully!"]