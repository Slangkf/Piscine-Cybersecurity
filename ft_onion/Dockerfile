# Distribution used for the container.
# Debian Bookworm stable base image.
FROM	debian:bookworm

# Updates the package list and upgrades those that are installed.
# Installs required packages and then clean the apt cache.
RUN		apt update -y && apt upgrade -y && apt install -y \
		nginx \
		tor \
		openssh-server \
		&& rm -rf /var/lib/apt/lists/*

# Replaces default Tor configuration with custom torrc.
COPY	./tor/torrc /etc/tor/torrc

# Replaces default SSH configuration with custom sshd_config.
# Creates the directory needed for sshd
COPY	./ssh/sshd_config /etc/ssh/sshd_config
RUN		mkdir -p /run/sshd

# Creates the .ssh directory with the required permissions.
RUN		mkdir -p /root/.ssh && chmod 700 /root/.ssh

# Copies the public SSH key into the .ssh directory.
# Restricts access to the file's owner only (required by sshd).
COPY	./ssh/authorized_keys /root/.ssh/
RUN		chmod 600 /root/.ssh/authorized_keys

# Replaces default NGINX configuration with custom nginx.conf.
COPY	./nginx/nginx.conf /etc/nginx/nginx.conf

# Copies the index.html file into the directory created by the NGINX installation.
COPY	./web/index.html /var/www/html/

# Copies the script into the container.
# Makes it executable so it can be run at container startup.
COPY	./script/ /usr/local/bin/
RUN		chmod +x /usr/local/bin/entrypoint.sh

# Exposes HTTP and SSH ports.
EXPOSE	80
EXPOSE	4242

CMD	["/usr/local/bin/entrypoint.sh"]