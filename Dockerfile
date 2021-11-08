FROM ubuntu:18.04
LABEL maintainer="developer@dotoryspace.com"

ARG DEBIAN_FRONTEND=noninteractive

# Update apt packages
RUN apt update
RUN apt upgrade -y

# Install vim, git
RUN apt install vim -y
RUN apt-get install -y git

# Install rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
RUN export PATH="$HOME/.cargo/bin:$PATH"

# Install python 3.9
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.9

# Install pip
RUN apt install python3-pip -y
RUN python3 -m pip install --upgrade pip

COPY . /app/server

WORKDIR /app/server

RUN pip3 install --upgrade pip setuptools wheel

RUN pip3 install --no-cache-dir -r requirements.txt
RUN export FLASK_ENV=production

ENTRYPOINT ["python3.9", "run.py", "False", "0.0.0.0", "80"]
