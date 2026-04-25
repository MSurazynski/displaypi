import shutil
from playwright.sync_api import sync_playwright
from pathlib import Path
import subprocess
import time
import config.config as config
import logging

logger = logging.getLogger(__name__)


def start_vite():
    """
    Starts the Vite development server in a detached screen session. If a session named "vite" already exists, it will be terminated first.
    """
    subprocess.run(
        ["screen", "-S", "vite", "-X", "quit"],
        stderr=subprocess.DEVNULL,
    )

    subprocess.run(
        ["screen", "-dmS", "vite", "npm", "run", "dev"],
        cwd=config.DASHBOARD_PAGE_PROJECT_DIR,
        check=True,
    )


def stop_vite():
    """
    Stops the Vite development server by terminating the screen session named "vite". If no such session exists, it will simply do nothing.
    """
    subprocess.run(
        ["screen", "-S", "vite", "-X", "quit"],
        stderr=subprocess.DEVNULL,
    )


def take_screenshot():
    """
    Takes a screenshot of the Vite development server running on http://localhost:5173
    and saves it to the output path.
    """
    output_path = (
        config.TEMP_IMAGE_DIRECTORY_PATH / config.DASHBOARD_NOT_CONVERTED_IMAGE_NAME
    )

    chromium = shutil.which("chromium") or shutil.which("chromium-browser")

    if chromium is None:
        raise RuntimeError("Chromium not found. Install chromium or chromium-browser.")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=chromium,
            headless=True,
            args=["--no-sandbox"],
        )

        page = browser.new_page(
            viewport={"width": 480, "height": 800},
            device_scale_factor=1,
        )

        page.goto("http://localhost:5173", wait_until="networkidle")
        page.screenshot(
            path=str(output_path),
            full_page=False,
        )

        browser.close()


def main():
    """
    Starts the Vite development server, waits for it to be ready, takes a screenshot of the dashboard page, and then stops the server.
    The screenshot is saved to the specified output path.
    """
    start_vite()

    logger.info("Waiting for npm...")
    time.sleep(1)

    take_screenshot()
    stop_vite()

    logger.info("Dashboard screenshot taken successfully.")


if __name__ == "__main__":
    main()
