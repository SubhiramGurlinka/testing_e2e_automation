FROM rockylinux/rockylinux:8

# Install necessary tools and configure MongoDB repository
RUN yum install -y yum-utils && \
    rpm --import https://www.mongodb.org/static/pgp/server-8.0.asc && \
    yum-config-manager --add-repo https://repo.mongodb.org/yum/redhat/8/mongodb-org/8.0/x86_64/ && \
    yum clean all

# Install specific version of MongoDB (8.0.1 in this example)
RUN yum install -y mongodb-org-8.0.1 mongodb-org-database-8.0.1 mongodb-org-server-8.0.1 mongodb-mongosh mongodb-org-mongos-8.0.1 mongodb-org-tools-8.0.1 && \
    yum clean all

# Exclude MongoDB from automatic updates
#RUN echo "exclude=mongodb-org,mongodb-org-database,mongodb-org-server,mongodb-mongosh,mongodb-org-mongos,mongodb-org-tools" >> /etc/yum.conf

RUN rpm -qa | grep mongodb-org

# clear the files
WORKDIR /
RUN rm -rf /tmp/*

# Set the default command
CMD ["echo", "MongoDB installation completed successfully!"]
