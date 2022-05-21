FROM python:3.7.10-slim
# Make new user as root
WORKDIR /app
RUN useradd -d /app appuser && chown -R appuser: /app

RUN apt-get update \
&& apt-get install -y --no-install-recommends git \
&& apt-get purge -y --auto-remove \
&& rm -rf /var/lib/apt/lists/*

# ...
# Copy files and install dependencies still as root
COPY . .
RUN python -m pip install --upgrade pip &&\
    pip install -r requirements.txt

# Step down from being a root before calling CMD/ENTRYPOINT
USER appuser

EXPOSE 8080

CMD "bash"
