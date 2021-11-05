FROM python:3.9
LABEL maintainer="developer@dotoryspace.com"

COPY . /app/server

WORKDIR /app/server

RUN pip install -r requirements.txt
RUN export FLASK_ENV=production

ENTRYPOINT ["python", "run.py", "False", "0.0.0.0", "80"]