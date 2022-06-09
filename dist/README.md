# Local deployment

## Prerequisites

* Docker 20.10 or later
* [Task](https://taskfile.dev/) build tool

## Running locally

In order to build and run the system's components locally, execute:

```shell
task dist:compose:up
```

In order to remove them and their local data, execute:

```shell
task dist:compose:down
```
