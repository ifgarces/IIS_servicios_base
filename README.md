# IIS_servicios_base

> Introducción a la Ingeniería en Software, Universidad de los Andes, 2021

This project will use all systems as git submodules, for running them all easily with [`docker-compose`](https://docs.docker.com/compose/), a tool for managing multi-container Docker applications. This is much better than setting an rough command to run them one by one, and allows to restart them (or not) on crash, enhanced logging management, etc.

**Note: the project is intended to run in a Linux shell**. If you pretend to run or test the environment locally in Windows, you may install [Ubuntu](https://www.microsoft.com/en-us/p/ubuntu-2004-lts/9n6svws3rx71) via [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) and run it easily, after installing the [dependencies](#dependencies).

## Dependencies

- [`docker-compose`](https://docs.docker.com/compose/install/) command (and Docker service).
- Just for the `config` Makefile rule, the [`yq` command-line YAML processor](https://github.com/mikefarah/yq) is required. You can install it on Ubuntu-based OSes with `wget https://github.com/mikefarah/yq/releases/download/v4.13.2/yq_linux_amd64.tar.gz -O - | tar xz && sudo mv yq_linux_amd64 /usr/bin/yq`.

## Overall project software architecture

The exposed API ports for the systems can be configured at [`compose.env`](./compose.env). The below figures show the overall systems architecture. Each system is executed as a Docker container, with only a single exposed port (the API port). In the API calls figure, the arrows point towards the system they are providing the specified endpoint or call (in other words, the colored one is an endpoint exposed by Prendas, see the [PPE API documentation](./docs/api/PPE.md)).

![Overall systems diagram](./docs/diagram_overall.jpg "Overall diagram")

![API calls](./docs/diagram_api_calls.jpg "API calls diagram")

## API documentation

The usage docs for the APIs are located at `./docs/api` in this project. All of them contain sample `curl` commands (which is a console tool for making HTTP requests, working on Linux as well as Windows OSes, if desired).

## Build and run

The Makefile rules are stated in the below table. You may only have interest in the `up` one.

**If you have problems with `make pull`:** please pull manually and run `git submodule update --init --recursive`.

| Makefile rule     | Description                                                                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `build` (default) | Builds the Docker images for all systems.                                                                                                   |
| **`up`**          | **Launches the systems as Docker containers (builds and pulls if needed) and outputs to stdout/stderr**. Use ctrl+c to stop to environment. |
| `up_background`   | Executes `up`, but in background.                                                                                                           |
| `pull`            | Updates all systems (pulls/initializes submodule repos). Make sure you don't have uncommitted changes before running this rule.             |
| `down`            | Shuts down all systems. You may need it when running `up_background`.                                                                       |
| `config`          | Ensures the `docker-compose.yaml` configuration file is correct, and prints it prettified with `yq`.                                        |
| `test`            | Executes test API calls. See the [testing section](#testing) below.                                                                         |

## Logging

Before executing any shell command of this section, please run `alias docker-compose='docker-compose --env-file compose.env'`.

If you run the systems with `make up`, you will see the output in stdout/stderr. For `make up_background`, you can use `docker-compose logs` to view all logs or use `docker-compose logs [srcei|caja|rvm|ppe]` to view the log of one of the systems (e.g. `docker-compose logs srcei`). Ensure to execute these commands in the root directory of this project.

## Testing

For running automated test API calls, first ensure the systems are running locally in your machine and then run `make test`. You must have Python 3 installed.
