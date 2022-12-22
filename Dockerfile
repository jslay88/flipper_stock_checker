# syntax=docker/dockerfile:1.4
FROM python:3-alpine as base

# Ensure that the environment uses UTF-8 encoding by default
ENV LANG en_US.UTF-8
# Disable pip cache dir
ENV PIP_NO_CACHE_DIR true
# Stops Python default buffering to stdout, improving logging to the console.
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /src
ENV APP_NAME flipper

WORKDIR ${APP_HOME}

# Install and update common OS packages, pip, setuptools, wheel, and awscli
RUN apk update --no-cache && apk upgrade --no-cache
RUN pip install --upgrade pip setuptools wheel
#######################################################################
# Intermediate layer to build only prod deps
FROM base as python-builder

# Install python requirements
COPY requirements.txt requirements.txt
RUN mkdir /build && pip install --prefix=/build -r requirements.txt

#######################################################################
# dev is used for local development
FROM python-builder AS dev

ENV PYTHONPATH ${APP_HOME}/${APP_NAME}

# Install python requirements
COPY requirements.txt requirements.txt
# RUN cp -Rfp /build/* /usr/local && rm -Rf /build && pip install -r requirements/local.txt
RUN cp -Rfp /build/* /usr/local && rm -Rf /build

ENTRYPOINT ["python"]
CMD ["flipper.py"]

#######################################################################
# prod layer
FROM base as prod
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG USERNAME=flipper

ENV PYTHONPATH ${APP_HOME}/${APP_NAME}
# Convert sercrets to environment variables
COPY <<EOF /etc/profile.d/secrets_env.sh
if [ -d /var/run/secrets ]; then
    for s in $(find -L /var/run/secrets/$APP_NAME -type f); do
        export $(basename \$s)=$(cat \$s);
    done
fi
EOF

# Copy Python requirements from builder layer
COPY --from=python-builder /build /usr/local

# Cleanup *.key files
RUN for i in $(find /usr/local/lib/python3* -type f -name "*.key*"); do rm "$i"; done

# Create non-root user
RUN addgroup -S -g $USER_GID $USERNAME \
    && adduser -S -u $USER_UID $USERNAME $USERNAME \
    && chown -Rf $USER_UID:$USER_GID ${APP_HOME}
USER $USERNAME

# Copy code
COPY --chown=$USER_UID:$USER_GID . .

ENTRYPOINT ["python"]
CMD ["flipper.py"]
