FROM python:3.10 AS builder
ARG TASK_URL=https://github.com/go-task/task/releases/download/v3.12.1/task_linux_amd64.deb

RUN mkdir /app \
    && useradd -d /app appuser \
    && chown -R appuser: /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends git curl \
    && apt-get purge -y --auto-remove gcc libc-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -o task.deb -L ${TASK_URL} \
    && dpkg -i task.deb \
    && rm task.deb

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["bash"]

FROM builder AS final
EXPOSE 8000

WORKDIR /app
USER appuser
RUN mkdir models

COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
