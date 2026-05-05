FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[dev]"

COPY app/ ./app/
COPY config/ ./config/
COPY gunicorn.conf.py ./
COPY scripts/ ./scripts/

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
