# displaypi

A modular dashboard system for the Waveshare 7.3" 6-Color E-Paper Screen on Raspberry Pi 5. Display weather, tasks, NASA images, personal photos, or anything custom—all managed through a React-based dashboard interface.

## Features

- **Custom Dashboard**: React + Vite frontend renders real-time dashboard to the e-paper display
- **Modular Display System**: Easily add new display types (weather, tasks, images, etc.)
- **Scheduled Updates**: Morning/evening displays with cron job support
- **NASA Image Viewer**: Automatic daily image fetching and display
- **Private Image Gallery**: Display random images from a custom collection
- **Cross-Platform**: Runs on Raspberry Pi 5 and laptops for development

## Tech Stack

- **Backend**: Python (image conversion, API integration, e-paper driver)
- **Frontend**: React + Vite (dashboard UI)
- **Display**: Waveshare 7.3" 6-Color E-Paper Screen

## Quick Start

```bash
# Install dependencies
pip install -r requirements.pi.txt

# Display morning dashboard
just display-morning-today

# Display NASA image of the day
just display-nasa
```

See `justfile` for all available commands.

## Coming Soon

- Web-based control panel (hosted on RPi) for managing displays and scheduling

## Resources

- [Waveshare 7.3" E-Paper HAT Manual](https://www.waveshare.com/wiki/7.3inch_e-Paper_HAT_(E)_Manual#Overview)
