# 1. Base Stage: Common setup for installing dependencies
FROM python:3.14-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# OPTION 1: Update OS packages to patch vulnerabilities like OpenSSL
# We do this as root before switching users or installing app deps
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Install uv, the package manager from Astral
RUN pip install uv

# Create a virtual environment
RUN python -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"

# 2. Builder Stage
FROM base AS builder
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-cache

# 3. Development Stage
FROM base AS development
COPY pyproject.toml uv.lock ./
RUN uv sync --no-cache

COPY ./templates ./templates

ARG HOST=0.0.0.0
ARG PORT=8080
ENV HOST=${HOST}
ENV PORT=${PORT}

CMD sh -c 'uvicorn app.main:app --host $HOST --port "$PORT" --reload'

# 4. Production Stage: Create the final, lean application image
FROM python:3.14-slim AS production

WORKDIR /app

# IMPORTANT: You must repeat the upgrade here because 'FROM python:3.14-slim'
# starts a fresh layer separate from the 'base' stage above.
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user for better security
RUN groupadd --system app && useradd --system --gid app app
USER app

# Copy the virtual environment with dependencies from the builder stage
COPY --from=builder /app/.venv ./.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY --chown=app:app ./app ./app
COPY --chown=app:app ./templates ./templates

ARG HOST=0.0.0.0
ARG PORT=8080
ENV HOST=${HOST}
ENV PORT=${PORT}

EXPOSE $PORT

CMD sh -c 'uvicorn app.main:app --host $HOST --port "$PORT"'
