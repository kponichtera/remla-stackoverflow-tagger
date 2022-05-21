FROM python:3.10

# Make new user as root
WORKDIR /app
RUN useradd -d /app appuser && chown -R appuser: /app


RUN apt-get update \
&& apt-get install -y --no-install-recommends git \
&& apt-get purge -y --auto-remove gcc libc-dev \
&& rm -rf /var/lib/apt/lists/*

# ...
# Copy files and install dependencies still as root
COPY . .
RUN python -m pip install --upgrade pip &&\
    pip install -r requirements.txt

# Step down from being a root before calling CMD/ENTRYPOINT
USER appuser

RUN mkdir models

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
