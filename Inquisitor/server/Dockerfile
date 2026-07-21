# Use Debian Bookworm as the base image for the container environment.
FROM	debian:bookworm

# Install the VSFTPD server dependency.
# Remove package lists afterward to reduce the final image size.
RUN		apt update -y && apt upgrade -y && apt install -y \
		vsftpd \
		net-tools \
		&& rm -rf /var/lib/apt/lists/*

# Create the secure chroot directory required by vsftpd for isolated filesystem access.
RUN		mkdir -p /var/run/vsftpd/empty

RUN		mkdir -p /srv/ftp/ \
		&& chown root:root /srv/ftp/ \
		&& chmod 755 /srv/ftp/ \
		&& mkdir -p /srv/ftp/uploads \
		&& chown root:ftp /srv/ftp/uploads \
		&& chmod 775 /srv/ftp/uploads

# Copy the custom vsftpd configuration into the image.
COPY	./conf/vsftpd.conf	/etc/vsftpd.conf

# Set the working directory.
WORKDIR	/srv/ftp/uploads

# Expose the control port (21) and the passive mode data port range.
EXPOSE	21 50000-50004

# Keep the container running.
ENTRYPOINT ["/usr/sbin/vsftpd"]
