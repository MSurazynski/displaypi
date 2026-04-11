set shell := ["bash", "-c"]

sync:
    @echo "Starting syncing..."
    git pull
    @echo "Finished syncing..."

display-morning-today:
    @echo "Running..."
    python3 main.py --daytime morning --day today

run:
    @echo "Running..."
    python3 display_image.py 

convert: sync
    @echo "Running..."
    venv/bin/python3 convert.py

ss: sync 
    venv/bin/python3 weather.py
    venv/bin/python3 tasks.py
    venv/bin/python3 date.py
    shot-scraper  http://localhost:5173 -o image.png --width 480 --height 800
    rm --force images-to-convert/*
    mv image.png images-to-convert/image.png
    python3 convert.py

ss-rpi: sync
    venv/bin/python3 weather.py
    venv/bin/python3 tasks.py
    venv/bin/python3 date.py
    screen -S vite -X quit || true
    cd dashboard-page && screen -dmS vite npm run dev
    @echo "Wait for npm..."
    sleep 3
    venv/bin/shot-scraper http://localhost:5173 -o image.png --width 480 --height 800
    screen -S vite -X quit || true
    rm --force images-to-convert/*
    mv image.png images-to-convert/image.png
    venv/bin/python3 convert.py

write-requirements:
    source venv/bin/activate
    pip freeze > requirements.txt