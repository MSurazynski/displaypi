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
    python3 tasks.py
    shot-scraper http://localhost:5173 -o image.png --width 480 --height 800
    rm --force images-to-convert/*
    mv image.png images-to-convert/image.png
    python3 convert.py

ss-rpi:
    python3 weather.py
    python3 tasks.py
    pkill -f "npm run dev" || true
    cd dashboard && screen -dmS vite npm run dev
    sleep 3
    shot-scraper http://localhost:5173 -o image.png --width 480 --height 800
    pkill -f "npm run dev" || true
    rm --force images-to-convert/*
    mv image.png images-to-convert/image.png
    python3 convert.py
