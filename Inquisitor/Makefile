.PHONY: help build up stop down destroy images ps logs

help:
	@echo "Makefile commands:"
	@echo "  make build		- Build Docker images"
	@echo "  make up		- Start Docker containers"
	@echo "  make stop		- Stop containers"
	@echo "  make down		- Stop and remove containers"
	@echo "  make destroy		- Stop and remove images, containers, and network"
	@echo "  make images		- List images"
	@echo "  make ps		- List running containers"
	@echo "  make logs		- Show container logs"

build:
	@docker compose -f ./docker-compose.yml build

up:
	docker compose up -d
	@printf "\033[1;33mWarning\033[0m: to activate the venv in the inquisitor container, run: source venv/bin/activate\n"
	@for id in $$(docker compose ps -q); do \
		docker inspect -f '{{.Name}} {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}} {{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' $$id; \
	done

stop:
	@docker compose -f ./docker-compose.yml stop

down:
	@docker compose -f ./docker-compose.yml down

destroy:
	@printf "\033[1;31mWarning\033[0m: containers images, and network will be deleted. Do you want to continue?\n"
	@read -p "Type 'YES' to confirm: " confirm; \
	if [ "$$confirm" != "YES" ] && [ "$$confirm" != "yes" ]; then \
		echo "Aborting destroy."; \
		exit 1; \
	fi
	@docker compose -f ./docker-compose.yml down --rmi all --volumes --remove-orphans

images:
	@docker compose -f ./docker-compose.yml images

ps:
	@docker compose -f ./docker-compose.yml ps

logs:
	@docker compose -f ./docker-compose.yml logs -f
