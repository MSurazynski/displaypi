# displaypi

Dashboard and image display system for the Waveshare 7.3" 6-color e-paper screen on Raspberry Pi 5.

## What it does

- Shows dashboard screens for morning/evening
- Displays NASA image of the day
- Displays a random private image
- Runs locally with `uv`
- Runs on Raspberry Pi through Docker with GPIO/SPI access

## Local usage

Install/sync dependencies:

```bash
uv sync
```

Run commands through `just`:

```bash
just display-morning-today
just display-evening-today
just display-morning-tomorrow
just display-nasa
just display-random-private-image
```

Sync latest code:

```bash
just sync
```

## Docker usage

Build the image:

```bash
sudo docker build -t displaypi .
```

Run through the Docker wrapper recipe:

```bash
just docker-run nasa
just docker-run morning-today
just docker-run evening-today
just docker-run morning-tomorrow
just docker-run random-image
```

The Docker run uses:

```bash
sudo docker run --rm \
  --privileged \
  -v /dev:/dev \
  -v /run/udev:/run/udev:ro \
  displaypi <command>
```

This is required so the container can access the Raspberry Pi GPIO/SPI devices.

## Docker commands

The container entrypoint supports:

```text
morning-today
evening-today
morning-tomorrow
nasa
random-image
sync
help
```

Example:

```bash
sudo docker run --rm --privileged -v /dev:/dev -v /run/udev:/run/udev:ro displaypi nasa
```

## Files

- `main.py` - main Python entrypoint
- `justfile` - local and Docker command shortcuts
- `entrypoint.sh` - Docker command router
- `Dockerfile` - container image definition
- `assets/` - generated and source images
- `utils/` - API, image, display, and helper code

## Resource

- [Waveshare 7.3" E-Paper HAT Manual](https://www.waveshare.com/wiki/7.3inch_e-Paper_HAT_(E)_Manual#Overview)
