FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libsqlite3-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./

RUN uv pip install --system --no-cache-dir .

COPY . .

ENV PYTHONPATH=/app

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]