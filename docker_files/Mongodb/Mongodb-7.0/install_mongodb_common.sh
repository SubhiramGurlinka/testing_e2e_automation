#!/bin/bash

# Usage:
# bash install_mongodb.sh <os_type> <os_version> <mongodb_version>
# os_type: "rhel" or "ubuntu"
# os_version: For RHEL: major version like 7, 8, or 9. For Ubuntu: "jammy", "focal", or "bionic"
# mongodb_version: MongoDB version like 7.0.5

if [ $# -ne 3 ]; then
    echo "Usage: $0 <os_type> <os_version> <mongodb_version>"
    exit 1
fi

os_type=$1
os_version=$2
version=$3

major_version=$(echo "$version" | cut -d. -f1-2)

install_mongodb_rhel() {
    # Check which package manager to use
    if command -v dnf &> /dev/null; then
        package_manager="dnf"
    elif command -v yum &> /dev/null; then
        package_manager="yum"
    else
        echo "Neither dnf nor yum package manager found. Exiting."
        exit 1
    fi

    # Install wget
    $package_manager install -y sudo
    sudo $package_manager install -y wget

    # Download MongoDB packages
    sudo wget "https://repo.mongodb.org/yum/redhat/$os_version/mongodb-org/$major_version/x86_64/RPMS/mongodb-org-tools-$version-1.el$os_version.x86_64.rpm"
    sudo wget "https://repo.mongodb.org/yum/redhat/$os_version/mongodb-org/$major_version/x86_64/RPMS/mongodb-org-server-$version-1.el$os_version.x86_64.rpm"
    sudo wget "https://repo.mongodb.org/yum/redhat/$os_version/mongodb-org/$major_version/x86_64/RPMS/mongodb-org-mongos-$version-1.el$os_version.x86_64.rpm"
    sudo wget "https://repo.mongodb.org/yum/redhat/$os_version/mongodb-org/$major_version/x86_64/RPMS/mongodb-org-database-tools-extra-$version-1.el$os_version.x86_64.rpm"
    sudo wget "https://repo.mongodb.org/yum/redhat/$os_version/mongodb-org/$major_version/x86_64/RPMS/mongodb-org-database-$version-1.el$os_version.x86_64.rpm"
    sudo wget "https://repo.mongodb.org/yum/redhat/$os_version/mongodb-org/$major_version/x86_64/RPMS/mongodb-org-$version-1.el$os_version.x86_64.rpm"
    sudo wget "https://repo.mongodb.org/yum/redhat/$os_version/mongodb-org/$major_version/x86_64/RPMS/mongodb-mongosh-2.2.1.x86_64.rpm"
    sudo wget "https://repo.mongodb.org/yum/redhat/$os_version/mongodb-org/$major_version/x86_64/RPMS/mongodb-database-tools-100.9.4.x86_64.rpm"

    # Install MongoDB packages
    sudo $package_manager install -y mongodb*.rpm

    # Clean up
    sudo rm -f mongodb*.rpm

    # Show installed MongoDB version and packages
    echo "Installed MongoDB version: $version"
    rpm -qa | grep mongo
}

install_mongodb_ubuntu() {
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
    apt-get install -y sudo libcurl4

    # Download MongoDB packages
    sudo wget "https://repo.mongodb.org/apt/ubuntu/dists/$os_version/mongodb-org/$major_version/multiverse/binary-amd64/mongodb-mongosh_2.2.1_amd64.deb"
    sudo wget "https://repo.mongodb.org/apt/ubuntu/dists/$os_version/mongodb-org/$major_version/multiverse/binary-amd64/mongodb-database-tools_100.9.4_amd64.deb"
    sudo wget "https://repo.mongodb.org/apt/ubuntu/dists/$os_version/mongodb-org/$major_version/multiverse/binary-amd64/mongodb-org-database-tools-extra_${version}_amd64.deb"
    sudo wget "https://repo.mongodb.org/apt/ubuntu/dists/$os_version/mongodb-org/$major_version/multiverse/binary-amd64/mongodb-org-shell_${version}_amd64.deb"
    sudo wget "https://repo.mongodb.org/apt/ubuntu/dists/$os_version/mongodb-org/$major_version/multiverse/binary-amd64/mongodb-org-mongos_${version}_amd64.deb"
    sudo wget "https://repo.mongodb.org/apt/ubuntu/dists/$os_version/mongodb-org/$major_version/multiverse/binary-amd64/mongodb-org-tools_${version}_amd64.deb"
    sudo wget "https://repo.mongodb.org/apt/ubuntu/dists/$os_version/mongodb-org/$major_version/multiverse/binary-amd64/mongodb-org-database_${version}_amd64.deb"
    sudo wget "https://repo.mongodb.org/apt/ubuntu/dists/$os_version/mongodb-org/$major_version/multiverse/binary-amd64/mongodb-org-server_${version}_amd64.deb"
    sudo wget "https://repo.mongodb.org/apt/ubuntu/dists/$os_version/mongodb-org/$major_version/multiverse/binary-amd64/mongodb-org_${version}_amd64.deb"

    # Install MongoDB packages
    sudo dpkg -i mongodb-mongosh_2.2.1_amd64.deb
    sudo dpkg -i mongodb-database-tools_100.9.4_amd64.deb
    sudo dpkg -i mongodb-org-database-tools-extra_${version}_amd64.deb
    sudo dpkg -i mongodb-org-shell_${version}_amd64.deb
    sudo dpkg -i mongodb-org-mongos_${version}_amd64.deb
    sudo dpkg -i mongodb-org-tools_${version}_amd64.deb
    sudo dpkg -i mongodb-org-server_${version}_amd64.deb
    sudo dpkg -i mongodb-org-database_${version}_amd64.deb
    sudo dpkg -i mongodb-org_${version}_amd64.deb

    # Clean up
    sudo rm -f mongodb*.deb

    # Show installed MongoDB version and packages
    echo "Installed MongoDB version: $version"
    dpkg -l | grep mongo
}

restart_bes_client() {
    # Restart BES client with a timeout of 15 seconds
    /etc/init.d/besclient restart &
    sleep 15
    # Check if BES client restarted, if not, start it
    if ! ps -ef | grep -q "[b]esclient"; then
        /etc/init.d/besclient start
    fi
}

# Display OS details
cat /etc/os-release
echo
echo

# Execute installation based on OS type
case $os_type in
    rhel)
        install_mongodb_rhel
        ;;
    ubuntu)
        install_mongodb_ubuntu
        ;;
    *)
        echo "Invalid OS type. Please specify 'rhel' or 'ubuntu'."
        exit 1
        ;;
esac

# Restart BES client if desired
restart_bes_client
