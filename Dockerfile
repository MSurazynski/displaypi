FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /displayi

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin \

COPY . .

RUN uv sync --locked --no-dev

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["help"]
