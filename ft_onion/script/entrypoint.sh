#!/bin/bash

set -eou pipefail

/usr/sbin/sshd -D &
echo "SSH started ✅"

tor &
echo "Check if Tor is ready... ⏳"

while [ ! -f /var/lib/tor/hidden_service/hostname ]; do
    echo "Check if Tor is ready... ⏳"
    sleep 2
done
echo "Tor started ✅"

echo "NGINX started ✅. Website available on:" &
cat "/var/lib/tor/hidden_service/hostname" &
nginx -g "daemon off;"
