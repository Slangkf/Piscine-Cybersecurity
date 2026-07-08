# Use Debian Bookworm as the base image for the container environment.
FROM	debian:bookworm

# Install Python dependencies and the required cryptographic library.
# Remove package lists afterward to reduce the final image size.
RUN		apt update -y && apt upgrade -y && apt install -y \
		python3 \
		python3-pip \
		python3-venv \
		libsodium-dev \
		&& rm -rf /var/lib/apt/lists/*

# Create the directory used by the program to store test files.
RUN		mkdir -p /home/infection/

# Copy the application scripts into the container.
COPY	./create_test_files.py	/app/
COPY	./stockholm.py			/app/

# Set the working directory.
WORKDIR	/app

# Keep the container running indefinitely.
ENTRYPOINT ["sleep", "infinity"]
