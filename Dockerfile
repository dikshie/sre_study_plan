# --- Build stage: install dependencies into a venv ---
FROM python:3.12-slim AS builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Final stage: copy venv + app code only ---
FROM python:3.12-slim

WORKDIR /app

# Create a non-root user (good practice, and interview-relevant)
RUN useradd --create-home --shell /bin/bash appuser

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY app.py .

USER appuser

EXPOSE 5000

ENV APP_ENV=production
ENV PORT=5000

# gunicorn is more production-appropriate than Flask's dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "app:app"]
