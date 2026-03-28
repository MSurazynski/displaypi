sync:
    @echo "Starting syncing..."
    git pull
    @echo "Finishes syncing..."

run: sync
    @echo "Running..."
    python3 display_image.py 