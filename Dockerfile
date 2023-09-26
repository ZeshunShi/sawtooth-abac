# Use Ubuntu 18.04 as the base image
FROM ubuntu:bionic

# Install necessary tools, libraries, and C dependencies
RUN apt-get update \
 && apt-get install -y python3 python3-pip libffi-dev python3-dev

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the current directory into the container
COPY . .

# Install Python 3 specific dependencies
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install marshmallow-annotations marshmallow~=3.2

# Make the log directory
RUN mkdir /var/log/sawtooth

# Install the package using Python 3
RUN python3 setup.py install

# Expose necessary port
# EXPOSE 4004/tcp

# Set the default command for the container
# CMD ["abac-tp-python", "-vv"]
