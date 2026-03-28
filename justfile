sync:
    @echo "Starting syncing..."
    git pull
    @echo "Finishes syncing..."

run: sync
    @echo "Running..."
    git display_image.py 