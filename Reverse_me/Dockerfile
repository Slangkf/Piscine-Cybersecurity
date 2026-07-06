# Distribution used for the container.
# Debian Bookworm stable base image.
FROM	debian:bookworm

# Allows packages for the i386 architecture.
# Updates the package list and upgrades those that are installed.
# Installs required packages, then cleans the apt cache.
RUN		dpkg --add-architecture i386 && \
		apt update -y && apt upgrade -y && apt install -y \
		gcc \
		file \
		binutils \
		gdb \
		libc6:i386 \
		&& rm -rf /var/lib/apt/lists/*

# Copies the exercise files into the container.
COPY	./level1/	/app/level1/
COPY	./level2/	/app/level2/
COPY	./level3/	/app/level3/

# Sets the working directory to /app. 
WORKDIR	/app

# Keeps the container running.
ENTRYPOINT ["sleep", "infinity"]
