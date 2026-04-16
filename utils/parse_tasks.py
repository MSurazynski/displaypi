from dotenv import load_dotenv
from pathlib import Path
import os
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

def load_and_parse_tasks():
    """
    Fetch all tasks from the Todoist API, handling pagination if necessary.
    """
    token = os.getenv("TODOIST_TOKEN")
    if not token:
        raise RuntimeError("TODOIST_TOKEN is not set")

    all_tasks = []
    cursor = None

    while True:
        params = {}
        if cursor:
            params["cursor"] = cursor

        response = requests.get(
            "https://api.todoist.com/api/v1/tasks",
            params=params,
            headers={"Authorization": f"Bearer {token}"},
            timeout=20,
        )

        print("Todoist status:", response.status_code)
        print("Todoist content-type:", response.headers.get("Content-Type"))
        print("Todoist body preview:", repr(response.text[:300]))

        response.raise_for_status()

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as e:
            raise RuntimeError(
                f"Todoist did not return JSON. "
                f"status={response.status_code}, "
                f"content_type={response.headers.get('Content-Type')}, "
                f"body={response.text[:300]!r}"
            ) from e

        all_tasks.extend(data.get("results", []))

        cursor = data.get("next_cursor")
        if not cursor:
            break

    return all_tasks
