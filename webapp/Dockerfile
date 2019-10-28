ARG NODE_VERSION=latest
ARG PORT=3000
ARG APPLICATION_PATH=/app
ARG DEPENDENCY_PATH=/dependencies

# prod dependencies
# --------------------------------------------------
FROM node:${NODE_VERSION} AS dependencies-prod
ARG DEPENDENCY_PATH

WORKDIR $DEPENDENCY_PATH

ADD ./package.json ./package.json

RUN yarn install --production

# dev dependencies
# --------------------------------------------------
FROM node:${NODE_VERSION} AS dependencies-dev
ARG DEPENDENCY_PATH

WORKDIR $DEPENDENCY_PATH

COPY --from=dependencies-prod $DEPENDENCY_PATH/node_modules $DEPENDENCY_PATH/node_modules

ADD ./package.json ./package.json

RUN yarn install