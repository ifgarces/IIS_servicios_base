# Updates all systems (pulls submodules repos)
update:
	git submodule update --recursive --init

# Builds the Docker images for all systems
build:
	docker-compose --env-file compose.env build

# Launches all the systems and outputs to stdout/stderr
up: update
	docker-compose --env-file compose.env up --build --force-recreate

# Ensures the docker-compose.yaml file is correct and prints it, parsed and prettified with `yq`
# https://github.com/mikefarah/yq#install
# wget https://github.com/mikefarah/yq/releases/download/v4.13.2/yq_linux_amd64.tar.gz -O - | tar xz && sudo mv yq_linux_amd64 /usr/bin/yq
config:
	docker-compose --env-file compose.env config | yq eval

#TODO
tests_maybe:
	echo TODO