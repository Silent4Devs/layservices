FROM python:3.12
WORKDIR /app

COPY . /app

RUN pip install uv
RUN uv sync --only-group dev

RUN cd /app/app && uv run --only-group dev alembic upgrade head

WORKDIR /app

CMD sh -c "cd /app/app && uv run --only-group dev alembic upgrade head && cd /app && uv run --only-group dev uvicorn main:app --host 0.0.0.0 --port 8000 --reload"