FROM python:3.9
LABEL maintainer="developer@dotoryspace.com"

COPY . /app/server

WORKDIR /app/server

RUN pip install --upgrade pip
RUN pip3 install --upgrade pip

CMD ["python", "--version"]
CMD ["pip", "--version"]

RUN pip install --no-cache-dir -r requirements.txt
RUN export FLASK_ENV=production

ENTRYPOINT ["python", "run.py", "False", "0.0.0.0", "80"]
