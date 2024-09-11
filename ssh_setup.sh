#!/bin/bash

# Generate SSH key pair if not already present
if [ ! -f /root/ssh_keys/id_rsa ]; then
    echo "Generating SSH keys..."
    ssh-keygen -t rsa -b 2048 -f /root/ssh_keys/id_rsa -q -N ""
    cat /root/ssh_keys/id_rsa.pub > /root/.ssh/authorized_keys
    chmod 600 /root/.ssh/authorized_keys
    chmod 700 /root/.ssh
    echo "SSH keys generated and added to authorized_keys."

    # Change ownership of the keys to match the host user (UID 1000, GID 1000)
    chown 1000:1000 /root/ssh_keys/id_rsa /root/ssh_keys/id_rsa.pub
else
    echo "SSH keys already exist, skipping generation."
fi

# Start the SSH daemon
/usr/sbin/sshd -D
