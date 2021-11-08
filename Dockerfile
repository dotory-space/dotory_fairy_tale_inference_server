FROM ubuntu:18.04
LABEL maintainer="developer@dotoryspace.com"

RUN apt update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.9 python3-pip

COPY . /app/server

WORKDIR /app/server

RUN pip3 install --upgrade setuptools pip

RUN pip3 install --no-cache-dir -r requirements.txt
RUN export FLASK_ENV=production

ENTRYPOINT ["python3.9", "run.py", "False", "0.0.0.0", "80"]
