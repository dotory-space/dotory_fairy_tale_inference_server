FROM python:3.9
LABEL maintainer="developer@dotoryspace.com"

COPY . /app/server

WORKDIR /app/server

RUN pip3 install -r requirements.txt --no-cache-dir
RUN export FLASK_ENV=production

ENTRYPOINT ["python3", "run.py", "False", "0.0.0.0", "80"]
