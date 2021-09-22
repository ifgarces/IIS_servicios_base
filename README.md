# IIS_servicios_base

This project will use all systems as submodules, for running them all easily with [`docker-compose`](https://docs.docker.com/compose/), a tool for managing multi-container Docker applications. This is much better than setting an ugly command to run them all, and allows to restart them (or not) on failure, enhanced logging management, etc.

## Dependencies

`docker-compose` command (and Docker service). In Windows, it all comes with Docker Desktop. For other OSes, follow the [official installation guide](https://docs.docker.com/compose/install/).

## Overall project software architecture

Some settings (ports) can be configured at `compose.env`.

<!-- TODO: Makefile rules table -->

<!-- TODO: overall description and usage. Insert images. -->

## Build and run

Initializing nested submodules:

```sh
git submodule update --recursive --init
```
