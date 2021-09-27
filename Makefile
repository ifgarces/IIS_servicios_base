# Make sure you don't have uncommited changes before running this rule.
pull:
	git fetch && git pull
	git submodule update --recursive --init --remote

# Builds the Docker images for all systems
build:
	docker-compose --env-file compose.env build

# Launches all the systems and outputs to stdout/stderr
up:
	docker-compose --env-file compose.env up --build --force-recreate

down:
	docker-compose --env-file compose.env down

# Ensures the docker-compose.yaml file is correct and prints it, prettified by `yq`
config:
	docker-compose --env-file compose.env config | yq eval

#TODO
# tests:
