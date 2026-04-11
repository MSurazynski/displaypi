set shell := ["bash", "-c"]

sync:
    @echo "Starting syncing..."
    git pull
    @echo "Finished syncing..."

display-morning-today:
    @echo "Running..."
    python3 main.py --daytime morning --day today

write-requirements:
    source venv/bin/activate
    pip freeze > requirements.txt