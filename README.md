# IIS_servicios_base

This project will use all systems as submodules, for running them all easily with [`docker-compose`](https://docs.docker.com/compose/), a tool for managing multi-container Docker applications. This is much better than setting an ugly command to run them all, and allows to restart them (or not) on failure, enhanced logging management, etc.

## Dependencies

Note: this project is intended to run in an Ubuntu-based host OS.

- `docker-compose` command (and Docker service). In Windows, it all comes with Docker Desktop. For other OSes, follow the [official installation guide](https://docs.docker.com/compose/install/).
- Just for the `config` Makefile rule, the [`yq` command-line YAML processor](https://github.com/mikefarah/yq) is required. You can install it on Ubuntu with `wget https://github.com/mikefarah/yq/releases/download/v4.13.2/yq_linux_amd64.tar.gz -O - | tar xz && sudo mv yq_linux_amd64 /usr/bin/yq`.

## Overall project software architecture

The exposed API ports for the systems can be configured at [`compose.env`](./compose.env).

<!-- TODO: overall description and usage. Insert images. -->

## Build and run

The Makefile rules are stated in the below table. You may only have interest in the `up` one.

| Makefile rule | Description                                                                                          |
| ------------- | ---------------------------------------------------------------------------------------------------- |
| `pull`        | Updates all systems (pulls/initializes submodules repos).                                            |
| `build`       | Builds the Docker images for all systems.                                                            |
| **`up`**      | **Launches (and pull/build, if needed) the systems as Docker containers.**                           |
| `down`        | Shuts down all systems.                                                                              |
| `config`      | Ensures the `docker-compose.yaml` configuration file is correct, and prints it prettified with `yq`. |
