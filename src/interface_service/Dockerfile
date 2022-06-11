FROM python:3.10 AS common

RUN mkdir /app \
    && useradd -d /app appuser \
    && chown -R appuser: /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends git curl \
    && apt-get purge -y --auto-remove gcc libc-dev \
    && rm -rf /var/lib/apt/lists/*

FROM common AS builder
ARG TASK_URL=https://github.com/go-task/task/releases/download/v3.12.1/task_linux_amd64.deb

RUN curl -o task.deb -L ${TASK_URL} \
    && dpkg -i task.deb \
    && rm task.deb

ENV XDG_CACHE_HOME /cache
RUN mkdir $XDG_CACHE_HOME

COPY interface_service/requirements.txt .

RUN pip install --upgrade pip wheel \
    && pip install -r requirements.txt \
    && chmod -R 777 $XDG_CACHE_HOME

CMD ["uvicorn", "interface_service.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM common AS final
EXPOSE 8000

COPY interface_service/requirements.txt .

RUN pip install --upgrade pip wheel --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir

WORKDIR /app
USER appuser
RUN mkdir models

COPY common .
COPY interface_service .

CMD ["uvicorn", "interface_service.main:app", "--host", "0.0.0.0", "--port", "8000"]