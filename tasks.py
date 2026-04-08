from dotenv import load_dotenv
import os
import requests
from datetime import datetime
import json

load_dotenv()
TOKEN = os.getenv("TODOIST_TOKEN")
TODAY = str(datetime.now().date())

def get_all_tasks():
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

all_tasks = get_all_tasks()
result = {}

result['tasks'] = []
result['more-than-three'] = False

for task in all_tasks:
    if task.get("due") and str(task["due"]["date"]) == TODAY:
        result['tasks'].append({"title": task["content"]})

if len(result['tasks']) > 3:
    result['tasks'] = result['tasks'][:3]
    result['more-than-three'] = True;

os.makedirs("data", exist_ok=True)
with open("data/tasks.json", "w") as f:
    json.dump(result, f, indent=2)