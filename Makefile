APP_LOCATION           = "$(PWD)"

GIT_HOOK_TEMPLATE      = "$(APP_LOCATION)/_utils/pre-commit.sh"
GIT_HOOK_DEST          = "$(APP_LOCATION)/.git/hooks/pre-commit"

DB_NAME                = "flaskdb"
DB_USER                = "postgres"
DB_ENV_TEMPLATE        = "$(APP_LOCATION)/docker/db/.env.template"
DB_ENV_DEST            = "$(APP_LOCATION)/docker/db/.env"

APP_ENV_TEMPLATE       = "$(APP_LOCATION)/application/.env.template"
APP_ENV_DEST           = "$(APP_LOCATION)/application/.env"


all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

validate_env:
	@command -v docker > /dev/null || (echo "You need to install docker and docker-compose before proceeding" && exit 1)
	@command -v docker-compose > /dev/null || (echo "You need to install docker and docker-compose before proceeding" && exit 1)

build: validate_env ## Build images and run the containers
	@[ -f $(APP_ENV_DEST) ] || cp $(APP_ENV_TEMPLATE) $(APP_ENV_DEST)
	@[ -f $(DB_ENV_DEST) ] || cp $(DB_ENV_TEMPLATE) $(DB_ENV_DEST)
	@docker-compose build
	@docker-compose up -d
	@sleep 15
	@docker-compose restart
	@sleep 15
	@docker-compose exec --user="$(DB_USER)" postgres /bin/bash -c "psql -c 'CREATE DATABASE $(DB_NAME) ENCODING 'UTF8' TEMPLATE template0'" || true
	@docker-compose exec app python manage.py db upgrade

start:
	@docker-compose start

stop:
	@docker-compose stop

up: start ## Start containers and run the project in dev mode
	@docker-compose exec app python manage.py runserver

down: stop ## Stop containers

reset-container: ## Reset the container to the original state
	@docker-compose down
	@docker-compose up -d

remove: stop ## Remove all containers
	@docker-compose down

restart: ## Restart all containers
	@docker-compose restart

logs: ## Show logs of container
	@docker-compose logs -f --tail=100

cmd: ## Run a command line inside the container
	@docker-compose exec app /bin/bash

psql: ## Attach to psql inside postgres container
	@docker-compose exec --user $(DB_USER) postgres psql $(DB_NAME)

psql-cmd: ## Command line inside database container
	@docker-compose exec --user $(DB_USER) postgres /bin/bash

git-hooks: ## Config git hooks
	@pip install flake8
	@[ -f $(GIT_HOOK_DEST) ] || ln -s $(GIT_HOOK_TEMPLATE) $(GIT_HOOK_DEST)

.DEFAULT_GOAL := help
