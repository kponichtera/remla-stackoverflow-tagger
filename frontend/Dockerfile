FROM node:16.15 AS builder
ARG TASK_URL=https://github.com/go-task/task/releases/download/v3.12.1/task_linux_amd64.deb

ENV CHROME_BIN /usr/bin/chromium

RUN apt-get update \
    && apt-get install -y curl chromium \
    && rm -rf /var/lib/apt/lists/*

RUN curl -o task.deb -L ${TASK_URL} \
    && dpkg -i task.deb \
    && rm task.deb

WORKDIR /build

# Warm up the cache
ENV npm_config_cache /npm-cache
COPY package.json package-lock.json ./
RUN npm install \
    && chmod -R 777 ${npm_config_cache}

CMD ["npm", "start"]

FROM builder AS build

COPY . .
RUN npm run-script build

FROM nginx:1.21.6-alpine AS final

# Set to /etc/nginx/templates/dev to use the development template
# that proxies the API requests to the inference service
ENV NGINX_ENVSUBST_TEMPLATE_DIR /etc/nginx/templates/dist

COPY docker/nginx/ /etc/nginx/templates/

COPY --from=build /build/dist/remla-stackoverflow-tagger/ /usr/share/nginx/html
