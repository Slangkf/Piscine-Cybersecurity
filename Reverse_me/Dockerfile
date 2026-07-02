# Distribution used for the container.
# Debian Bookworm stable base image.
FROM	debian:bookworm

# Allows packages for the i386 architecture.
# Updates the package list and upgrades those that are installed.
# Installs required packages and then clean the apt cache.
RUN		dpkg --add-architecture i386 && \
		apt update -y && apt upgrade -y && apt install -y \
		file \
		binutils \
		gdb \
		libc6:i386 \
		&& rm -rf /var/lib/apt/lists/*

# Create the directories for the two exercises, then copy them there.
RUN		mkdir -p /app/level1 && \
		mkdir -p /app/level2

COPY	./level1/	/app/level1/ && \
		./level2/	/app/level2/

WORKDIR	/app

ENTRYPOINT ["sleep", "infinity"]
