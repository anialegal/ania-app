FROM python:3.12-slim

WORKDIR /app

COPY ./app /app
COPY ../common /app/common

RUN pip install --upgrade pip
RUN pip install fastapi "uvicorn[standard]" sqlmodel sqlalchemy redis celery python-dotenv

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

