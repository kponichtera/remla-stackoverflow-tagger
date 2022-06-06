FROM python:3.7.10 AS builder
ARG TASK_URL=https://github.com/go-task/task/releases/download/v3.12.1/task_linux_amd64.deb

RUN mkdir /app \
    && useradd -d /app appuser \
    && chown -R appuser: /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

RUN curl -o task.deb -L ${TASK_URL} \
    && dpkg -i task.deb \
    && rm task.deb

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# mllint tries to make its file executable - can't do this unless it's root or owns the file
RUN chown -R appuser: /usr/local/lib/python3.7/site-packages/mllint

# TODO: Replace with actual application startup
CMD ["bash"]

FROM builder AS final

WORKDIR /app
USER appuser

COPY . .
