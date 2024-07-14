.PHONY: build up up-logs down restart logs shell

SERVICE_NAME := web

build:
	@echo "Building Docker images..."
	docker-compose build

up:
	@echo "Starting Express application..."
	docker-compose up -d --build
	@echo "Vue application started at http://localhost:8080"

down:
	@echo "Stopping Express application..."
	docker-compose down

restart:
	@echo "Restarting Express application..."
	docker-compose down
	docker-compose up -d --build
	@echo "Vue application started at http://localhost:8080"

logs:
	@echo "Fetching logs..."
	docker-compose logs -f

shell:
	@echo "Opening shell..."
	docker-compose exec $(SERVICE_NAME) sh