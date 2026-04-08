set shell := ["bash", "-c"]

sync:
    source venv/bin/activate
    @echo "Starting syncing..."
    git pull
    @echo "Finished syncing..."

run: sync
    @echo "Running..."
    python3 display_image.py 

convert: sync
    @echo "Running..."
    python3 convert.py

ss: sync 
    python3 weather.py
    python3 tasks.py
    shot-scraper http://localhost:5173 -o image.png --width 480 --height 800
    rm --force images-to-convert/*
    mv image.png images-to-convert/image.png
    python3 convert.py

ss-rpi: sync
    python3 weather.py
    python3 tasks.py
    screen -S vite -X quit || true
    cd dashboard-page && screen -dmS vite npm run dev
    @echo "Wait for npm..."
    sleep 3
    shot-scraper http://localhost:5173 -o image.png --width 480 --height 800
    screen -S vite -X quit || true
    rm --force images-to-convert/*
    mv image.png images-to-convert/image.png
    python3 convert.py
