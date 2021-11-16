# Builds the Docker images for all systems
build:
	docker-compose --env-file compose.env build

# Launches all the systems and outputs to stdout/stderr
up:
	docker-compose --env-file compose.env up --build --force-recreate

up_background:
	docker-compose --env-file compose.env up --build --force-recreate --detach

down:
	docker-compose --env-file compose.env down

clean: down
	docker container prune --force
	docker network prune --force

# Pulling this repo and all submodules
pull:
	git fetch
	git pull
	git submodule foreach --recursive git checkout main
	git submodule foreach --recursive git fetch
	git submodule foreach --recursive git pull
	git submodule update --recursive --init

# Ensures the docker-compose.yaml file is correct and prints it, prettified by `yq`
config:
	docker-compose --env-file compose.env config | yq eval

# Executes tests for API endpoints for all systems
test:
	cd tests && python3 curl_tests.py $(TGR_TARGET_HOST)
