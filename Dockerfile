FROM node:23-slim AS jsbuilder
WORKDIR /app
COPY . .
RUN npm ci; npm run build

ENV UV_PYTHON_DOWNLOADS=0

FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS pybuilder

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.13-slim-bookworm

COPY --from=pybuilder --chown=app:app /app /app
COPY --from=jsbuilder /app/ui/dist /app/dist

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="."

WORKDIR /app

ENTRYPOINT ["python", "tbot2/runner.py"]

# docker build -t thomaserlang/tbot --rm . 
# docker push thomaserlang/tbot:latest 