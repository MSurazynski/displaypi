FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /displayi

COPY . .

RUN uv sync --locked --no-dev

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["help"]
