FROM google/cloud-sdk:387.0.0-alpine AS builder
ARG TASK_URL=https://github.com/go-task/task/releases/download/v3.12.1/task_linux_amd64.tar.gz
ARG TERRAFORM_URL=https://releases.hashicorp.com/terraform/1.2.1/terraform_1.2.1_linux_amd64.zip

RUN gcloud components install beta

RUN apk add --no-cache unzip

RUN curl -o task.tgz -L ${TASK_URL} \
    && tar xvzf task.tgz task \
    && mv task /usr/bin/ \
    && rm task.tgz

RUN curl -o terraform.zip -L ${TERRAFORM_URL} \
    && unzip terraform.zip terraform -d /usr/bin/ \
    && rm terraform.zip