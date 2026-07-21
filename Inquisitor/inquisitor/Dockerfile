# Use Debian Bookworm as the base image for the container environment.
FROM	debian:bookworm

# Install Python dependencies.
# Remove package lists afterward to reduce the final image size.
RUN		apt update -y && apt upgrade -y && apt install -y \
		python3 \
		python3-pip \
		python3-venv \
		libpcap-dev \
		procps \
		iproute2 \
		net-tools \
		&& rm -rf /var/lib/apt/lists/*

# Copy the scripts into the container.
COPY ./script/*.py		/app/

# Set the working directory.
WORKDIR	/app

# Keep the container running indefinitely.
ENTRYPOINT ["sleep", "infinity"]
