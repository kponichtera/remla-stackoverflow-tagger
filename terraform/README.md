# Infrastructure provisioning

The project's infrastructure is meant to be deployed on Google Cloud and is managed by Terraform.

## Prerequisites

* Docker 20.10 or later
* [Task](https://taskfile.dev/) build tool
* Google Cloud SDK 372.0.0 or newer

All the necessary infrastructure management operations are wrapped in Docker containers,
so there is no need to install Terraform or anything else locally.

### Authenticating with Google Cloud

The credentials are stored in a dedicated Docker container and mounted whenever commands are executed in the new one.
To authenticate, execute the following command and follow the instructions:

```shell
task terraform:docker-gcloud-login
```

In order to logout, remove the container with credentials by calling:

```shell
task terraform:docker-gcloud-logout
```

### Initial provisioning

> **Note:** the Terraform-specific tasks within the builder container are executed in the terraform directory,
> so they do not require *terraform:* prefix.

#### If the project doesn't exist

Once authenticated, it is possible to proceed with initial provisioning of the project 
(e.g. create project in Google Cloud, create bucket for Terraform state etc.)

If the project in Google Cloud doesn't exist yet, execute

```shell
task terraform:docker-run -- task provision PROJECT_ID=<project_id> BILLING_ACCOUNT_ID=<billing_account_id>
```

The `<project_id>` is the identifier of a project to be created 
and `<billing_account_id>` is the identifier of the billing account that will be charged.
The identifiers of the billing accounts can be obtained with

```shell
task terraform:docker-run -- gcloud beta billing accounts list
```

#### If the project exists

In case the project already exists and has a billing account attached, the provisioning can be performed
to ensure that all the necessary elements are present:

```shell
task terraform:docker_run -- task provision PROJECT_ID=<project_id>
```

### Creating Terraform service account key

Terraform uses a Google Cloud service account to perform necessary infrastructure operations
without having the full owner role.
In order to generate a new key and store it locally in the project directory, execute:

```shell
task terraform:docker-run -- task service-account:create-key PROJECT_ID=<project_id>
```

### Initializing Terraform project

In order to initialize the local Terraform directory and the remote state bucket, execute:

```shell
task terraform:docker-run -- task init PROJECT_ID=<project_id>
```

### Applying infrastructure changes

To see what changes are waiting to be applied in the infrastructure, execute:

```shell
task terraform:docker-run -- task plan
```

To review them again and apply, execute:

```shell
task terraform:docker-run -- task apply
```

### Taking down the infrastructure

To remove all the Terraform resources, execute:

```shell
task terraform:docker-run -- task destroy
```

In order to perform final cleanup (eg. remove the state bucket and Terraform's service account), execute:

```shell
task terraform:docker-run -- task cleanup PROJECT_ID=<project_id>
```

### Executing arbitrary Terraform command

```shell
task terraform:docker-run -- task run -- <command_and_args>
```
