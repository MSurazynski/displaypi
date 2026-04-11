set shell := ["bash", "-c"]

sync:
    @echo "Starting syncing..."
    git pull
    @echo "Finished syncing..."

display-morning-today:
    @echo "Running..."
    python3 main.py --daytime morning --day today
    @echo "Finished!"

display-evening-today:
    @echo "Running..."
    python3 main.py --daytime evening --day today
    @echo "Finished!"

load-data:
    python3 -m utils.data.py

write-requirements:
    source venv/bin/activate
    pip freeze > requirements.txt