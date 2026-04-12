set shell := ["bash", "-c"]
venv_python := "venv/bin/python3"

sync:
    @echo "Starting syncing..."
    git pull
    @echo "Finished syncing..."

display-morning-today:
    @echo "Starting display-morning-today..."
    venv/bin/python3 main.py --type dashboard --daytime morning --day today
    @echo "Finished display-morning-today..."

display-evening-today:
    @echo "Starting display-evening-today..."
    venv/bin/python3 main.py --type dashboard --daytime evening --day today
    @echo "Finished display-evening-today..."

display-nasa:
    @echo "Starting display-nasa..."
    venv/bin/python3 main.py --type nasa
    @echo "Finished display-nasa..."

display-random-private-image:
    @echo "Starting display-random-private-image..."
    venv/bin/python3 main.py --type random-image
    @echo "Finished display-private-random-image..."

load-data:
    venv/bin/python3 -m utils.data

requirements-laptop:
    venv/bin/python3 -m pip freeze > requirements.laptop.txt
    @echo "Generated requirements.laptop.txt"

requirements-pi:
    venv/bin/python3 -m pip freeze --local > requirements.pi.txt
    @echo "Generated requirements.pi.txt"

apt-pi:
    dpkg-query -W -f='${binary:Package}\n' \
        python3-gpiozero \
        python3-lgpio \
        python3-rpi-lgpio \
        > apt-packages.pi.txt
    @echo "Generated apt-packages.pi.txt"

export-all-laptop:
    just requirements-laptop

export-all-pi:
    just requirements-pi
    just apt-pi
    git add requirements.pi.txt apt-packages.pi.txt
    git commit -m "Update Raspberry Pi dependency snapshots" || true
    git push
