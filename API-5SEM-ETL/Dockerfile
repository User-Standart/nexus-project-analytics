FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir polars "psycopg[binary]"

CMD ["python", "etl/main.py"]
