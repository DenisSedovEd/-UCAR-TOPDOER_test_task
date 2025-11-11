#!/bin/bash
set -e

# Apply alembic migrations before starting app
alembic upgrade head

# Run regular CMD (uvicorn)
exec "$@"