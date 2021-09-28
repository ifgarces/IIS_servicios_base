# Builds the Docker images for all systems
build:
	docker-compose --env-file compose.env build

# Launches all the systems and outputs to stdout/stderr
up: pull
	docker-compose --env-file compose.env up --build --force-recreate

down:
	docker-compose --env-file compose.env down

# Pulling this repo and all submodules
pull:
	git fetch
	git pull
	git submodule foreach --recursive git checkout main
	git submodule foreach --recursive git fetch
	git submodule foreach --recursive git pull

# Ensures the docker-compose.yaml file is correct and prints it, prettified by `yq`
config:
	docker-compose --env-file compose.env config | yq eval
