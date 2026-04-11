from dotenv import load_dotenv
import os
import requests
from datetime import datetime
import json

load_dotenv()
TOKEN = os.getenv("TODOIST_TOKEN")
TODAY = str(datetime.now().date())

def load_and_parse_tasks():
    '''
    Fetches all tasks from the Todoist API, handling pagination if necessary, and returns a list of tasks.
    '''
    
    all_tasks = []
    cursor = None

    while True:
        params = {}
        if cursor:
            params["cursor"] = cursor

        response = requests.get(
            "https://api.todoist.com/api/v1/tasks",
            params=params,
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        data = response.json()
        all_tasks.extend(data["results"])

        # Stop if no more pages
        if not data.get("next_cursor"):
            break
        cursor = data["next_cursor"]

    return all_tasks