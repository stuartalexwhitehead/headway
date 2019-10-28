ARG PYTHON_VERSION=latest
ARG PORT=8000
ARG APPLICATION_PATH=/app
ARG DEPENDENCY_PATH=/dependencies

# 1. download and build prod dependencies
# --------------------------------------------------
FROM python:${PYTHON_VERSION} AS dependencies-prod
ARG DEPENDENCY_PATH

ADD ./requirements/prod.txt ./requirements/prod.txt
RUN pip wheel --wheel-dir=${DEPENDENCY_PATH} -r requirements/prod.txt

# 2. download and build dev dependencies
# --------------------------------------------------
FROM python:${PYTHON_VERSION} AS dependencies-dev
ARG DEPENDENCY_PATH

COPY --from=dependencies-prod ${DEPENDENCY_PATH} ${DEPENDENCY_PATH}

ADD ./requirements ./requirements
RUN pip wheel --wheel-dir=${DEPENDENCY_PATH} --find-links=${DEPENDENCY_PATH} -r requirements/dev.txt

# 3. install prod dependencies from Wheels
# --------------------------------------------------
FROM python:${PYTHON_VERSION} AS prod
ARG PORT
ARG APPLICATION_PATH
ARG DEPENDENCY_PATH

WORKDIR $APPLICATION_PATH

COPY --from=dependencies-prod ${DEPENDENCY_PATH} ${DEPENDENCY_PATH}

ADD ./requirements/prod.txt ./requirements/prod.txt
RUN pip install --no-index --find-links=${DEPENDENCY_PATH} -r requirements/prod.txt

ADD . .

EXPOSE $PORT

# 4. install dev dependencies from Wheels
# --------------------------------------------------
FROM python:${PYTHON_VERSION} AS dev
ARG PORT
ARG APPLICATION_PATH
ARG DEPENDENCY_PATH

WORKDIR $APPLICATION_PATH

COPY --from=dependencies-dev ${DEPENDENCY_PATH} ${DEPENDENCY_PATH}

ADD ./requirements ./requirements
RUN pip install --no-index --find-links=${DEPENDENCY_PATH} -r requirements/dev.txt

ADD . .

EXPOSE $PORT
