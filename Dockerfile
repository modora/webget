#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

FROM python:3.7.3

WORKDIR /tmp
# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Configure apt and install packages
RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils 2>&1 \
    #
    # Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
    && apt-get -y install git procps lsb-release \
    && pip install --upgrade pip

# ------------------------------------- COMMANDS -----------------------
# Copy requirements.txt (if found) to a temp locaition so we can install it. Also
# copy "noop.txt" so the COPY instruction does not fail if no requirements.txt exists.
COPY requirements*.txt pip-tmp/

RUN if [ -f "pip-tmp/requirements-dev.txt" ]; then pip install -r pip-tmp/requirements-dev.txt; fi
RUN if [ -f "pip-tmp/requirements.txt" ]; then pip install -r pip-tmp/requirements.txt; fi

# Install firefox webdriver
ENV GECKO_DRIVER_VERSION='v0.24.0'
RUN wget https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz \
        -O geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz \
        --quiet \
    && tar -xvzf geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/

# ------------------------------------ END -----------------------------
# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog


