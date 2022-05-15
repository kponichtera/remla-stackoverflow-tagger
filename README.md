# StackOverflow Tagger

Project for [Release Engineering for Machine Learning Applications](https://se.ewi.tudelft.nl/remla/2022/) 
(REMLA) course at TU Delft.

## Development

### Prerequisites

* Python 3.10 or later
* Docker 20.10 or later

### Launching development containers

In order to locally run the system's dependencies, run the Docker Compose containers with:

```shell
docker compose up -d
```

**IMPORTANT:** The emulator of Google Cloud BigTable does not persist data between restarts!

In order to remove their local data, execute:

```shell
docker compose down --volumes
```