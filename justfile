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

ss: 
    python3 weather.py
    shot-scraper http://localhost:5173 -o image.png --width 480 --height 800
    rm --force images-to-convert/*
    mv image.png images-to-convert/image.png
    python3 convert.py
