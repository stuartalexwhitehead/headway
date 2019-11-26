ARG NODE_VERSION=latest
ARG PORT=3001
ARG APPLICATION_PATH=/app

# prod dependencies
# --------------------------------------------------
FROM node:${NODE_VERSION} AS dependencies-prod
ARG APPLICATION_PATH

WORKDIR $APPLICATION_PATH

ADD ./yarn.lock ./yarn.lock
ADD ./package.json ./package.json

RUN yarn install --production

# dev dependencies
# --------------------------------------------------
FROM node:${NODE_VERSION} AS dependencies-dev
ARG APPLICATION_PATH

WORKDIR $APPLICATION_PATH

COPY --from=dependencies-prod $APPLICATION_PATH/node_modules $APPLICATION_PATH/node_modules

ADD ./yarn.lock ./yarn.lock
ADD ./package.json ./package.json

RUN yarn install