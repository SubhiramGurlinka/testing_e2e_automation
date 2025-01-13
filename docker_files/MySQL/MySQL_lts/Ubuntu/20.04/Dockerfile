# Dockerfile for Ubuntu 20.04/22.04

# Choose the correct base image for Ubuntu
FROM ubuntu:20.04

# Set environment variables
ARG MYSQL_VERSION=8.0.37
ARG OS_VERSION=20.04

# Disable interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y curl wget
# Copy MySQL files to the container
WORKDIR /tmp
RUN wget https://downloads.mysql.com/archives/get/p/23/file/mysql-server_${MYSQL_VERSION}-1ubuntu${OS_VERSION}_amd64.deb-bundle.tar
# COPY mysql-server_${MYSQL_VERSION}-1ubuntu${OS_VERSION}_amd64.deb-bundle.tar /tmp/

# Install required packages
RUN apt-get update && \
    apt-get install -y sudo unzip perl libaio1 libmecab2 libnuma1 psmisc libmysqlclient-dev libjson-perl mecab-ipadic-utf8 libsasl2-2 libgssapi-krb5-2 libkrb5-3 && \
    tar -xvf /tmp/mysql-server_${MYSQL_VERSION}-1ubuntu${OS_VERSION}_amd64.deb-bundle.tar -C /tmp/ && \
    apt install -y /tmp/mysql*.deb && \
    dpkg --configure -a && \
    rm -f /tmp/mysql-server_${MYSQL_VERSION}-1ubuntu${OS_VERSION}_amd64.deb-bundle.tar
# clear the files
WORKDIR /
RUN rm -rf /tmp/*
CMD ["echo", "Mysql installation completed successfully!"]
