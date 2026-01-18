FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock .
RUN uv sync

COPY app .

ENTRYPOINT ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]
