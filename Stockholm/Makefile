IMAGE := stock_image
CONTAINER := stock_container

.PHONY: help build run exec stop ps images down destroy

help:
	@echo "Makefile commands:"
	@echo "  make build		- Build the container"
	@echo "  make run		- Start the container"
	@echo "  make stop		- Stop the container"
	@echo "  make down		- Stop and remove the container"
	@echo "  make destroy		- Stop and remove the Stockholm container and image"
	@echo "  make images		- List all Docker images"
	@echo "  make ps		- List all running containers"

build:
	@docker build -t $(IMAGE) .

run:
	@docker rm -f $(CONTAINER) || true
	@docker run -d --name $(CONTAINER) $(IMAGE)

exec:
	@docker exec -it $(CONTAINER) bash || true

stop:
	@docker stop $(CONTAINER) || true

ps:
	@docker ps

images:
	@docker images

down:
	@docker stop $(CONTAINER) || true
	@docker rm $(CONTAINER) || true

destroy:
	@printf "\033[1;31mWarning\033[0m: the $(CONTAINER) container and image will be deleted. Do you want to continue?\n"
	@read -p "Type 'YES' to confirm: " confirm; \
	if [ "$$confirm" != "YES" ] && [ "$$confirm" != "yes" ]; then \
		echo "Aborting destroy."; \
		exit 1; \
	fi
	@docker stop $(CONTAINER) || true
	@docker rm $(CONTAINER) || true
	@docker rmi -f $(IMAGE) || true
