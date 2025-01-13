# Dockerfile for RHEL 7/8/9

# Choose the correct base image for RHEL
FROM oraclelinux:7

# Set environment variables
ARG MYSQL_VERSION=8.4.0
ARG OS_VERSION=7
RUN yum install wget -y
# Copy MySQL files to the container
WORKDIR /tmp
RUN wget https://downloads.mysql.com/archives/get/p/23/file/mysql-${MYSQL_VERSION}-1.el${OS_VERSION}.x86_64.rpm-bundle.tar
#COPY mysql-${MYSQL_VERSION}-1.el${OS_VERSION}.x86_64.rpm-bundle.tar /tmp/

# Install required packages
RUN yum install -y sudo unzip perl libaio numactl net-tools openssl-devel openssl-libs libtirpc libcrypto.so.1.1 perl-JSON && \
    tar -xvf /tmp/mysql-${MYSQL_VERSION}-1.el${OS_VERSION}.x86_64.rpm-bundle.tar -C /tmp/ && \
    yum install -y /tmp/mysql-*.rpm && \
    rm -f /tmp/mysql-${MYSQL_VERSION}-1.el${OS_VERSION}.x86_64.rpm-bundle.tar

# clear the files
WORKDIR /
RUN rm -rf /tmp/*
# Set the default command
CMD ["echo", "Mysql installation completed successfully!"]
