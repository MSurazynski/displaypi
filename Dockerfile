FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /displayi

RUN apt-get update \
    && apt-get install -y --no-install-recommends just

COPY . .

RUN uv sync --locked --no-dev

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["help"]
