FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# App lives here inside the container.
WORKDIR /displayi

# Install base system packages.
#
# gcc/build-essential/python3-dev:
#   Needed if any Python packages compile native extensions.
#
# chromium:
#   Used by Playwright to take screenshots.
#
# curl/ca-certificates/gnupg:
#   Needed to install external tools and NodeSource's Node.js repository.
#
# screen:
#   Used by your Python code to run the Vite dev server in the background.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        python3-dev \
        chromium \
        curl \
        ca-certificates \
        gnupg \
        screen \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 22.
#
# Do not use Debian Bookworm's default nodejs package here because
# modern Vite versions require Node 20.19+ or 22.12+.
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && node --version \
    && npm --version \
    && rm -rf /var/lib/apt/lists/*

# Install just command runner.
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh \
    | bash -s -- --to /usr/local/bin \
    && just --version

# Copy the project into the image.
COPY . .

# Install Python dependencies from uv.lock.
RUN uv sync --locked --no-dev

# Install frontend dependencies for the Vite dashboard.
#
# This assumes your Vite app is at:
#   /displayi/dashboard-page
#
# It must be the directory containing package.json and package-lock.json.
RUN cd dashboard-page && npm ci

# Make the entrypoint executable.
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["help"]
