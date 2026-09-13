# --- Build stage: use uv to install dependencies fast, into a venv ---
FROM python:3.12-slim AS builder

# Install uv (static binary, no pip needed)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# Copy only dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install only production deps (no dev group), into /app/.venv
RUN uv sync --frozen --no-dev --no-install-project

# Now copy the app code and finalize the venv
COPY app.py .
RUN uv sync --frozen --no-dev

# --- Final stage: copy the built venv + app code only ---
FROM python:3.12-slim

WORKDIR /app

RUN useradd --create-home --shell /bin/bash appuser

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app.py .

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 5000

ENV APP_ENV=production
ENV PORT=5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "app:app"]
