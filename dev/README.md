# Development

## Prerequisites

* Python 3.8 or 3.9 (`mllint` not supported by 3.10)
* Docker 20.10 or later
* [Task](https://taskfile.dev/) build tool
* (Optional) Node.js and npm
    * Can be skipped by using Task's Docker tasks

## Running locally

### Interface service

```bash
cd interface_service/
virtualenv venv
source venv/bin/activate # or source venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Or, to avoid creating local virtual environments and Python version discrepancies:

```shell
task interface_service:docker_run
```

### Learning service

```bash
cd learning_service/
virtualenv venv
source venv/bin/activate # or source venv/Scripts/activate
pip install -r requirements.txt
```

Or, to avoid creating local virtual environments and Python version discrepancies:

```shell
task learning_service:docker_run
```

### Frontend

```bash
cd frontend/
npm ci
npm start
```

Or, to avoid Node and NPM version discrepancies:

```shell
task frontend:docker_run -- npm ci
task frontend:docker_run
```

## Launching development containers

In order to locally run the system's dependencies, run the Docker Compose containers with:

```shell
task dev:compose_up
```

**IMPORTANT:** The emulator of Google Cloud BigTable does not persist data between restarts!

In order to remove them and their local data, execute:

```shell
task dev:compose_down
```
