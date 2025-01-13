# RHEL 9 Dockerfile
FROM rockylinux/rockylinux:9

# Install necessary tools and configure MongoDB repository
RUN yum install -y yum-utils && \
    rpm --import https://www.mongodb.org/static/pgp/server-8.0.asc && \
    yum-config-manager --add-repo https://repo.mongodb.org/yum/redhat/9/mongodb-org/8.0/x86_64/ && \
    yum clean all

# Install specific version of MongoDB (8.0.1 in this example)
RUN yum install -y mongodb-org-8.0.1 mongodb-org-database-8.0.1 mongodb-org-server-8.0.1 mongodb-mongosh mongodb-org-mongos-8.0.1 mongodb-org-tools-8.0.1 && \
    yum clean all

RUN rpm -qa | grep mongodb-org

# clear the files
WORKDIR /
RUN rm -rf /tmp/*

# Set the default command
CMD ["echo", "MongoDB installation completed successfully!"]