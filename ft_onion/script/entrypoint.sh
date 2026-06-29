#!/bin/bash

set -eou pipefail

# Start the SSH server in the background.
# -D keeps sshd running in the foreground, but "&" sends it to the background
# so the script can continue executing.
/usr/sbin/sshd -D &
echo "SSH started ✅"

# Start the Tor service in the background.
# This will create the Tor hidden service and generate its hostname file.
tor &
echo "Check if Tor is ready... ⏳"

# Wait until Tor has created the hidden service hostname file.
# The file appears only when the .onion address has been generated.
while [ ! -f /var/lib/tor/hidden_service/hostname ]; do
    echo "Check if Tor is ready... ⏳"
    sleep 2
done
echo "Tor started ✅"

# Start NGINX and display the generated Tor hidden service address.
# The hostname file contains the .onion URL where the website is accessible.
# "daemon off;" keeps NGINX running in the foreground,
# which is required for Docker containers so the container stays alive.
echo "NGINX started ✅. Website available on:" &
cat "/var/lib/tor/hidden_service/hostname" &
nginx -g "daemon off;"
