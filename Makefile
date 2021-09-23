# Make sure you don't have uncommited changes before running this rule.
pull:
	git fetch && git pull
	git submodule update --recursive --init

# Builds the Docker images for all systems
build:
	docker-compose --env-file compose.env build

# Launches all the systems and outputs to stdout/stderr
up: pull
	docker-compose --env-file compose.env up --build --force-recreate

down:
	docker-compose --env-file compose.env down

# Ensures the docker-compose.yaml file is correct and prints it, parsed and prettified with `yq`
config:
	docker-compose --env-file compose.env config | yq eval

#TODO
# tests:
