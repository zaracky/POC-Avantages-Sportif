FROM python:3.11

WORKDIR /app

RUN pip install kafka-python requests psycopg2 

COPY listener.py .

CMD ["python", "listener.py"]
