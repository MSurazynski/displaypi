set shell := ["bash", "-c"]
venv_python := "venv/bin/python3"

sync:
    @echo "Starting syncing..."
    git pull
    @echo "Finished syncing..."

display-morning-today:
    @echo "Starting display-morning-today..."
    uv run main.py --type dashboard --daytime morning --day today
    @echo "Finished display-morning-today..."

display-evening-today:
    @echo "Starting display-evening-today..."
    uv run main.py --type dashboard --daytime evening --day today
    @echo "Finished display-evening-today..."

display-morning-tomorrow:
    @echo "Starting display-evening-tomorrow..."
    uv run main.py --type dashboard --daytime morning --day tomorrow
    @echo "Finished display-evening-tomorrow..."

display-nasa:
    @echo "Starting display-nasa..."
    uv run main.py --type nasa
    @echo "Finished display-nasa..."

display-random-private-image:
    @echo "Starting display-random-private-image..."
    uv run main.py --type random-image
    @echo "Finished display-private-random-image..."
