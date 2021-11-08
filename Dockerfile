FROM ubuntu:18.04
LABEL maintainer="developer@dotoryspace.com"

RUN sudo apt update
RUN sudo apt install software-properties-common
RUN sudo add-apt-repository ppa:deadsnakes/ppa
RUN sudo apt install python3.9

COPY . /app/server

WORKDIR /app/server

RUN pip3 install --upgrade setuptools pip

RUN pip3 install --no-cache-dir -r requirements.txt
RUN export FLASK_ENV=production

ENTRYPOINT ["python3.9", "run.py", "False", "0.0.0.0", "80"]
