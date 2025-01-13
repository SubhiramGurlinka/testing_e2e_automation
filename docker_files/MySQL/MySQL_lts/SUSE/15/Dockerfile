# Dockerfile for openSUSE 15

FROM opensuse/leap:15

# Set environment variables
ARG MYSQL_VERSION=8.0.37
RUN zypper install -y wget
# Copy MySQL files to the container
RUN wget https://downloads.mysql.com/archives/get/p/23/file/mysql-8.0.37-1.sl15.x86_64.rpm-bundle.tar
COPY mysql-8.0.37-1.sl15.x86_64.rpm-bundle.tar /tmp/

# Install required packages
RUN zypper install -y wget sudo perl libaio numactl net-tools libopenssl1_1 libtirpc0 && \
    tar -xvf /tmp/mysql-8.0.37-1.sl15.x86_64.rpm-bundle.tar -C /tmp/ && \
    zypper install -y /tmp/mysql-*.rpm && \
    rm -f /tmp/mysql-8.0.37-1.sl15.x86_64.rpm-bundle.tar
# clear the files
WORKDIR /
RUN rm -rf /tmp/*
# Show MySQL version
CMD ["mysql", "--version"]
