from datetime import datetime
import json

result = [datetime.now().strftime("%A, %-d %B")]

with open("data/date.json", "w") as f:
    json.dump(result, f, indent=2)