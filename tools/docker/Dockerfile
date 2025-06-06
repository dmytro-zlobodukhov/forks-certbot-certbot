#base image
FROM python:3.12-alpine3.20 AS certbot

ENTRYPOINT [ "certbot" ]
EXPOSE 80 443
VOLUME /etc/letsencrypt /var/lib/letsencrypt
WORKDIR /opt/certbot

# Copy certbot code
COPY CHANGELOG.md README.rst src/
COPY tools tools
COPY acme src/acme
COPY certbot src/certbot

# Install certbot runtime dependencies
RUN apk add --no-cache --virtual .certbot-deps \
        libffi \
        libssl3 \
        openssl \
        ca-certificates \
        binutils

# We set this environment variable and install git while building to try and
# increase the stability of fetching the rust crates needed to build the
# cryptography library
ARG CARGO_NET_GIT_FETCH_WITH_CLI=true
# Install certbot from sources
#
# For some reason, setting the CARGO_LOG and CARGO_TERM_VERBOSE environment
# variables and -v/--verbose flags on pip seems to help cryptography builds not
# hang when building Docker images for other architectures using QEMU. See
# https://github.com/certbot/certbot/issues/10020. This may hopefully also help
# us to get more information about the problem to aid further debugging.
RUN apk add --no-cache --virtual .build-deps \
        gcc \
        linux-headers \
        openssl-dev \
        musl-dev \
        libffi-dev \
        python3-dev \
        cargo \
        git \
        pkgconfig \
    && CARGO_LOG=trace CARGO_TERM_VERBOSE=true python tools/pip_install.py \
            --no-cache-dir -vvv \
            --editable src/acme \
            --editable src/certbot \
    && apk del .build-deps \
    && rm -rf ${HOME}/.cargo

#static definition for making a plugin, but beware that
#using this layer definition will cause collisions if you make
#extensive use of the cache.
FROM certbot AS certbot-plugin
COPY --from=plugin-src . /opt/certbot/src/plugin
RUN python tools/pip_install.py --no-cache-dir --editable /opt/certbot/src/plugin
