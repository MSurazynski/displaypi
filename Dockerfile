FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# App lives here inside the container
WORKDIR /displayi

# Install system packages:
# - gcc/build-essential/python3-dev: needed by some Python packages during install
# - chromium: used by Playwright for screenshots
# - curl/ca-certificates: needed to install just
# - screen: used by your Python code to run Vite in the background
# - nodejs/npm: needed to run the Vite dashboard with `npm run dev`
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        python3-dev \
        chromium \
        curl \
        ca-certificates \
        screen \
        nodejs \
        npm \
    && rm -rf /var/lib/apt/lists/*

# Install just command runner
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh \
    | bash -s -- --to /usr/local/bin \
    && just --version

# Copy the project into the image
COPY . .

# Install Python dependencies from uv.lock
RUN uv sync --locked --no-dev

# Install frontend dependencies for the Vite dashboard.
# IMPORTANT: change `dashboard-page` to the directory that contains your package.json.
RUN cd dashboard-page && npm ci

# Make the entrypoint executable
RUN chmod +x entrypoint.sh

# Use your entrypoint script
ENTRYPOINT ["./entrypoint.sh"]

# Default command when no command is provided
CMD ["help"]
