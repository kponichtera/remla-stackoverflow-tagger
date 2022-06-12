FROM python:3.8.10 AS common

RUN mkdir /app \
    && useradd -d /app appuser \
    && chown -R appuser: /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

FROM common AS builder
ARG TASK_URL=https://github.com/go-task/task/releases/download/v3.12.1/task_linux_amd64.deb

RUN curl -o task.deb -L ${TASK_URL} \
    && dpkg -i task.deb \
    && rm task.deb

ENV XDG_CACHE_HOME /cache
RUN mkdir $XDG_CACHE_HOME

COPY learning_service/requirements.txt .

RUN pip install --upgrade pip wheel \
    && pip install -r requirements.txt \
    && chmod -R 777 $XDG_CACHE_HOME

# mllint tries to make its file executable - can't do this unless it's root or owns the file\
RUN chown -R appuser: /usr/local/lib/python3.8/site-packages/mllint

CMD ["python", "-m", "learning_service.main"]

FROM common AS final
EXPOSE 9010

COPY learning_service/requirements.txt .

RUN pip install --upgrade pip wheel --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir

WORKDIR /app
USER appuser

COPY common .
COPY learning_service .

CMD ["python", "-m", "learning_service.main"]