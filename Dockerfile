FROM python:3.8-slim
WORKDIR /app
RUN apt-get update && apt-get install -y
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install  -r requirements.txt
