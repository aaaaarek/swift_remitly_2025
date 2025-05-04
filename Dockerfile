FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install fastapi uvicorn sqlalchemy pandas openpyxl

EXPOSE 8080

CMD ["sh", "-c", "python parser.py && uvicorn main:app --host 0.0.0.0 --port 8080"]
