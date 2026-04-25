FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /displayi

# Install system build dependencies needed by Python packages
RUN echo "Installing system build dependencies: gcc, build-essential, python3-dev..." \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        python3-dev \
        chromium

# Install tools needed for downloading/installing just
RUN echo "Installing curl and ca-certificates..." \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        screen

# Install just command runner
RUN echo "Installing just..." \
    && curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin \
    && just --version

COPY . .

RUN uv sync --locked --no-dev

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["help"]
