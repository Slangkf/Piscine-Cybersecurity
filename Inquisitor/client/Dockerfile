# Use Debian Bookworm as the base image for the container environment.
FROM	debian:bookworm

# Install the TNFTP client dependency.
# Remove package lists afterward to reduce the final image size.
RUN		apt update -y && apt upgrade -y && apt install -y \
		tnftp \
		python3 \
		net-tools \
		&& rm -rf /var/lib/apt/lists/*

# Create the directory used by the program to store test files.	
RUN		mkdir -p /home/test_environment/

# Copy the script into the container.
COPY	./script/create_test_files.py	/app/

# Set the working directory.
WORKDIR	/app

# Keep the container running.
ENTRYPOINT ["sleep", "infinity"]
