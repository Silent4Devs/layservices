FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install uv

CMD ["uv", "run", "--only-group", "dev", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]