# Development

## Prerequisites

* Python 3.6-3.9 (`mllint` not supported by 3.10)
* Docker 20.10 or later
* [Task](https://taskfile.dev/) build tool
* (Optional) Node.js and npm
    * Can be skipped by using Task's Docker tasks

## Running locally

### Launching development containers

In order to locally run the system's dependencies, run the Docker Compose containers with:

```shell
task dev:compose:up
```

In order to remove them and their local data, execute:

```shell
task dev:compose:down
```

### Interface service

In case the compatible version of Python is used locally:

```shell
cd interface_service
task prepare
source interface_venv/bin/activate # on Windows: source venv/Scripts/activate
uvicorn main:app --reload
```

Or, to avoid Python version discrepancies and creating virtual environments:

```shell
task interface_service:docker_run
```

### Learning service

In case the compatible version of Python is used locally:

```shell
cd learning_service
task prepare
source learning_venv/bin/activate # on Windows: source venv/Scripts/activate
# TODO: Add command to run the learning service
```

Or, to avoid Python version discrepancies and creating virtual environments:

```shell
task learning_service:docker_run
```

### Frontend

```shell
cd frontend/
npm ci
npm start
```

Or, to avoid Node and NPM version discrepancies:

```shell
task frontend:docker_run -- npm ci
task frontend:docker_run
```
