set shell := ["bash", "-c"]

sync:
    @echo "Just: Starting syncing..."
    git pull
    @echo "Just: Finished syncing..."

display-morning-today:
    @echo "Just: Starting display-morning-today..."
    uv run main.py --type dashboard --daytime morning --day today
    @echo "Just: Finished display-morning-today..."

display-evening-today:
    @echo "Just: Starting display-evening-today..."
    uv run main.py --type dashboard --daytime evening --day today
    @echo "Just: Finished display-evening-today..."

display-morning-tomorrow:
    @echo "Just: Starting display-evening-tomorrow..."
    uv run main.py --type dashboard --daytime morning --day tomorrow
    @echo "Just: Finished display-evening-tomorrow..."

display-nasa:
    @echo "Just: Starting display-nasa..."
    uv run main.py --type nasa
    @echo "Just: Finished display-nasa..."

display-random-private-image:
    @echo "Just: Starting display-random-private-image..."
    uv run main.py --type random-image
    @echo "Just: Finished display-private-random-image..."

docker-run command:
    @echo "Just: Running Docker command: {{command}}"
    sudo docker run --rm \
        --privileged \
        -v /dev:/dev \
        -v /run/udev:/run/udev:ro \
        displaypi {{command}}
