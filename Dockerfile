# FROM python:3.13-slim-bookworm

# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1 \
#     UV_LINK_MODE=copy \
#     UV_COMPILE_BYTECODE=1 \
#     UV_NO_DEV=1 \
#     UV_FROZEN=1 \
#     PYTHONPATH=/app \
#     PATH="/root/.local/bin:$PATH"

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends curl ca-certificates \
#     && rm -rf /var/lib/apt/lists/* \
#     && curl -LsSf https://astral.sh/uv/install.sh | sh

# WORKDIR /app

# COPY pyproject.toml uv.lock ./
# RUN uv sync --frozen --no-install-project --no-dev

# COPY . .

# RUN uv sync --frozen --no-dev

# EXPOSE 8002

# CMD ["uv", "run", "python", "-m", "bin.api"]


# -------- STAGE 1: build dependencies --------
FROM python:3.13-slim-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# system deps (минимально нужные)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

# копируем только зависимости (для кеша)
COPY pyproject.toml uv.lock ./

# создаём venv и ставим зависимости
RUN /root/.local/bin/uv sync --frozen --no-dev


# -------- STAGE 2: runtime --------
FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# только runtime зависимости ОС (минимум)
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# копируем готовое окружение из builder
COPY --from=builder /app /app
COPY --from=builder /root/.local /root/.local

# добавляем venv в PATH
ENV PATH="/app/.venv/bin:/root/.local/bin:$PATH"

# копируем код
COPY . .

EXPOSE 8002

# НЕ используем uv в runtime
CMD ["python", "-m", "bin.api"]