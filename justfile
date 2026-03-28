sync:
    @echo "Starting syncing..."
    git pull
    @echo "Finished syncing..."

run: sync
    @echo "Running..."
    python3 display_image.py 

convert: sync
    @echo "Running..."
    python3 convert.py