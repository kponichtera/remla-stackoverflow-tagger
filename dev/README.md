# Development

## Prerequisites

* Python 3.10 or later
* Docker 20.10 or later
* [Task](https://taskfile.dev/) build tool

## Running locally

### Interface service

```bash
cd interface_service/
virtualenv venv
source venv/Scripts/activate # or source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Learning service

```bash
cd learning_service/
virtualenv venv
source venv/Scripts/activate # or source venv/bin/activate
pip install -r requirements.txt
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
