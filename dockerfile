FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install flask kafka-python requests

CMD ["python", "app.py"]